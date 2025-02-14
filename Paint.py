from tkinter import *  # Import everything from the tkinter library for creating a GUI
from tkinter.colorchooser import askcolor  # Import the color chooser dialog

class Paint(object):
    pen_size = 5.0  # Default pen size
    color = 'black'  # Default color

    def __init__(self):
        self.root = Tk()  # Create the main application window

        # Create buttons for different drawing tools
        self.pen_button = Button(self.root, text='A pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.brush_button = Button(self.root, text='Brush', command=self.use_brush)
        self.brush_button.grid(row=0, column=1)

        self.color_button = Button(self.root, text='Colour', command=self.choose_color)
        self.color_button.grid(row=0, column=2)

        self.eraser_button = Button(self.root, text='Eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=3)

        self.clear_button = Button(self.root, text='Clear', command=self.clear_canvas)
        self.clear_button.grid(row=0, column=4)

        # Create a slider to select the pen/brush size
        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL, label='Size')
        self.choose_size_button.grid(row=0, column=5)

        # Create a drawing canvas
        self.c = Canvas(self.root, bg='white', width=600, height=600)
        self.c.grid(row=1, columnspan=6)

        self.setup()  # Set up initial parameters
        self.root.mainloop()  # Start the main application loop

    def setup(self):
        self.old_x = None  # Stores the previous x-coordinate
        self.old_y = None  # Stores the previous y-coordinate
        self.line_width = self.choose_size_button.get()  # Get the current line width
        self.color = self.color  # Set the current color
        self.eraser_on = False  # Eraser mode is off by default
        self.active_button = self.pen_button  # Set the active button (default: pen)
        # Bind events to the canvas
        self.c.bind('<B1-Motion>', self.paint)  # Handle mouse movement while the left button is pressed
        self.c.bind('<ButtonRelease-1>', self.reset)  # Handle mouse button release

    def use_pen(self):
        self.activate_button(self.pen_button)  # Activate pen mode

    def use_brush(self):
        self.activate_button(self.brush_button)  # Activate brush mode

    def choose_color(self):
        self.eraser_on = False  # Disable eraser mode
        self.color = askcolor(color=self.color)[1]  # Open the color selection dialog

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)  # Activate eraser mode

    def clear_canvas(self):
        self.c.delete("all")  # Delete all elements on the canvas

    def activate_button(self, some_button, eraser_mode=False):
        # Configure active buttons
        self.active_button.config(relief=RAISED)  # Remove the pressed effect from the previous button
        some_button.config(relief=SUNKEN)  # Apply the pressed effect to the current button
        self.active_button = some_button  # Set the current active button
        self.eraser_on = eraser_mode  # Set eraser mode

    def paint(self, event):
        # Handles drawing on the canvas
        self.line_width = self.choose_size_button.get()  # Get the current line width
        paint_color = 'white' if self.eraser_on else self.color  # Set the color depending on the mode (eraser or normal)
        if self.old_x and self.old_y:  # Check if previous coordinates exist
            # Draw a line on the canvas
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=True, splinesteps=36)
        # Update previous coordinates
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        # Reset previous coordinates after releasing the mouse button
        self.old_x, self.old_y = None, None

# Run the application
if __name__ == '__main__':
    Paint()