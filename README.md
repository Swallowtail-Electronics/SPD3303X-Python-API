# SPD3303X/X-E Python Interface

Siglent’s SPD3000X Series Programmable Linear DC Power Supply has a 4.3 inch TFT-LCD display, supports Remote Programming and has a Real Time Wave Display. The ‘3000X family has three isolated outputs; two adjustable channels and one selectable channel from 2.5 V, 3.3 V, and 5 V. It also has output short and overload protection and can be used in production and development. This power supply can be controlled over LAN by sending SCPI commands and this helpful pythiong wrapper makes that a very simple process. All you need the IP address of your power supply and you can get connected to your supply remotely.

## Installation
Place the `SPD3303X.py` and `SCPI.py` files in the same directory as your main project to referance the associated objects.

TODO: make this package accessable though pip

## Usage
Example usage is included in the `main.py` file.

```py
from SPD3303X import SPD3303X
import time

def main():
    """
    Program logic main implementation
    """
    ps = SPD3303X('192.168.1.20')

    print(f"Made by {ps.manufacturer}\nModel Number: {ps.product_type}\nSeries Number: {ps.series_number}\nSoftware Version: {ps.software_version}\nHardware Version: {ps.hardware_version}")

    # Set the voltage to 3.3V and max current to 500mA
    ps.set_current(1, 0.5)
    ps.set_voltage(1, 3.3)
    ps.turn_on_waveform_display(1)
    ps.output_on(1)
    time.sleep(2)
    channel1_current = ps.get_current(1)
    channel1_voltage = ps.get_voltage(1)
    channel1_power = ps.get_power(1)
    print(f"Channel 1: Voltage - {channel1_voltage}V, Current - {channel1_current}A, Power - {channel1_power}W")
    time.sleep(1)
    ps.output_off(1)
    ps.turn_off_waveform_display(1)
    ps.close()

if __name__ == '__main__':
    main()
```