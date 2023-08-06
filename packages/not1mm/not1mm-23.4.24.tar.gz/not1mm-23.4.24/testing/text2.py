"""
doc string
"""
import sounddevice as sd

devices = sd.query_devices()

print(f"There are {len(devices)} devices.")

print("Output devices:")
for device in devices:
    # if device.get("max_output_channels"):
    print(
        f"Index: {str(device.get('index')).rjust(2)} "
        f"Name: {device.get('name').ljust(30)} "
        f"{device.get('default_samplerate')}"
    )
