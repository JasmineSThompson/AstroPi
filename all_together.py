import layouts
from sense_hat import SenseHat
import time
import datetime
import csv

"""
The max and min values for each: x, y, z, magnitude
(found by analysing 3 week long CSVs)
-73.776049 --- 33.134748
-43.81003 --- 42.090793
-47.192799 --- 49.038967
1.7274182976630181 --- 76.2744085380704
"""

s = SenseHat()

# RGB values for various colours
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
pink = (255, 50, 50)
nothing = (0, 0, 0)
white = (255, 255, 255)


def separate(start, end, divisor):
    """
    Returns a list of values exactly going from start to end
    with exactly x number of "jumps" of equal size; x being "divisor"
    E.g. 0-99 divided into 4 returns [0, 24, 49, 74, 99]
    """
    i = start
    separated_range = [start]
    span = end - start; part = span / divisor
    while i < end:
        i += part
        separated_range.append(i)
    return separated_range


def create_heat_range():
    """
    Creates a list of 256 RGB values going from blue to purple to red
    """
    blue_values = [i for i in range(255, -1, -1)]
    red_values = [i for i in range(0, 256)]
    all_rgb = []
    for i in range(0, 256):
        all_rgb.append((red_values[i], 0, blue_values[i]))
    return all_rgb


def simplify(value, data):
    """
    This returns the number of the gap in the separated range
    E.g. Goes from gap 1 to gap 4 in [0, 24, 49, 74, 99]
    """
    for i in range(0, len(data) - 1): # number of "gaps" in the list
        if data[i] < value < data[i+1]: # if between the two being analysed
            return i + 1 # return the "gap number"
        elif value < data[0]: # if outside range and smaller, return 1
            return 1
        elif value > data[-1]:
            return len(data) - 1 # if outside range and bigger, return largest value


def main():
    # The number of seconds which the detection will run for (may overrun this by around 0.5s)
    seconds_to_run = 60
    display_direction = "up"
    row_id = 0

    # Objects created for the various displays
    large_compass_d = layouts.LargeCompassDisplay()
    magnitude_compass_d = layouts.MagnitudeCompassDisplay()
    multi_d = layouts.MultiDisplay()
    progressing_graph_d = layouts.ProgressingGraphDisplay()

    # The ranges made by the highest and lowest value of each sensor are separated ready for the display
    x_list = separate(-70, 30, 8)
    y_list = separate(-40, 40, 8)
    z_list = separate(-50, 50, 8)
    mag_list = separate(0, 80, 8)
    mag_list_rgb = separate(0, 80, 256)
    # The heat range for the display is also formed
    heat_range = create_heat_range()

    # File opened to store the CSV and an object created for writing to it
    writefile = open("magnetic_strength_sensor.csv", "w")
    datawriter = csv.writer(writefile, delimiter=",")
    # Headings for each column are written to the file
    datawriter.writerow(["ROW_ID", "deg_north", "mag_x", "mag_y", "mag_z", "pitch", "roll", "yaw", "timestamp"])

    # Loop continues until time has passed seconds_to_run
    start_time = time.time()
    while time.time() - start_time <= seconds_to_run:
        # The relevant sensory data is retrieved from the Sense HAT and stored in variables
        deg_north = s.get_compass()
        # print("Degrees North:", deg_north)
        raw_compass = s.get_compass_raw()
        x_mag = raw_compass["x"]
        y_mag = raw_compass["y"]
        z_mag = raw_compass["z"]
        #  print("x:", x_mag, "y:", y_mag, "z:", z_mag)
        orientation = s.get_orientation_radians()
        pitch = orientation["pitch"]
        roll = orientation["roll"]
        yaw = orientation["yaw"]
        # Value for magnetic field magnitude calculated using sensory information
        magnitude = (x_mag ** 2 + y_mag ** 2 + z_mag ** 2) ** 0.5
        # Timestamp created
        timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

        # Sensory information written to the CSV file
        datawriter.writerow([row_id, deg_north, x_mag, y_mag, z_mag, pitch, roll, yaw, timestamp])

        # For each of the values, their strength is "simplified" into an integer value in certain range
        # E.g. the value for the x-axis sensor might be simplified to a number from 1-8
        x_simp = simplify(x_mag, x_list)
        y_simp = simplify(y_mag, y_list)
        z_simp = simplify(z_mag, z_list)
        mag_simp = simplify(magnitude, mag_list)
        mag_simp_rgb = simplify(magnitude, mag_list_rgb)

        # The RGB colour denoting the magnitude is chosen using the simplified magnitude reading
        heat_colour = heat_range[mag_simp_rgb-1]

        # The last direction in which the joystick was pressed is found
        try:
            event = s.stick.get_events()[-1]
            display_direction = event.direction
        except IndexError:
            pass

        # According to that direction, a certain display is calculated using sensory information
        if display_direction == "up":
            output = large_compass_d.update_and_output(deg_north)
        elif display_direction == "right":
            output = magnitude_compass_d.update_and_output(deg_north, mag_simp)
        elif display_direction == "left":
            output = multi_d.update_and_output(deg_north, x_simp, y_simp, z_simp)
        elif display_direction == "down":
            output = progressing_graph_d.update_and_output(mag_simp)

        """for i in range(0, 65, 8):
                print(", ".join(output[i:i+8]))"""

        # The strings returned by the display are converted to the relevant RGB values
        output = [nothing if x == "o"
               else red if x == "l" else green if x == "m" else blue if x == "r"
               else heat_colour if x == "b" else white if x == "p"
               else white if x == "d"
               else nothing for x in output]

        # The final display is output
        s.set_pixels(output)

        row_id += 1
        time.sleep(1)

    # print(time.time() - start_time)
    # Once the time has passed, the file is closed (data saved) and the display is set to go dark
    writefile.close()
    s.clear()
        

if __name__ == "__main__":
    main()

