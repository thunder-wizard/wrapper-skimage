import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import sys
import json
from matplotlib.widgets import Button

if len(sys.argv) != 3:
    print("Usage: python script_name.py <image_path1> <image_path2>")
    sys.exit(1)

image_path1 = sys.argv[1]
image_path2 = sys.argv[2]

img1 = mpimg.imread(image_path1)
img2 = mpimg.imread(image_path2)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

ax1.imshow(img1)
ax1.set_title('Image 1 - Click to save coordinates')
ax1.axis('off')

ax2.imshow(img2)
ax2.set_title('Image 2 - Click to save coordinates')
ax2.axis('off')

# Initialize scatter plots, lists to hold coordinates, and a history stack
coords1 = []  
coords2 = []
history = []  # To track added points

# Function to handle mouse clicks
def on_click(event):
    if event.inaxes == ax1 and event.button == 1:
        coord = (event.xdata, event.ydata)
        if all(np.linalg.norm(np.array(coord) - np.array(existing)) > 20 for existing in coords1):
            print(f'Origin: {coord}')
            coords1.append(coord)  # Add to the list of coordinates
            history.append(('add', 'coords1', coord))  # Record action in history
            ax1.scatter(coord[0], coord[1], color='red', s=40, marker='x', edgecolors='white', linewidths=2)
            plt.draw()
        else:
            print('Point too close to existing points.')

    elif event.inaxes == ax2 and event.button == 1:
        coord = (event.xdata, event.ydata)
        if all(np.linalg.norm(np.array(coord) - np.array(existing)) > 10 for existing in coords2):
            print(f'Target: {coord}')
            coords2.append(coord)  # Add to the list of coordinates
            history.append(('add', 'coords2', coord))  # Record action in history
            ax2.scatter(coord[0], coord[1], color='blue', s=40, marker='x', edgecolors='white', linewidths=2)
            plt.draw()
        else:
            print('Point too close to existing points.')

# Function to save coordinates when closing the window
def on_close(event):
    data = {
        'coords1': coords1,
        'coords2': coords2
    }
    with open('coordinates.json', 'w') as f:
        json.dump(data, f)
    print("Coordinates saved to coordinates.json")

# Function to clear coordinates
def clear_coordinates(event):
    global coords1, coords2, history
    coords1 = []
    coords2 = []
    history = []  # Clear history
    reset_plot()
    print("Coordinates cleared.")

# Function to reset the plot
def reset_plot():
    ax1.cla()
    ax1.imshow(img1)
    ax1.set_title('Image 1 - Click to save coordinates')
    ax1.axis('off')

    ax2.cla()
    ax2.imshow(img2)
    ax2.set_title('Image 2 - Click to save coordinates')
    ax2.axis('off')

    plt.draw()

# Function to undo the last added point
def return_last_point(event):
    global coords1, coords2
    if history:
        action, coord_type, coord = history.pop()  # Get the last action
        if action == 'add':
            if coord_type == 'coords1':
                coords1.remove(coord)
                print(f'Removed Origin: {coord}')
            elif coord_type == 'coords2':
                coords2.remove(coord)
                print(f'Removed Target: {coord}')

        reset_plot()
        # Redraw remaining points
        for coord in coords1:
            ax1.scatter(coord[0], coord[1], color='red', s=40, marker='x', edgecolors='white', linewidths=2)
        for coord in coords2:
            ax2.scatter(coord[0], coord[1], color='blue', s=40, marker='x', edgecolors='white', linewidths=2)
        plt.draw()
    else:
        print("No points to remove.")

# Add buttons
ax_clear = plt.axes([0.1, 0.01, 0.2, 0.075])  # Clear button
btn_clear = Button(ax_clear, 'Clear Coordinates')
btn_clear.on_clicked(clear_coordinates)

ax_return = plt.axes([0.4, 0.01, 0.2, 0.075])  # Return button
btn_return = Button(ax_return, 'Return Last Point')
btn_return.on_clicked(return_last_point)

# Connect the click event to the handler
cid_click = fig.canvas.mpl_connect('button_press_event', on_click)
cid_close = fig.canvas.mpl_connect('close_event', on_close)

# Show the image
plt.show()
