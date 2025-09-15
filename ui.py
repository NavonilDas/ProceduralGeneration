import tkinter as tk
from PIL import Image, ImageTk
from grass_2d import create_2d_grass_tileset
# Create the main window
root = tk.Tk()
root.title("2D Grass Tile Generator - Dual Grid system")
root.geometry("500x500")  # width x height

# Add a label
label = tk.Label(root, text="Hello, Tkinter!", font=("Arial", 14))
label.pack(pady=20)


def grass_image():
    pil_img = Image.fromarray(create_2d_grass_tileset())
    return ImageTk.PhotoImage(pil_img)

canvas = tk.Canvas(root,width=128,height=128)
canvas.pack()
canvas.create_image(20,20, anchor="nw", image=grass_image())


# Add a button with an action
def on_click():
    new_img = create_2d_grass_tileset()
    image_viewer.config(image=new_img)
    # image_viewer.image

# button = tk.Button(root, text="Click Me", command=on_click)
# button.pack(pady=10)


# Start the event loop
root.mainloop()
