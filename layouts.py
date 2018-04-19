import degree_display
import linear_display
import graph_display
from sense_hat import SenseHat
import time

s = SenseHat()

# RGB values for various colours
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
pink = (255, 50, 50)
nothing = (0, 0, 0)
white = (255, 255, 255)
# Heat is set to red for testing purposes
heat = red


def layer_items(items):
    """
    The various different displays in items are "layered" on top of one another
    This is done by replacing the pixels of the display "below" with the pixels of the display "above"-
    whenever the character is not "o" (treated as transparent)
    """
    o = "o"
    img = [
            o, o, o, o, o, o, o, o,
            o, o, o, o, o, o, o, o,
            o, o, o, o, o, o, o, o,
            o, o, o, o, o, o, o, o,
            o, o, o, o, o, o, o, o,
            o, o, o, o, o, o, o, o,
            o, o, o, o, o, o, o, o,
            o, o, o, o, o, o, o, o,
        ]
    for item in items:
        for i in range(0, 64):
            if item[i] != "o":
                img[i] = item[i]
    return img


class MagnitudeCompassDisplay:
    def __init__(self):
        self.med_cpass = degree_display.DegreeDisplay("medium")
        self.left_bar = linear_display.LinearDisplay("left")
        self.mid_bar = linear_display.LinearDisplay("mid")
        self.right_bar = linear_display.LinearDisplay("right")

    def update_and_output(self, values):
        med_deg, mag_h = values
        med_c_display = self.med_cpass.output_display(med_deg)
        left_bar_display = self.left_bar.output_display(mag_h)
        mid_bar_display = self.mid_bar.output_display(mag_h)
        right_bar_display = self.right_bar.output_display(mag_h)
        return layer_items([med_c_display, left_bar_display, mid_bar_display, right_bar_display])


class LargeCompassDisplay:
    def __init__(self):
        self.large_cpass = degree_display.DegreeDisplay("large")

    def update_and_output(self, large_deg):
        large_c_display =  self.large_cpass.output_display(large_deg)
        return large_c_display


class MultiDisplay:
    def __init__(self):
        self.med_cpass = degree_display.DegreeDisplay("medium")
        self.left_bar = linear_display.LinearDisplay("left")
        self.mid_bar = linear_display.LinearDisplay("mid")
        self.right_bar = linear_display.LinearDisplay("right")

    def update_and_output(self, values):
        med_deg, left_h, mid_h, right_h = values
        med_c_display =  self.med_cpass.output_display(med_deg)
        left_bar_display = self.left_bar.output_display(left_h)
        mid_bar_display = self.mid_bar.output_display(mid_h)
        right_bar_display = self.right_bar.output_display(right_h)
        return layer_items([med_c_display, left_bar_display, mid_bar_display, right_bar_display])


class ProgressingGraphDisplay:
    def __init__(self):
        self.graph = graph_display.GraphDisplay()
        self.points = []

    def update_and_output(self, point):
        """
        The new point is added to the current list of points
        If the list already has 8 values, the last point is lost and will no longer be displayed
        This allows the graph to "progress" by a point by maintaining only the 7 previous values in the graph
        """
        if len(self.points) < 8:
            self.points.append(point)
        else:
            self.points.insert(0, point)
            del self.points[-1]

        filled_points = self.points
        missing_no = 8-len(filled_points)
        for i in range(0, missing_no):
            filled_points.append(0)
        graph_display = self.graph.output_display(filled_points)
        return graph_display


def test(display, data):
    """
    The display given is tested with the data given
    Shown by outputting the display to the console as string
    """
    pixels = display.update_and_output(data)
    for i in range(0, 65, 8):
                print(", ".join(pixels[i:i+8]))


def test_with_display(display, data):
    """
    Same as test but using the Sense HAT display
    """
    pixels = display_type.update_and_output(data)
    pixels = [nothing if x == "o"
               else red if x == "l" else yellow if x == "m" else green if x == "r"
               else heat if x == "b" else white if x == "p"
               else pink if x == "d"
               else nothing for x in pixels]
    s.set_pixels(pixels)

if __name__ == "__main__":
    # Displays can be tested here using the modules of test and test_with_display
    display_type = ProgressingGraphDisplay()
    input_data = [270, 8, 5, 3]
    for i in [1, 2, 3, 5, 6, 7, 8, 8, 6, 5, 3, 2, 1]:
        test_with_display(display_type, [i])
        time.sleep(0.5)
