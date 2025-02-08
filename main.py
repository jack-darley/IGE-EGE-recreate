from psychopy import visual, monitors, event, core
import math
import numpy as np
import matplotlib.pyplot as plt

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
    fillColor='white',
    lineColor='white',
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
rot = [20]  # Possible rotation angles (in degrees)
hand_rot_data = []

# Variables for phase-based rotation
last_phase = None       # To detect phase changes
current_theta = None    # To store the current rotation (in radians)

# Main loop: update cursors until Escape is pressed
while True:
    # Update the cursor position with the current mouse position
    true_cursor.pos = mouse.getPos()
    mouse_pos = mouse.getPos()
    
    # Check if the game phase has changed; if so, select a new rotation
    if game_phase != last_phase:
        current_theta = np.radians(-np.random.choice(rot))
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

        cursor_trajectory = []
        actual_trajectory = []

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
        cursor_trajectory.append(rotated_cursor.pos)
        actual_trajectory.append(true_cursor.pos)

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
            
            print(prev_pos)
            reset_flag = True

        if curs_to_start <= start_circle_radius:
            hand_rot_data.append((list(actual_trajectory), list(cursor_trajectory)))
            game_phase = 0  # Move to next phase

    keys = event.getKeys()
    if 'escape' in keys:
        break  

    # Update the display
    win.flip()
    

win.close()

# Test trajectory code

# x_vals_cursor, y_vals_cursor = zip(*cursor_trajectory) 
# x_vals_actual, y_vals_actual = zip(*actual_trajectory) 

# plt.scatter(target.pos[0], target.pos[1], s=500, color='yellow')
# plt.plot(x_vals_cursor, y_vals_cursor, color='w', lw=4, label="Rotated Cursor")
# plt.plot(x_vals_actual, y_vals_actual, color='g', lw=4, label="Veridical Trajectory")
# plt.gca().set_facecolor("black")

# plt.xlim([-100, 100])
# plt.ylim([min(y_vals_cursor)-20, max(y_vals_cursor)+20])
# plt.legend()
# plt.show()

print("Total trials stored:", len(hand_rot_data))
for i, (actual_traj, rotated_traj) in enumerate(hand_rot_data):
    print(f"Trial {i}: {len(actual_traj)} actual points, {len(rotated_traj)} rotated points")

plt.figure(figsize=(8, 6))  # Set figure size

for i, (actual_traj, rotated_traj) in enumerate(hand_rot_data):
    if not actual_traj or not rotated_traj:
        continue  # Skip empty trials

    print(f"Plotting Trial {i}: {len(actual_traj)} points")  # Debug print

    # Extract X, Y for actual & rotated paths
    x_vals_actual, y_vals_actual = zip(*actual_traj)  
    x_vals_cursor, y_vals_cursor = zip(*rotated_traj)  

    plt.plot(x_vals_actual, y_vals_actual, color='g', lw=2, alpha=0.6,
             label="Veridical Trajectory" if i == 0 else "")
    plt.plot(x_vals_cursor, y_vals_cursor, color='w', lw=2, alpha=0.6,
             label="Rotated Cursor" if i == 0 else "")


all_y_vals = [y for trial in hand_rot_data for _, y in trial[0]]  # Flatten all Y values
if all_y_vals:
    plt.ylim([min(all_y_vals) - 20, max(all_y_vals) + 20])

plt.scatter(target.pos[0], target.pos[1], s=500, color='yellow')

# Set Background and Labels
plt.gca().set_facecolor("black")
plt.xlim([-100, 100])
plt.legend()
plt.show()

