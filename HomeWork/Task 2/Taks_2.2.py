    # We use time to dellay the drawing
import time
    # This is a basic contructor.
class DrawingConstructor:
    def __init__(self, drawing):
        self.drawing = drawing
    
    # This is where we aqcualy draw the thing
    def draw_drawing(self, flipped=False):
        if flipped:
            drawing = self.drawing[::-1]
        else:
            drawing = self.drawing
        
        #   And this is where we go trough the Array
        max_length = max(len(line) for line in drawing)
        for line in drawing:
            centered_line = line.center(max_length)
            for char in centered_line:
                print(char, end='')
                if char != ' ':
                    time.sleep(0.05)  # This OUNLY will dellay if its *
            print()

# Here are our Objects Mid/ Starter/ And the basic drawing
mid_object = [
    "  *** *  ********  * ***"
]

starter_object = [
    "             *         ",
    "             *         ",
    "             *         ",
    "       *******   "
]

drawing = [
    "      *        *      ",
    "     *  ********  *     ",
    "    *  **********  *    ",
    "  *  ****    ****  *  ",
    "  *  ****    ****  *  ",
    "     *  **********  *     "
]

# Create DrawingConstructor objects
constructor = DrawingConstructor(starter_object)

# Draw the Starter object
constructor.draw_drawing()

# Draw the drawing
constructor = DrawingConstructor(drawing)
constructor.draw_drawing()

# Draw the mid_object
constructor = DrawingConstructor(mid_object)
constructor.draw_drawing()

# Draw the flipped drawing
constructor = DrawingConstructor(drawing)
constructor.draw_drawing(flipped=True)

# Draw the flipped Starter object
constructor = DrawingConstructor(starter_object)
constructor.draw_drawing(flipped=True)
