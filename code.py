import tkinter as tk
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


# Create a Tkinter window
root = tk.Tk()
root.title("Matrix Transformation Application")
WIDTH = 800
HEIGHT = 800
RESOLUTION = 20
# Create a canvas for plotting vectors
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack(side=tk.LEFT)

# Create a label and entry for matrix input
matrix_label = tk.Label(root, text="Enter square matrix (e.g., 2x2, 3x3):")
matrix_label.pack()
default_matrix = tk.StringVar()
default_matrix.set('[[1, 2],[3, 4]]')
matrix_entry = tk.Entry(root, textvariable=default_matrix)
matrix_entry.pack()


# Function to apply matrix transformation to vectors
def apply_transformation():
    matrix_str = matrix_entry.get()
    try:
        matrix = np.array(eval(matrix_str))  # Convert the input string to a numpy array
        vectors = np.array([[x, y] for x in range(-RESOLUTION, RESOLUTION+1) for y in range(-RESOLUTION, RESOLUTION+1)])  # Generate vectors from -10 to 10
        vectors_centers = np.array([[WIDTH // 2 + x * WIDTH // RESOLUTION, HEIGHT // 2 + y * HEIGHT // RESOLUTION] for x in range(-RESOLUTION, RESOLUTION+1) for y in range(-RESOLUTION, RESOLUTION+1)])
        transformed_vectors = np.dot(vectors, matrix)  # Apply matrix transformation
        # norm = np.linalg.norm(transformed_vectors)
        # transformed_vectors = transformed_vectors / norm
        plot_vectors(transformed_vectors, vectors_centers, vectors)  # Plot the transformed vectors
        generate_initial_vectors()
    except Exception as e:
        print("Error:", e)


# Function to plot the vectors on the canvas
def plot_vectors(vectors, centers, vectors_init):
    canvas.delete("all")  # Clear the canvas
    max_norm = max(np.linalg.norm(vector) for vector in vectors)
    max_init_norm = max(np.linalg.norm(vector) for vector in vectors_init)
    max_scale = max_norm / max_init_norm

    for k, vector in enumerate(vectors):
        center_x, center_y = centers[k]
        if vectors_init[k][0] != 0 or vectors_init[k][1] != 0:
            norm_init = np.linalg.norm(vectors_init[k])
        else:
            norm_init = 1
        norm = np.linalg.norm(vector)
        if vector[0] != 0 or vector[1] != 0:
            vector = vector / norm
        else:
            vector = [0, 0]
        #print(vector)
        x, y = vector
        color_value = np.clip(int(255 * (norm / norm_init) / max_scale), 0, 255)
        color = "#{:02x}{:02x}{:02x}".format(color_value, 0, 255 - color_value)  # Gradient from blue to red
        canvas.create_line(center_x, center_y, center_x + x * RESOLUTION * 2, center_y - y * RESOLUTION * 2, arrow=tk.LAST, fill=color)


# Function to generate and plot the initial vectors
# Function to generate and plot the initial vectors, center, and axes
def generate_initial_vectors():
    # Draw x-axis
    canvas.create_line(0, HEIGHT // 2, WIDTH, HEIGHT // 2, fill="black", arrow=tk.LAST)
    # Draw y-axis
    canvas.create_line(WIDTH // 2, HEIGHT, WIDTH // 2, 0, fill="black", arrow=tk.LAST)
    # Draw center
    canvas.create_oval(WIDTH // 2 - 2, HEIGHT // 2 - 2, WIDTH // 2 + 2, HEIGHT // 2 + 2, outline="black")


# Create a button to apply the transformation
apply_button = tk.Button(root, text="Apply Transformation", command=apply_transformation)
apply_button.pack()

# Generate and plot the initial vectors
generate_initial_vectors()

# Run the Tkinter main loop
root.mainloop()



