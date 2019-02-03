'use strict';

const SerialPort = require('serialport')
const Readline = require('@serialport/parser-readline')
const port = new SerialPort('/dev/ttyACM0', { baudRate: 115200 })

port.on('error', function(err){
	console.log(err);
})

const parser = new Readline()
port.pipe(parser)

parser.on('data', line => {
	//console.log(`> ${line}`)
	if ('^' == line.charAt(0)) button_press(line)
})


function button_press(line) {
	//console.log( line.match(/^\^ (\d) (\d)/) )
	let [s, x, y, o] = line.match(/^\^ (\d) (\d)/)
	console.log(`Button press (${x}, ${y})`)
}



port.write("\r")
port.write("v\r")

//const ON = Buffer.from([0x21, 0x00, 0xaa, 0x00, 0xaa, 0x0d])
//const OFF = Buffer.from([0x21, 0x00, 0x00, 0x00, 0x00, 0x0d])

const ON = "@11aa00aa\r"
const OFF = "@11000000\r"

var on = false;
function toggle() {
	if (on) {
		console.log("Sending OFF: ", OFF)
		port.write(OFF)
	} else {
		console.log("Sending ON: ", ON)
		port.write(ON)		
	}
	//port.write((on) ? OFF : ON)
	on = !on;
}
//setInterval(toggle, 1000)


function wheel(pos, brightness=0.2) {
	if (pos < 0 || pos > 255)
        return [0, 0, 0]
    if (pos < 85)
        return [Math.trunc((255 - pos * 3)*brightness), Math.trunc(pos * 3 * brightness), 0]
    if (pos < 170) {
        pos -= 85
        return [0, Math.trunc((255 - pos * 3)*brightness), Math.trunc(pos * 3 * brightness)]
    }
    pos -= 170
    return [Math.trunc(pos * 3 * brightness), 0, Math.trunc((255 - (pos * 3)) * brightness)]
}


var pos = 0;

async function run() {
	while (true) {
		for (var x = 0; x < 8; x++) {
			for (var y = 0; y < 4; y++) {
				var cmd = `@${x}${y}${rgbToHex(...wheel(pos * 256 / 32))}\r`
				//console.log("            sending: ", cmd)
				port.write(cmd)
				await sleep(20);
				
			}
			pos = (pos < 31) ? pos + 1 : 0
		}
		//pos = (pos < 31) ? pos + 1 : 0
	}
}


function rgbToHex(r, g, b) {
    return ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

run();
