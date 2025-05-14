import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import tkinter as tk
from tkinter import messagebox

# --- Tkinter UI for Initial Positions of Bugs 1–3 ---
class BugInputUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Enter Initial Positions for Bugs 1–3")

        self.entries = []
        labels = ["Bug 1", "Bug 2", "Bug 3"]
        defaults = ["0.0 0.0", "0.0 20.0", "20.0 20.0"]

        for i in range(3):
            tk.Label(master, text=f"{labels[i]} (x y):").grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(master, width=20)
            entry.insert(0, defaults[i])
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries.append(entry)

        tk.Button(master, text="Run", command=self.submit).grid(row=4, columnspan=2, pady=10)
        self.positions = None

    def submit(self):
        try:
            self.positions = []
            for entry in self.entries:
                x_str, y_str = entry.get().split()
                x, y = float(x_str), float(y_str)
                self.positions.append((x, y))
            self.master.destroy()
        except:
            messagebox.showerror("Error", "Enter positions as: x y (e.g., 10.0 15.0)")

# Launch UI
root = tk.Tk()
ui = BugInputUI(root)
root.mainloop()

if ui.positions is None:
    exit()

# --- Parameters ---
s = 20
x0, y0 = 18.0, 2.0  # Bug 4 is fixed
v = [1.0, 1.0, 1.0, 0.0]
initial_positions = np.array(ui.positions + [(x0, y0)])

# --- Simulation ---
num_bugs = 4
steps = 1000
dt = 0.05
positions = np.zeros((steps, num_bugs, 2))
positions[0] = initial_positions

def unit_vector(p_from, p_to):
    direction = p_to - p_from
    dist = np.linalg.norm(direction)
    return direction / dist if dist != 0 else np.zeros_like(direction)

for i in range(1, steps):
    for j in range(num_bugs):
        curr = positions[i-1, j]
        target = positions[i-1, (j+1) % num_bugs]
        direction = unit_vector(curr, target)
        positions[i, j] = curr + v[j] * dt * direction

# --- Plot + Slider ---
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(bottom=0.2)

all_coords = initial_positions
margin = 5
ax.set_xlim(np.min(all_coords[:, 0]) - margin, np.max(all_coords[:, 0]) + margin)
ax.set_ylim(np.min(all_coords[:, 1]) - margin, np.max(all_coords[:, 1]) + margin)
ax.set_aspect('equal')
ax.grid(True)

colors = ['r', 'g', 'b', 'm']
dots = [ax.plot([], [], color + 'o')[0] for color in colors]
lines = [ax.plot([], [], color + '--')[0] for color in colors]

slider_ax = plt.axes([0.2, 0.05, 0.6, 0.03])
slider = Slider(slider_ax, 'Step', 0, steps - 1, valinit=0, valstep=1)

def update(frame):
    frame = int(frame)
    for j in range(num_bugs):
        x, y = positions[frame, j]
        dots[j].set_data(x, y)
        lines[j].set_data(positions[:frame+1, j, 0], positions[:frame+1, j, 1])
    fig.canvas.draw_idle()

slider.on_changed(update)
update(0)

plt.title("4-Bug Problem with Tkinter Input and Slider")
plt.show()
