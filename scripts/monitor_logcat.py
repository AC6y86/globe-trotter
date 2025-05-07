#!/usr/bin/env python3
# monitor_logcat.py: A script to monitor logcat output and print logs from app PIDs
# Can be used either with stdin or with a log file
# Usage:
#   adb logcat | ./monitor_logcat.py [PACKAGE_NAME]
#   ./monitor_logcat.py [PACKAGE_NAME] [LOG_FILE]

import sys
import argparse
import select
import os
import re
import time

def is_app_pid_line(line, package_name, pid):
    """Check if this line indicates a new app PID."""
    return (
        # Process start for our package
        f"Start proc {pid}:{package_name}" in line or
        # Activity manager starting our package
        f"pid={pid}" in line and package_name in line or
        # Activity manager with different format
        f"pid {pid}" in line and package_name in line and "for" in line or
        # Monkey test runner
        "W Monkey" in line and pid or
        # Our main activity logs
        "D ImmersiveActivity" in line or
        # Explicit process name mention
        f"Process {package_name} (pid {pid})" in line
    )

def is_crash_related(line, package_name):
    """Check if this line is related to a crash."""
    return any([
        # Crash log section marker
        "--------- beginning of crash" in line,
        # Fatal exceptions
        "FATAL EXCEPTION" in line,
        # Activity force finishing due to crash
        "Force finishing activity" in line and package_name in line,
        # Window death notifications
        "WIN DEATH" in line and package_name in line,
        # Native crashes
        "Native crash" in line,
        # Common crash signals
        "SIGSEGV" in line or "SIGABRT" in line,
        # Stack traces
        "backtrace:" in line,
        "Stack trace:" in line,
        # Java exceptions
        "AndroidRuntime: FATAL EXCEPTION:" in line,
        "AndroidRuntime: java.lang." in line,
        "Exception:" in line,
        # Native crash info
        "libc:" in line and ("Fatal signal" in line or "abort" in line),
        # Debug assertions
        "DEBUG" in line and package_name in line,
        # Common crash reporters
        "crash_dump" in line,
        "DEBUG:" in line and "Dumping" in line
    ])

def should_ignore_line(line, ignore_patterns):
    """Check if this line should be ignored based on patterns."""
    return any(pattern in line for pattern in ignore_patterns)

def process_line(line, app_pids, package_name, ignore_patterns, in_crash_section, whitelist_tags, last_line=None, repeat_count=0, max_repeats=0):
    """Process a single logcat line and determine if it should be printed."""
    # Skip empty lines
    if not line:
        return in_crash_section, False, None
    
    # Extract PID from the line
    pid_match = re.search(r'\s+(\d+)\s+\d+\s+([A-Z])\s+([^:]+)', line)
    if not pid_match:
        return in_crash_section, False, None
        
    current_pid = pid_match.group(1)
    log_level = pid_match.group(2)
    tag = pid_match.group(3).strip()
    
    # Check if this is a new app PID to track
    if current_pid and current_pid not in app_pids and package_name in line:
        if is_app_pid_line(line, package_name, current_pid):
            app_pids.add(current_pid)
            print(f"Found app PID: {current_pid}")
            return in_crash_section, True, current_pid
    
    # Check if this is a crash-related line
    if is_crash_related(line, package_name):
        if "--------- beginning of crash" in line:
            return True, True, None
        return in_crash_section, True, None
    
    # If we're in a crash section, print all lines
    if in_crash_section:
        return in_crash_section, True, None
    
    # First, filter out specific noisy errors regardless of PID
    if any(pattern in line for pattern in [
        # Media playback related
        "ExoPlayerImplInternal",
        "MediaCodec",
        "CodecException",
        "setSurface()",
        "Invalid to call at Released state",
        "rendering to non-initialized",
        "releaseOutputBuffer()",
        "BufferQueueProducer",
        "MediaPlayer",
        "AudioTrack",
        
        # System errors and warnings
        "ApkAssets",
        "Compatibility callbacks",
        "ClassNotFoundException",
        "NoClassDefFoundError",
        "Service not registered",
        "Timeout",
        "FetchBLEStatsTask",
        "W System",
        "type=1400",
        "audit"
    ]):
        return in_crash_section, False, None
        
    # Only show logs from our app's PID or with whitelisted tags
    if current_pid in app_pids or tag in whitelist_tags:
        # Skip lines that match ignore patterns
        if should_ignore_line(line, ignore_patterns):
            return in_crash_section, False, None
        return in_crash_section, True, None
    
    # Default: don't print
    return in_crash_section, False, None

def monitor_logcat(logcat_file, package_name, max_repeats=0, verbose=False, no_backup_filter=False):
    """Monitor logcat output and print logs from the specified package's PIDs only.
    Filter out repetitive system logs and noise.
    
    Args:
        logcat_file: File-like object containing logcat output
        package_name: Package name to monitor for logs
        
    Returns:
        Always returns 0
    """
    print(f"Monitoring logs for package: {package_name}...")
    print(f"Press Ctrl+C to stop monitoring")
    
    app_pids = set()
    in_crash_section = False
    
    # Only show logs with these tags (add more as needed)
    whitelist_tags = [
        "ImmersiveActivity",
        "GlobeTrotter",  # Add our custom tag for debug logs
        # Removed generic OpenXR tag to reduce noise
        # Only include specific VR-related tags we care about
        "VrApi",
        "Unity",
        "AndroidRuntime",
        "art",
        "System.err",
        "DEBUG",
        "WARN",
        "ERROR",
        "FATAL"
    ]
    
    # Patterns to ignore (noisy system logs)
    ignore_patterns = [
        # OpenXR permission checks and extensions
        "Required permission horizonos.permission",
        "Required permission com.oculus.permission",
        "xrEnumerateInstanceExtensionProperties: skipping extension",
        "Checking for permission",
        "PassesGKKillswitch",
        "checkTrexKillswitchGk",
        "xrPerfSettingsSetPerformanceLevelEXT",
        "xrCreateInstance",
        "xrCreateSession",
        "xrBeginSession",
        "PostSessionStateChange",
        "Extension status:",
        "missing uses-feature string",
        "missing uses-permission string",
        
        # Avatar and 3D rendering related
        "Avatar2ResourceSystem",
        "Failed to get TexCoord1 attribute",
        "LoadMorphTargets",
        "TexCoord1 attribute info for buffer",
        "Avatar2ResourceSystem: LoadMorphTargets: Failed to get TexCoord1",
        
        # Media and codec related
        "CCodecBufferChannel",
        "BufferQueueProducer",
        "dequeueBuffer",
        "Codec2Client",
        "query -- param skipped",
        "flushed work; ignored",
        "Discard frames from previous generation",
        "Ignoring stale input buffer",
        "DequeueBuffer: dequeueBuffer failed",
        
        # System framework
        "PersistableBundle",
        "ReactNativeJS",
        "IPCThreadState",
        "Adreno",
        "Failed acquire read lock",
        "diagnosticdata",
        "Choreographer",
        "OpenGLRenderer",
        "ViewRootImpl",
        "InputMethodManager",
        "HostConnection",
        "EGL_emulation",
        "SurfaceFlinger",
        "ConfigStore",
        "RenderThread",
        "ActivityThread",
        "ThreadPoolExecutor",
        "dalvikvm",
        "libEGL",
        "eglCodecCommon",
        
        # Networking and services
        "resolv",
        "netd",
        "crash-uploader",
        "CloudBackup",
        "UIManagerBinding",
        "VrApi",
        "AudioFlinger",
        "oneway function results",
        "CompatibilityChangeReporter",
        "Tracking",
        "MRSS",
        "MrRuntime",
        "VD628x",
        "UnifiedTelemetryLogger",
        
        # Backup related
        "FullBackup_native",
        "file_backup_helper",
        "BackupManagerService",
        "BackupRestoreController",

        # Oculus/Meta/PlaneFreeSpace JNI/NoSuchElementException noise
        "OculusFederatedComputingIPCServer: encountered JNI exception in EndGPRIPSTransaction: java.util.NoSuchElementException: Key",
        "OculusFederatedComputingIPCServer: java.util.NoSuchElementException: Key",
        "MIXEDREALITY: PlaneFreeSpace: PlaneFreespaceComputeCapability: GpripsClient: Exception in task: Failed to end transaction: java.util.NoSuchElementException: Key",

        # ExoPlayer and system errors
        "ExoPlayerImplInternal",  # Filter all ExoPlayer errors
        "No Compatibility callbacks set! Querying change",
        "type=1400 audit(0.0:",
        "FetchBLEStatsTask: FetchBLEStatsTask did not succeed",
        "IPCManager: java.lang.IllegalArgumentException: Service not registered",
        "System.err: INFO: com.whatsapp",

        "KeyValueBackupTask",
        "PFTBT",
        "KVBT",
        "OculusStorageFullBackupPlugin",
        "OculusCloudBackupManagementServiceClient",
        "measured [",
        "TrafficStats",
        "KvBackupCoordinator",
        "GraphQLClient",
        "OkHttpClientFacade"
    ]
    
    try:
        # Variables to track repeated lines
        last_line = None
        repeat_count = 0
        
        # If reading from stdin, use select to check for available input
        if logcat_file == sys.stdin:
            while True:
                # Check if there's data to read
                if select.select([logcat_file], [], [], 0.1)[0]:
                    line = logcat_file.readline().strip()
                    
                    # Apply backup filter if enabled
                    if not no_backup_filter and any(pattern in line for pattern in [
                        "FullBackup", "file_backup_helper", "BackupManagerService", "measured ["]):
                        continue
                    
                    in_crash_section, should_print, new_pid = process_line(
                        line, app_pids, package_name, ignore_patterns, in_crash_section,
                        whitelist_tags, last_line, repeat_count, max_repeats
                    )
                    
                    if should_print:
                        # Check for repeated lines
                        if line == last_line and max_repeats > 0:
                            repeat_count += 1
                            if repeat_count <= max_repeats:
                                print(line)
                            elif repeat_count == max_repeats + 1:
                                print(f"... (suppressing identical lines) ...")
                        else:
                            repeat_count = 0
                            print(line)
                        
                        last_line = line
        else:
            # If reading from a file, process line by line
            for line in logcat_file:
                line = line.strip()
                
                # Apply backup filter if enabled
                if not no_backup_filter and any(pattern in line for pattern in [
                    "FullBackup", "file_backup_helper", "BackupManagerService", "measured ["]):
                    continue
                
                in_crash_section, should_print, new_pid = process_line(
                    line, app_pids, package_name, ignore_patterns, in_crash_section,
                    whitelist_tags, last_line, repeat_count, max_repeats
                )
                
                if should_print:
                    # Check for repeated lines
                    if line == last_line and max_repeats > 0:
                        repeat_count += 1
                        if repeat_count <= max_repeats:
                            print(line)
                        elif repeat_count == max_repeats + 1:
                            print(f"... (suppressing identical lines) ...")
                    else:
                        repeat_count = 0
                        print(line)
                    
                    last_line = line
    
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    
    return 0

def main():
    parser = argparse.ArgumentParser(description='Monitor logcat for app PIDs and print only their logs')
    parser.add_argument('package_name', nargs='?', default='com.mycompany.GlobeTrotter',
                        help='Package name to monitor')
    parser.add_argument('log_file', nargs='?', help='Log file to process (optional)')
    parser.add_argument('-v', '--verbose', action='store_true', 
                        help='Show more verbose output (fewer filters)')
    parser.add_argument('-c', '--count', type=int, default=0,
                        help='Maximum number of consecutive identical lines to show (0 for unlimited)')
    parser.add_argument('-b', '--no-backup-filter', action='store_true',
                        help='Do not filter out backup-related logs')
    args = parser.parse_args()
    
    # If log file is provided, read from it
    if args.log_file:
        with open(args.log_file, 'r') as f:
            exit_code = monitor_logcat(f, args.package_name, args.count, args.verbose, args.no_backup_filter)
    # Otherwise, read from stdin
    else:
        exit_code = monitor_logcat(sys.stdin, args.package_name, args.count, args.verbose, args.no_backup_filter)
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
