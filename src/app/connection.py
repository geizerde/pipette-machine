import serial
import serial.tools.list_ports

# ports = serial.tools.list_ports.comports()
#
# for port in ports:
#     print(port.device)

def establish_connection():
    try:
        # Find and open the COM port
        ports = serial.tools.list_ports.comports()
        port = next((p.device for p in ports), None)
        if port is None:
            raise ValueError("No COM port found.")

        ser = serial.Serial(port, baudrate=9600)
        return ser

    except ValueError as ve:
        print("Error:", str(ve))
        return ve

    except serial.SerialException as se:
        print("Serial port error:", str(se))
        return se

    except Exception as e:
        print("An error occurred:", str(e))
        return e

def setup_coords(ser: serial.Serial):
    ser.write("G92 X.. Y.. Z.. E..")
