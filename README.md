# esp32-smartmeter
A program for obtaining readings from an Iskra MT174 with a serial reading head from Volkszähler.

## Required Hardware
```
- ESP32
- Iskra MT174
- Serial reading head from Volkszähler
```
## Serial Reading Head from Volkszähler
Please note, the instructions are in German:
```
https://wiki.volkszaehler.org/hardware/controllers/ir-schreib-lesekopf
```

## Home Assistant Configuration

You will be required to create an access token for Home Assistant.
```
https://www.home-assistant.io/docs/authentication/
```

## Installation

Relying on Thony would be my preferred choice for programming the ESP32.
```
https://thonny.org/
```

## To-Do
```
- Incorporate a web server for data reading and configuration.
- Test the code on other power meters.
- Integrate a MQTT client.
```

## Debugging

If you encounter errors, try modifying the end-of-line definition in the code on lines 112/113:

```
if b'53.5*255' in line or b'1.8.4*15' in line:
    break
```
(Note: The IR-LED on my first reading head was faulty so it required a replacement.)

## License
[MIT](https://choosealicense.com/licenses/mit/)