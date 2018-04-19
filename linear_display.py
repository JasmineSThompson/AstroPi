"""from sense_hat import SenseHat

s = SenseHat()"""

# RGB values for various colours
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
pink = (255, 50, 50)
nothing = (0, 0, 0)
white = (255, 255, 255)


class LinearDisplay:
    def __init__(self, pos):
        """
        According to the desired position, the x-position and character used for the bar changes
        """
        if pos == "mid":
            self.x= 6
            self.char = "m"
        elif pos == "right":
            self.x= 7
            self.char = "r"
        else:
            self.x = 5
            self.char = "l"

    def output_display(self, height):
        """
        A display for the bar is calculated using the height of the bar and returned
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
        for y in range(7, 7-height, -1):
            img[8*y + self.x] = self.char
        return img
    
    def test(self):
        """
        Using the height given, the program outputs the display of tha bar height as string in the console
        """
        while True:
            height = int(input("Height: "))
            display = self.output_display(height)
            # Outputs grid display
            for i in range(0, 65, 8):
                print(", ".join(display[i:i+8]))

    def test_with_display(self):
        """
        Same as test, but using the Sense HAT display
        """
        while True:
            height = int(input("Height: "))
            display = self.output_display(height)
            display = [nothing if x == "o" else red if x == "l"
                       else yellow if x == "m" else green if x == "r"
                       else nothing for x in display]
            s.set_pixels(display)

if __name__ == "__main__":
    # When opened the program tests a particular bar
    left = LinearDisplay("right")
    left.test()
