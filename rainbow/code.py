#
# Experiment with fast pixel drawing, rainbows, and the accelerometer
#
import adafruit_trellism4
import adafruit_adxl34x
import busio
import board

trellis = adafruit_trellism4.TrellisM4Express()
trellis.pixels.auto_write = False
trellis.pixels.brightness = 0.2

i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

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
    for x, v in enumerate(COLOR_WHEEL):
        pos = (x * 256 // 8)
        color = wheel(pos & 255)
        trellis.pixels[v] = color


offset = 0
length = 32

def draw():
    for x in range(trellis.pixels.width):
        for y in range(trellis.pixels.height):
            trellis.pixels[x,y] = wheel(((x+offset) * 256 // length) & 255)


while True:
    draw()
    offset = (offset + 1) % length
    trellis.pixels.show()
    (y, x, z) = accelerometer.acceleration
    if x > 2 and length < 128:
        length += 1
    elif x < -2 and length > 4:
        length -= 1
    #print(length, x)


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
