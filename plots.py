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
plt.xlim([-200, 200])
plt.legend()
plt.show()