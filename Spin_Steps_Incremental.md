# General Rules
Go through in order
Add logging at each step to know a phase has passed
Mark DONE on each before proceeding to the next step
Don't move to the next step until I've told you to
Use the Meta Spatial SDK sample in samples/geo_voyage as a reference for all steps

# Incremental Implementation for Globe Spinning

## Phase 1: Basic Touch Detection (Learning Component Structure)
1. **Create a Simple Touchable Component**
   - Create a Touchable.xml component schema in app/src/main/components
   - Add a simple boolean attribute to track touch state
   - Register the generated component in ImmersiveActivity
   - Create a system that listens for touch events on touchable entities
   - Apply the Touchable component to the sphere entity
   - Log messages when touches are detected
   - Test to ensure touch detection works before adding more complexity

## Phase 2: Simple Rotation
1. **Create the Spinnable Component**
   - Create a simple version with just isSpinning flag and speed
   - Register the component in ImmersiveActivity
   - Apply it to the sphere entity

2. **Create a Minimal SpinnableSystem**
   - Implement a basic system that only handles constant rotation
   - Register the system in ImmersiveActivity
   - Test to verify component-based rotation works
   - Remove the Touchable component/system once this is working

## Phase 3: Input-Controlled Rotation
1. **Enhance SpinnableSystem with Input Handling**
   - Add input detection to the SpinnableSystem
   - Handle button press/release to toggle rotation
   - Start/stop rotation based on user input
   - Test to verify user can toggle rotation

## Phase 4: Advanced Rotation
1. **Implement Direction-Based Rotation**
   - Calculate rotation based on controller movement
   - Apply rotation directly when controller moves
   - Test to verify controller-guided rotation

2. **Add Inertia and Physics**
   - Implement momentum when releasing the globe
   - Add drag coefficient to slow down over time
   - Test to verify natural-feeling rotation

## Phase 5: Refinement
1. **Optimize and Polish**
   - Add pitch control (tilting)
   - Refine constants for optimal feel
   - Add visual/audio feedback
   - Final testing and debugging

This approach ensures we have a working implementation at each step, making it easier to identify and fix issues as they arise.
