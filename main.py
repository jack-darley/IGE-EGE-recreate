from psychopy import visual, monitors, event, core
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame(columns=["Trial", "Mouse X", "Mouse Y", "Cursor X", "Cursor Y"])
ts = pd.read_csv("tgt.csv") # trial schedule

# Monitor Specs
monitor_width = 2560  # in pixels
monitor_height = 1080  # in pixels
diagonal_inches = 29   # in inches

# Aspect Ratio Calculation
aspect_ratio_width = 21  # Standard aspect width for 16:9
aspect_ratio_height = 9  # Standard aspect height for 16:9

# Corrected Physical Width Calculation
physical_width_inches = (diagonal_inches * aspect_ratio_width) / math.sqrt(aspect_ratio_width**2 + aspect_ratio_height**2)

# Pixels Per Inch (PPI)
ppi = monitor_width / physical_width_inches

# mm to Pixel Conversion
mm2pixel = ppi / 25.4  # Since 1 inch = 25.4 mm

# Set unit
unit = "pix"

# Define and save a monitor profile
mon = monitors.Monitor(name="MyMonitor")
mon.setSizePix((monitor_width, monitor_height))  # Set resolution (width, height in pixels)
mon.setWidth(67.733)  # Screen width in cm
mon.setDistance(60)   # Distance in cm
mon.save()            # Save the settings

# Create the PsychoPy window using the monitor name (as a string)
win = visual.Window(
    size=(monitor_width, monitor_height),  # Actual resolution
    monitor="MyMonitor",                   # Use the saved monitor profile name
    fullscr=True,
    color=(-1, -1, -1),
    colorSpace='rgb',
    units=unit
)

# Sizes
cursor_radius = mm2pixel * 2
target_radius = mm2pixel * 4
start_circle_radius = mm2pixel * 3

# Create objects
true_cursor = visual.Circle(
    win,
    fillColor='red',
    lineColor='red',
    units=unit,
    size=(cursor_radius * 2, cursor_radius * 2)
)

rotated_cursor = visual.Circle(
    win,
    fillColor='white',
    lineColor='white',
    units=unit,
    size=(cursor_radius * 2, cursor_radius * 2)
)

target = visual.Circle(
    win,
    fillColor='yellow',
    lineColor='yellow',
    units=unit,
    size=(target_radius * 2, target_radius * 2),
    pos=(0, mm2pixel * 60)
)

start_circle = visual.Circle(
    win,
    fillColor='black',
    lineColor='white',
    units=unit,
    size=(start_circle_radius * 2, start_circle_radius * 2),
    pos=(0, 0)
)

# Create a mouse object
mouse = event.Mouse(visible=False, win=win)
prev_pos = mouse.getPos()

game_phase = 0
timer = None
reset_flag = False
rot = [45]  # Possible rotation angles (in degrees)
hand_rot_data = [] # mouse pos xy, cursor pos xy

# Variables for phase-based rotation
last_phase = None       # To detect phase changes
current_theta = None    # To store the current rotation (in radians)

CURSOR_X_TOTAL_TRAJ = []
CURSOR_Y_TOTAL_TRAJ = []
MOUSE_X_TOTAL_TRAJ = []
MOUSE_Y_TOTAL_TRAJ = []
TRIALS = []
ROTS = []

# Trial counter
trial = 0
n_baseline = 5
n_exposure = 5
exposore_trials = [n_baseline, n_baseline + n_exposure]

# Main loop: update cursors until Escape is pressed
while True:

    # Update the cursor position with the current mouse position
    true_cursor.pos = mouse.getPos()
    mouse_pos = mouse.getPos()
    
    # Check if the game phase has changed; if so, select a new rotation
    if game_phase != last_phase:
        current_theta = np.radians(ts["rotation"][trial])
        last_phase = game_phase

    # Compute rotated cursor position using the current rotation angle
    rotated_x = mouse_pos[0] * np.cos(current_theta) - mouse_pos[1] * np.sin(current_theta)
    rotated_y = mouse_pos[0] * np.sin(current_theta) + mouse_pos[1] * np.cos(current_theta)
    rotated_cursor.pos = (rotated_x, rotated_y)
  
    
    # Draw objects
    start_circle.draw()
    true_cursor.draw()
    rotated_cursor.draw()
    
    # Optionally hide the true_cursor
    true_cursor.opacity = 0

    # Calculate the distance between the true_cursor and start_circle
    curs_to_start = math.sqrt(
        (rotated_cursor.pos[0] - start_circle.pos[0])**2 + (rotated_cursor.pos[1] - start_circle.pos[1])**2
    )


    # Game Phase 0: START CIRCLE CHECK
    if game_phase == 0:

        if trial == ts['trial'].max() - 1: # Fix for final trial
            break

        # Total trajectory
        CURSOR_X_TRAJ = []
        CURSOR_Y_TRAJ = []
        MOUSE_X_TRAJ = []
        MOUSE_Y_TRAJ = []
        rot_vals = []
        trial_num = []

        start_circle.opacity = 1
        target.opacity = 1

        if curs_to_start <= start_circle_radius:
            if timer is None:  # Start the timer only once
                timer = core.Clock()
            elif timer.getTime() >= 1:  # If 1 second has passed
                timer = None
                game_phase = 1  # Move to next phase

    # Game Phase 1: MOVE
    if game_phase == 1:
        target.draw()
        rotated_cursor.draw()
        # true_cursor.draw()
        start_circle.opacity = 0

        current_pos = mouse.getPos() 
        CURSOR_X, CURSOR_Y = rotated_cursor.pos
        MOUSE_X, MOUSE_Y = true_cursor.pos

        rot_vals.append(current_theta)
        trial_num.append(trial)
        
        CURSOR_X_TRAJ.append(CURSOR_X)
        CURSOR_Y_TRAJ.append(CURSOR_Y)
        MOUSE_X_TRAJ.append(MOUSE_X)
        MOUSE_Y_TRAJ.append(MOUSE_Y)

        if np.array_equal(current_pos, prev_pos) and (curs_to_start >= (target.pos[1]/2)):
            if timer is None:
                timer = core.Clock()
            elif timer.getTime() >= 1:
                target.opacity = 0
                start_circle.opacity = 1
                timer = None
                game_phase = 2
                
            
        prev_pos = current_pos
        
    # Game Phase 2: DATA?
    if game_phase == 2:
        
        if not reset_flag:
            trial += 1
            
            CURSOR_X_TOTAL_TRAJ.extend(CURSOR_X_TRAJ)
            CURSOR_Y_TOTAL_TRAJ.extend(CURSOR_Y_TRAJ)
            MOUSE_X_TOTAL_TRAJ.extend(MOUSE_X_TRAJ)
            MOUSE_Y_TOTAL_TRAJ.extend(MOUSE_Y_TRAJ)
            ROTS.extend(rot_vals)
            TRIALS.extend(trial_num)
            
            # print(prev_pos)
            reset_flag = True

        if curs_to_start <= start_circle_radius:
            reset_flag = False
            game_phase = 0  # Move to next phase

    keys = event.getKeys()
    if 'escape' in keys:
        break  

    # Update the display
    win.flip()
    
    
win.close()


# Save Data
df["Trial"] = TRIALS
df["Rotation"] = ROTS
df["Mouse X"] = MOUSE_X_TOTAL_TRAJ
df["Mouse Y"] = MOUSE_Y_TOTAL_TRAJ
df["Cursor X"] = CURSOR_X_TOTAL_TRAJ
df["Cursor Y"] = CURSOR_Y_TOTAL_TRAJ


# Save to CSV
df.to_csv("data.csv", index=False)


