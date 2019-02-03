#
# Provides an interface for remotely controlling LIFX bulbs and
# Elektricy Wifi Outlets.  Interfaces with 
#
import adafruit_trellism4
import supervisor

trellis = adafruit_trellism4.TrellisM4Express()
trellis.pixels.auto_write = False

COLOR_WHEEL = [ (0,0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1)]

def log(*args):
    "Print all arguments to stdout"
    #print("# ", *args)

def wheel(pos, brightness=0.5):
    if pos < 0 or pos > 255:
        return 0, 0, 0
    if pos < 85:
        return int((255 - pos * 3)*brightness), int(pos * 3 * brightness), 0
    if pos < 170:
        pos -= 85
        return 0, int((255 - pos * 3)*brightness), int(pos * 3 * brightness)
    pos -= 170
    return int(pos * 3 * brightness), 0, int((255 - (pos * 3)) * brightness)

def color_wheel_on():
    log("Color wheel ON:")
    for x, v in enumerate(COLOR_WHEEL):
        pos = (x * 256 // 8)
        color = wheel(pos & 255, 0.5)
        log("Set", v, "=", color)
        trellis.pixels[v] = color

#color_wheel_on()

def send(*data):
    print("^",*data)

def process_serial_input():
    try:
        if supervisor.runtime.serial_bytes_available:
            command = input()
            log("Input:",command, "$")
            # Set an individual pixel to specified color
            if ("@" == command[0:1]):
                #Change individual pixel at given address
                x = int(command[1:2])
                y = int(command[2:3])
                r = int(command[3:5], 16)
                g = int(command[5:7], 16)
                b = int(command[7:9], 16)
                log("x:", x, "y:", y, "(r,g,b):", (r,g,b))
                if x < 8 and y < 4:
                    trellis.pixels[x,y] = (r,g,b)
                else:
                    trellis.pixels.fill((r,g,b))
                trellis.pixels.show()
            elif "!" == command[0:1]
                #Expect 32-pixel array
            elif "$" == command[0:1]
                #Arbitrary command, e.g. turn on accelorometer

    except:
        log("Error reading command")


current_press = set()

def process_button_press():
    global current_press
    try:
        pressed = set(trellis.pressed_keys)
     
        for press in pressed - current_press:
            x, y = press
            log("Pressed:", press)
            send(x,y)
     
        current_press = pressed
    except:
        log("Error reading button presses")
    

print("* Trellis serial interface online.")

while True:
    process_serial_input()
    process_button_press()

