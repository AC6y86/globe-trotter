#!/bin/bash
# run_gallery.sh: Unified script for building, installing, launching, and monitoring logcat for Gallery app
set -euo pipefail

# Default configuration
DEVICE=""
PACKAGE="com.paleyprojects.GlobeTrotter"
MODE="build-install"
POWERSHELL_SCRIPT="./gradlew assembleDebug"
PUSH_ASSETS_ONLY=0

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --launch-only) MODE="launch-only"; shift ;;
    --build-install) MODE="build-install"; shift ;;
    --push-assets-only) MODE="push-assets-only"; shift ;;
    --device) DEVICE="$2"; shift 2 ;;
    --package) PACKAGE="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# Detect device if not specified
if [[ -z "$DEVICE" ]]; then
  DEVICE=$(adb devices | awk 'NR>1 && $2=="device" {print $1}' | head -n 1)
  if [[ -z "$DEVICE" ]]; then
    echo "No Android device detected!" >&2
    exit 1
  fi
fi

# disable asset pushing for now
# Always update assets before running or launching
#SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
#"$SCRIPT_DIR/push_glxf_to_sd.sh"

# If only pushing assets and running, skip build/install
if [[ "$MODE" == "push-assets-only" ]]; then
  echo "[INFO] Assets pushed. Launching app only."
  MODE="launch-only"
fi

echo "Using device: $DEVICE"
echo "Using package: $PACKAGE"

# Build and install if requested
if [[ "$MODE" == "build-install" ]]; then
  WIN_PROJECT_ROOT=$(wslpath -w ".")
  echo "[1/4] Building APK via Gradle in Windows..."
  
  # Temporarily disable strict error handling for the build command
  set +e
  
  # Run the build command and capture its output
  powershell.exe -NoProfile -Command "cd \"$WIN_PROJECT_ROOT\"; $POWERSHELL_SCRIPT" 2>&1 | tee build_logs.txt
  BUILD_EXIT_CODE=$?
  
  # Re-enable strict error handling
  set -e
  
  # Check if the build failed either by exit code or by looking for specific failure patterns in the log
  if [ $BUILD_EXIT_CODE -ne 0 ] || grep -q "BUILD FAILED" build_logs.txt || grep -q "FAILURE:" build_logs.txt || grep -q "Compilation error" build_logs.txt; then
    echo ""
    echo "=============================================="
    echo "[ERROR] BUILD FAILED! Kotlin compilation errors detected."
    echo "See build_logs.txt for complete details."
    echo "=============================================="
    echo ""
    exit 1
  fi
  
  apk_path=$(find ./app/build/outputs/apk/debug -type f -name "*.apk" | head -n 1)
  if [ -z "$apk_path" ]; then
    echo "APK not found!" >&2
    exit 1
  fi
  echo "[2/4] APK found at $apk_path"

  echo "[3/4] Installing $apk_path to device $DEVICE..."
  adb -s "$DEVICE" install -r "$apk_path"
  echo "APK installed."
fi

# Clear logcat buffer before launching the app to ensure only new logs are present
adb -s "$DEVICE" logcat -c

# Quit the app if it is running
adb -s "$DEVICE" shell am force-stop "$PACKAGE"

# Launch the app
adb -s "$DEVICE" shell monkey -p "$PACKAGE" -c android.intent.category.LAUNCHER 1


# Run logcat with the dedicated monitoring script
echo "Monitoring for crashes (press Ctrl+C to stop)..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
adb -s "$DEVICE" logcat | python3 "$SCRIPT_DIR/monitor_logcat.py" "$PACKAGE"
MONITOR_EXIT=$?

# Check exit code from monitor script
if [ $MONITOR_EXIT -eq 0 ]; then
  # No crash detected (user manually stopped monitoring)
  echo "App monitoring stopped without detecting crashes."
  exit 0
elif [ $MONITOR_EXIT -eq 1 ]; then
  # Crash was detected and printed (monitor script exited with code 1)
  echo "Crash detected and logged."
  exit 1
else
  # Something unexpected happened
  echo "Logcat monitoring ended unexpectedly (code $MONITOR_EXIT)."
  exit 2
fi