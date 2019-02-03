#
# Provides an interface for remotely controlling LIFX bulbs and
# Elektricy Wifi Outlets.  Interfaces with 
#
import adafruit_trellism4
import supervisor
 
trellis = adafruit_trellism4.TrellisM4Express()

#Don't use brightness, implementation slows down performance
#trellis.pixels.brightness = 0.2

def log(*args):
    print("# ", *args)

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

minimum = (3,3,3)
on_value = (60,60,60)
off_value = minimum

# Start with all-black
trellis.pixels.fill((0, 0, 0))

# Start with example state
lifx_state = [ (60,10,30), (60,60,60), None, (50,0,20) ]
outl_state = [0,0,1,1]

COLOR_WHEEL = [ (0,0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1)]

def init():
    for x, v in enumerate(lifx_state):
        adjusted_value = led_adjust(v)
        log("Set", (x+4,0), "=", adjusted_value)
        trellis.pixels[x+4, 0] = adjusted_value
    for x, v in enumerate(outl_state):
        log("Set", (x+4,1), "=", on_value if v == 1 else off_value )
        trellis.pixels[(x+4,1)] = on_value if v == 1 else off_value
    color_wheel_on()


def led_adjust(rgb):
    if rgb is None:
        return minimum
    else:
        return rgb

init()


led_on = []
 
for x in range(trellis.pixels.width):
    led_on.append([])
    for y in range(trellis.pixels.height):
        led_on[x].append(False)
 
#trellis.pixels.fill((0, 0, 0))
 
current_press = set()

# def process_button_presses():
#     pressed = set(trellis.pressed_keys)
 
#     for press in pressed - current_press:
#         x, y = press
 
#         if not led_on[x][y]:
#             log("Turning on:", press)
#             pixel_index = ((x + (y * 8)) * 256 // 32)
#             trellis.pixels[x, y] = wheel(pixel_index & 255)
#             led_on[x][y] = True
 
#         else:
#             log("Turning off:", press)
#             trellis.pixels[x, y] = (0, 0, 0)
#             led_on[x][y] = False
 
#     current_press = pressed


# def process_serial_input():
#     if supervisor.runtime.serial_connected:
#         command = input()
#         try:
#             print("You said:",command)
#             continue
#         except:
#             print("Error!")
#             pass


while True:
    pressed = set(trellis.pressed_keys)
 
    for press in pressed - current_press:
        x, y = press
 
        if not led_on[x][y]:
            log("Turning on:", press)
            pixel_index = ((x + (y * 8)) * 256 // 32)
            trellis.pixels[x, y] = wheel(pixel_index & 255)
            led_on[x][y] = True
 
        else:
            log("Turning off:", press)
            trellis.pixels[x, y] = (0, 0, 0)
            led_on[x][y] = False
 
    current_press = pressed


# def wheel(pos, brightness=1.0):
#     if pos < 0 or pos > 255:
#         return 0, 0, 0
#     if pos < 85:
#         return int(255 - pos * 3), int(pos * 3), 0
#     if pos < 170:
#         pos -= 85
#         return 0, int(255 - pos * 3), int(pos * 3)
#     pos -= 170
#     return int(pos * 3), 0, int(255 - (pos * 3))

# Reading from serial port:
