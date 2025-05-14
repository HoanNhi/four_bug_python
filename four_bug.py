import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
import tkinter as tk
from tkinter import messagebox

# --- GUI to Input Initial Positions ---
class BugInputUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Enter Initial Positions for 4 Bugs")

        self.entries = []

        for i in range(4):
            tk.Label(master, text=f"Bug {i + 1} (x y):").grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(master, width=20)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entry.insert(0, "0.0 0.0")  # default value
            self.entries.append(entry)

        submit_btn = tk.Button(master, text="Run Simulation", command=self.submit)
        submit_btn.grid(row=5, columnspan=2, pady=10)

        self.positions = None

    def submit(self):
        try:
            self.positions = []
            for entry in self.entries:
                x_str, y_str = entry.get().split()
                x, y = float(x_str), float(y_str)
                self.positions.append((x, y))
            self.master.destroy()
        except Exception:
            messagebox.showerror("Input Error", "Please enter valid coordinates in the format: x y (e.g., 10.0 15.0)")

# Launch the GUI
root = tk.Tk()
app = BugInputUI(root)
root.mainloop()

# After GUI is closed
if app.positions is None:
    exit()  # No valid positions entered

initial_positions = app.positions

# --- Simulation Settings ---
num_bugs = 4
dt = 0.05
v = 1.0
steps = 1000

positions = np.zeros((steps, num_bugs, 2))
positions[0] = np.array(initial_positions)

def unit_vector(p_from, p_to):
    direction = (p_to - p_from)
    distance = np.linalg.norm(direction)
    if distance == 0:
        return np.zeros_like(direction)
    return direction / distance

for i in range(1, steps):
    for j in range(num_bugs):
        curr = positions[i - 1, j]
        next_bug = positions[i - 1, (j + 1) % num_bugs]
        direction = unit_vector(curr, next_bug)
        positions[i, j] = curr + v * dt * direction

# --- Plot Setup ---
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(bottom=0.2)  # Leave space at bottom for slider

all_coords = np.array(initial_positions)
margin = 5
min_x, max_x = all_coords[:, 0].min() - margin, all_coords[:, 0].max() + margin
min_y, max_y = all_coords[:, 1].min() - margin, all_coords[:, 1].max() + margin
ax.set_xlim(min_x, max_x)
ax.set_ylim(min_y, max_y)

ax.set_aspect('equal')
ax.grid(True)
colors = ['r', 'g', 'b', 'm']

# Bug points
bugs = [ax.plot([], [], marker + 'o')[0] for marker in colors]
# Trajectories
lines = [ax.plot([], [], color=marker, linestyle='--')[0] for marker in colors]

# Slider Axes
slider_ax = plt.axes([0.2, 0.05, 0.6, 0.03])
step_slider = Slider(slider_ax, 'Step', 0, steps - 1, valinit=0, valstep=1)

# Update function for slider
def update_slider(val):
    frame = int(val)
    for j in range(num_bugs):
        x, y = positions[frame, j, 0], positions[frame, j, 1]
        bugs[j].set_data(x, y)

        path = positions[:frame+1, j, :]
        lines[j].set_data(path[:, 0], path[:, 1])

    fig.canvas.draw_idle()

step_slider.on_changed(update_slider)

# Initialize with frame 0
update_slider(0)
plt.title("4-Bug Problem with Trajectories and Manual Slider")
plt.show()