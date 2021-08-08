# Simple Python script which fetches JSON data in the Circonus from the Aquasuite Web Service
# and stores it in a local file so it can be progressed by the FanControl tool by Remi Mercier

import requests
import os
import json
import time

if __name__=="__main__":
    target_filename = os.environ["FAN_CONTROL_TARGET_SENSOR"]
    temperature_url = os.environ["TEMPERATURE_URL"]
    update_frequency = float(os.environ["UPDATE_FREQUENCY_SECONDS"])
    print(f"Synching sensor data from {temperature_url} to {target_filename}")
    print(f"Temperature update frequency: {update_frequency:0.1f}s")
    while True:
        try:
            response = requests.get(temperature_url, timeout=5)
            temp_data = json.loads(response.text)
            temperature: str = list(temp_data.values())[0]
            with open(f"/fancontrol/{target_filename}", "w") as temperature_file:
                print(f"Received water temperature update: {temperature}")
                temperature = temperature.replace(".", ",")
                temperature_file.write(temperature)
        except:
            print("An error occurred while trying to fetch temperature update")
            pass
        time.sleep(update_frequency)
