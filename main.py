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