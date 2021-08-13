# Simple Python script which fetches JSON data in the Circonus from the Aquasuite Web Service
# and stores it in a local file so it can be progressed by the FanControl tool by Remi Mercier

import requests
import os
import json
import time
import signal
import traceback

class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


if __name__ == "__main__":
    target_filename = os.environ["FAN_CONTROL_TARGET_SENSOR"]
    temperature_url = os.environ["TEMPERATURE_URL"]
    update_frequency = float(os.environ["UPDATE_FREQUENCY_SECONDS"])
    print(f"Synching sensor data from {temperature_url} to {target_filename}")
    print(f"Temperature update frequency: {update_frequency:0.1f}s")
    gc = GracefulKiller()
    while not gc.kill_now:
        try:
            data_value = 0.0
            # Fetch data from Aquasuite server
            try:
                response = requests.get(temperature_url, timeout=5)
                temp_data = json.loads(response.text)
                data_value = list(temp_data.values())[0]
            except:
                print(f"An error occurred while trying to fetch temperature update. {traceback.format_exc()}")
                temperature = "0.0"
            # Try to process data
            try:
                temperature: str = data_value
                float_temperature = float(temperature)  # cast to float. if this fails (None) we won't write it to disk
            except:
                print(f"An error occurred while trying to fetch temperature update. {traceback.format_exc()}")
                temperature = "20.0"
            # Store value in fan control file
            with open(f"/fancontrol/{target_filename}", "w") as temperature_file:
                print(f"Received water temperature update: {temperature}")
                temperature = temperature.replace(".", ",")
                temperature_file.write(temperature)
        except:
            print(f"An error occurred while trying to store temperature update. {traceback.format_exc()}")
            pass
        for counter in range(0, int(update_frequency)):
            time.sleep(1.0)
            if gc.kill_now:
                break
