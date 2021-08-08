## Aquasuite to Fan Control sync script

The Aquasuite provided by Aqua Computer is an awesome tool. Unfortunately all of it's sensor data is not available
to tools such as Remi Mercier's Fan Control. In my system I have some fans which shall check the SSD's and mainboard
temperature and the water temperature. As a workaround I wrote this script which uses the Aquasuite web api to
fetch my own system's water temperature and store it in a file based temperature sensor (Fan Control's way to
import external sensor data).

### To use this script you need:
* Basic Docker and Docker-Compose knowledge
* Windows + Ubuntu 18.04 or 20.04 running in WSL2
* Docker-Desktop with WSL2 enabled
* Remi Mercier's Fan Control
  * And add a file based temperature sensor there. It will automatically create a file for you.
* Aquasuite
  * And enable the export of your internal water temperature sensor to the Aquasuite web api. The URL you receive
    should look lile https://aquasuite.aquacomputer.de/circonus/SOME_GUID_HERE
* Copy the file template.env to .env and
   * Replace the dummy URL there by the real one pointing to the circonus dump
   * Replace the temperature sensor file name and the Fan Control directory path (from WSL2 perspective)
* Run this script via Docker-Compose and keep it running