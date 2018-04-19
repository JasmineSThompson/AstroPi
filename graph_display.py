from sense_hat import SenseHat

s = SenseHat()

# RGB values for various colours
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
pink = (255, 50, 50)
nothing = (0, 0, 0)
white = (255, 255, 255)


class GraphDisplay:
    def __init__(self):
        self.char = "d"

    def output_display(self, values):
        """
        For each value in the list of values given, a point is plotted on the graph
        (the string at that location is changed to self.char)
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
        for x in range(0, 8):
            for y in range(0, 8):
                if values[x] == 8-y:
                    img[8*y+x] = self.char
        return img
    
    def test(self):
        """
        Using the list of values input in the console, the program calculates and outputs the relevant graph display
        """
        while True:
            print("These values should be integers 0-8")
            raw_values = input("List of values: ")
            # values split into strings and turned to integers
            values = raw_values.split(", ")
            values = [int(value) for value in values]
            print(values)
            # the list is padded out using 0's until the number of values reaches 8
            if len(values) > 8:
                values = values[0:8]
            elif len(values) < 8:
                missing_no = 8-len(values)
                for i in range(0, missing_no):
                    values.append(0)
            display = self.output_display(values)
            # Outputs grid display
            for i in range(0, 65, 8):
                print(", ".join(display[i:i+8]))

    def test_with_display(self):
        """
        Same as test, but using the Sense HAT display
        """
        while True:
            print("These values should be integers 0-8")
            raw_values = input("List of values: ")
            values = raw_values.split(", ")
            print(values)
            values = [int(value) for value in values]
            print(values)
            if len(values) > 8:
                values = values[0:8]
            elif len(values) < 8:
                missing_no = 8-len(values)
                for i in range(0, missing_no):
                    values.append(0)
            display = self.output_display(values)
            display = [nothing if x == "o" else pink if x == "d" else nothing for x in display]
            s.set_pixels(display)

if __name__ == "__main__":
    # If run, the graph display can be tested
    graph = GraphDisplay()
    graph.test_with_display()
