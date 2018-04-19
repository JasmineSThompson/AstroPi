from sense_hat import SenseHat
import json

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


class DegreeDisplay:
    def __init__(self, size):
        self.size = size

    def retrieve_display(self, img_no):
        """
        The desired display is retrieved from the json file
        """
        filename = self.size + "_compass_pixels.json"
        with open(filename, "r") as f:
            pixels = json.load(f)
        img = pixels[img_no]
        return img

    def angle_to_oclock(self, deg):
        """
        Converts a 360 degree value into a value from 0-11
        (uses each of the different numbers on a clock face with corresponding clockwise angles from 12 o'clock)
        There is a different display for the small compass as it points in 8 directions, not 12
        """
        if self.size == "small":
            oclock = -1
            if 337.5 <= deg <= 360 or 0 <= deg < 22.5:
                oclock = 0
            elif 22.5 <= deg < 67.5:
                oclock = 1
            elif 67.5 <= deg < 112.5:
                oclock = 3
            elif 112.5 <= deg < 157.5:
                oclock = 4
            elif 157.5 <= deg < 202.5:
                oclock = 6
            elif 202.5 <= deg < 247.5:
                oclock = 7
            elif 247.5 <= deg < 292.5:
                oclock = 9
            elif 292.5 <= deg < 337.5:
                oclock = 10
            return oclock
        else:
            oclock = -1
            if 345 <= deg <= 360 or 0 <= deg < 15:
                oclock = 0
            elif 15 <= deg < 45:
                oclock = 1
            elif 45 <= deg < 75:
                oclock = 2
            elif 75 <= deg < 105:
                oclock = 3
            elif 105 <= deg < 135:
                oclock = 4
            elif 135 <= deg < 165:
                oclock = 5
            elif 165 <= deg < 195:
                oclock = 6
            elif 195 <= deg < 225:
                oclock = 7
            elif 225 <= deg < 255:
                oclock = 8
            elif 255 <= deg < 285:
                oclock = 9
            elif 285 <= deg < 315:
                oclock = 10
            elif 315 <= deg < 345:
                oclock = 11
            return oclock

    def output_display(self, deg_north):
        """
        Returns the relevant display for that compass size as a response to whatever degree input is given
        """
        deg_north = int(round(deg_north))
        img_no = self.angle_to_oclock(deg_north)
        display = self.retrieve_display(img_no)
        return display

    def test(self):
        """
        Outputs compass display as string in console as a response to a degree input
        """
        while True:
            deg_north = int(round(float(input("Degrees: "))))
            img_no = self.angle_to_oclock(deg_north)
            print("Image number:", img_no)
            display = self.retrieve_display(img_no)
            # Outputs grid display
            for i in range(0, 65, 8):
                print(", ".join(display[i:i+8]))
            # s.set_pixels(images[img_no](off, white, blue))

    def test_with_display(self):
        """
        Does the same as test, but with the Sense HAT display, not the console
        """
        while True:
            deg_north = int(round(float(input("Degrees: "))))
            img_no = self.angle_to_oclock(deg_north)
            print("Image number:", img_no)
            display = self.retrieve_display(img_no)
            display = [nothing if x == "o" else heat if x == "b" else white if x == "p" else nothing for x in display]
            s.set_pixels(display)

if __name__ == "__main__":
    # This allows the various sizes to be tested when the program is run
    print("Input a size of small, medium or large. All lowercase, no whitespace")
    size = input("Size: ")
    compass = DegreeDisplay(size)
    compass.test_with_display()
