import layouts
from sense_hat import SenseHat
import time
import csv

""" The max and min values for each: x, y, z, magnitude
-73.776049 --- 33.134748
-43.81003 --- 42.090793
-47.192799 --- 49.038967
1.7274182976630181 --- 76.2744085380704
"""

def separate(s, e, d):
    i = s
    array = [s]
    span = e-s; part = span/d
    while i < e:
        i += part
        array.append(i)
    return array


def simplify(value, data):
    for i in range(0, len(data) - 1): # number of "gaps" in the list
        if value > data[i] and value < data[i+1]: # if between the two being analysed
            return i+1 # return the "gap number"
        elif value < data[0]: # if outside range and smaller, return 1
            return 1
        elif value > data[-1]:
            return len(data) - 1 # if outside range and bigger, return largest value

blue_values = [i for i in range(255, 128, -1)]
print(blue_values)
print(len(blue_values))

def main():
    s = SenseHat()
    display_no = 0
    counter = 1
    
    if display_no == 0:
        display = layouts.LargeCompassDisplay()
    elif display_no == 1:
        display = layouts.DualCompassDisplay()
    elif display_no == 2:
        display = layouts.MultiDisplay()
    elif display_no == 3:
        display = layouts.ProgressingGraphDisplay()

    x_list = separate(-70, 30, 8)
    y_list = separate(-40, 40, 100)
    z_list = separate(-50, 50, 100)
    mag_list = separate(0, 80, 100)

    writefile = open('magnetic_field_readings.csv', 'w', newline='')
    datawriter = csv.writer(writefile, delimiter=',')
    datawriter.writerow(["ROW_ID", "deg_north", "mag_x", "mag_y", "mag_z", "pitch", "roll", "yaw", "reset", "timestamp"]
        
    while True:
        deg_north = s.get_compass()
        raw_compass = s.get_compass_raw()
        x_mag = raw_compass["x"]
        y_mag = raw_compass["y"]
        z_mag = raw_compass["z"]
        orientation = s.get_orientation_radians()
        pitch = orientation["pitch"]
        roll = orientation["roll"]
        yaw = orientation["yaw"]
        reset = ""
        timestamp = ""

        datawriter.writerow([counter, deg_north, x_mag, y_mag, z_mag, pitch, roll, yaw, reset, timestamp])

        time.sleep(5)

        magnitude = (x_mag**2 + y_mag**2 + z_mag**2)**0.5

        x_simp = simplify(x_mag, x_list)
        y_simp = simplify(y_mag, y_list)
        z_simp = simplify(z_mag, z_list)
        mag_simp = simplify(magnitude, mag_list)
        
        if display_no == 0:
            output = display.update_and_output([deg_north])
        elif display_no == 1:
            output = display.update_and_output([deg_north, deg_north])
        elif display_no == 2:
            output = display.update_and_output([deg_north, x_simp, y_simp, z_simp])
        elif display_no == 3:
            output = display.update_and_output(mag_simp)

        counter += 1
        

if __name__ == "__main__":
    main()

