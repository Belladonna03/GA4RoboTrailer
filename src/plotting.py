import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, FancyArrow
from matplotlib.path import Path

# Definition of walls and obstacles
WALLS = [
    (0, 99, 100, 100),
    (0, 1, 1, 99),
    (0, 0, 100, 1),
    (99, 1, 100, 99)
]

OBSTACLES = [
    (56, 1, 62, 12),
    (1, 30, 22, 36),
    (22, 30, 28, 42),
    (28, 36, 40, 42),
    (64, 38, 70, 60),
    (70, 38, 99, 44),
    (36, 58, 42, 72),
    (30, 72, 46, 78),
    (72, 76, 80, 99)
]

def plot_obstacles():
    """Displays obstacles on the graph."""
    for (x_min, y_min, x_max, y_max) in OBSTACLES:
        plt.fill([x_min, x_min, x_max, x_max], [y_min, y_max, y_max, y_min], color='red', alpha=0.5)
    for (x_min, y_min, x_max, y_max) in WALLS:
        plt.fill([x_min, x_min, x_max, x_max], [y_min, y_max, y_max, y_min], color='black', alpha=0.7)

# Function to simulate the robot's trajectory based on wheel speeds
def calculate_trajectory(individual, START_X, START_Y, START_THETA, START_PHI):
    """Calculates the robot's trajectory based on the given sequence of wheel speeds.
    Returns an array with coordinates and orientation angles."""
    x, y, theta, phi = START_X, START_Y, START_THETA, START_PHI
    trajectory = np.zeros((len(individual), 4))  # Array to store coordinates and angles
    for i, (left_wheel, right_wheel) in enumerate(individual):
        u1 = (right_wheel + left_wheel) / 2
        u2 = (left_wheel - right_wheel)
        x_dot = np.cos(theta) * u1
        y_dot = np.sin(theta) * u1
        theta_dot = u2
        phi_dot = -np.sin(phi) * u1 + u2
        x += x_dot
        y += y_dot
        theta += theta_dot
        phi += phi_dot
        trajectory[i] = [x, y, theta, phi]
    return trajectory

def plot_trajectories(population, title, START_X, START_Y, START_THETA, START_PHI, GOAL_X, GOAL_Y):
    """Draws the trajectories of the population."""
    plt.figure(figsize=(10, 8))
    plot_obstacles()
    colors = plt.cm.rainbow(np.linspace(0, 1, len(population)))
    for individual, color in zip(population, colors):
        trajectory = calculate_trajectory(individual, START_X, START_Y, START_THETA, START_PHI)
        path_data = [(Path.MOVETO, (START_X, START_Y))]
        for x, y, theta, phi in trajectory:
            path_data.append((Path.LINETO, (x, y)))
        codes, verts = zip(*path_data)
        path = Path(verts, codes)
        patch = PathPatch(path, facecolor='none', lw=2, edgecolor=color)
        plt.gca().add_patch(patch)
    plt.plot(START_X, START_Y, "go", label="Start")
    plt.plot(GOAL_X, GOAL_Y, "ro", label="Goal")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True)
    plt.title(title)
    plt.show()

def plot_best_trajectory(best_individual, title, START_X, START_Y, START_THETA, START_PHI, GOAL_X, GOAL_Y):
    """Draws the combined trajectory of the best individual in the population."""
    plt.figure(figsize=(10, 8))
    plot_obstacles()
    ax = plt.gca()
    ax.set_aspect('equal')
    trajectory = calculate_trajectory(best_individual, START_X, START_Y, START_THETA, START_PHI)
    path_data = [(Path.MOVETO, (START_X, START_Y))]
    for step, (x, y, theta, phi) in enumerate(trajectory):
        path_data.append((Path.LINETO, (x, y)))
        if step % 30 == 0:  # Add robot and trailer at every 30th step
            draw_robot_and_trailer(x, y, theta, phi, ax)
    draw_robot_and_trailer(trajectory[-1, 0], trajectory[-1, 1], trajectory[-1, 2], trajectory[-1, 3], ax)
    codes, verts = zip(*path_data)
    path = Path(verts, codes)
    patch = PathPatch(path, facecolor='none', lw=2, edgecolor='blue', linestyle='--')
    ax.add_patch(patch)
    ax.plot(START_X, START_Y, "go", markersize=10, label="Start")
    ax.plot(GOAL_X, GOAL_Y, "ro", markersize=10, label="Goal")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend(loc='best')
    ax.grid(True)
    plt.title(title)
    plt.show()

def draw_robot_and_trailer(x, y, theta, phi, ax):
    """Draws the robot and trailer on the graph."""
    robot_height, robot_width = 3, 3
    trailer_height, trailer_width = 2, 2
    link_length = 0.75
    phi = np.arctan2(np.sin(phi), np.cos(phi))
    trailer_x = x - (robot_width / 2 + link_length + trailer_width / 2) * np.cos(theta + phi)
    trailer_y = y - (robot_width / 2 + link_length + trailer_width / 2) * np.sin(theta + phi)
    robot_corners = calculate_corners(x, y, theta, robot_width, robot_height)
    trailer_corners = calculate_corners(trailer_x, trailer_y, theta + phi, trailer_width, trailer_height)
    ax.add_patch(plt.Polygon(robot_corners, color='blue'))
    ax.add_patch(plt.Polygon(trailer_corners, color='yellow'))
    ax.plot([x, trailer_x], [y, trailer_y], 'k-')
    # Add arrow for the robot
    ax.add_patch(FancyArrow(x, y, np.cos(theta) * 2, np.sin(theta) * 2, color='green', width=0.3))
    # Add arrow for the trailer
    ax.add_patch(FancyArrow(trailer_x, trailer_y, np.cos(theta + phi) * 2, np.sin(theta + phi) * 2, color='red', width=0.3))

def calculate_corners(x, y, theta, width, height):
    """Calculates the coordinates of the rectangle corners at the given coordinates with rotation."""
    corners = []
    for corner in [(-width / 2, -height / 2), (-width / 2, height / 2),
                   (width / 2, height / 2), (width / 2, -height / 2)]:
        new_x = x + corner[0] * np.cos(theta) - corner[1] * np.sin(theta)
        new_y = y + corner[0] * np.sin(theta) + corner[1] * np.cos(theta)
        corners.append((new_x, new_y))
    return corners

