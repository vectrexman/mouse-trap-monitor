# Mouse Trap Monitor

A PIR Raspberry PI powered Python script to detect potential mouse movements.

## Hardware

This is what I used for this project, but most Raspberry PI models would work just as well providing they have GPIO to connect the PIR sensor to:

* Raspberry PI Zero WH (Wifi for networking and header for easy GPIO use)
* PIR sensor
* 3 Dupont jumper wires to connect them with
* (Optional) Case for PI and a coffee lid to protect the sensor!

## Software

### Installation / Setup

> Note: This is not a thorough guide, although if you know roughly what you are doing it is probably enough

1. Follow the [PiHut IFTTT Tutorial](https://thepihut.com/blogs/raspberry-pi-tutorials/using-ifttt-with-the-raspberry-pi)
2. Install python3 if it isn't already (may be covered by IFTTT tutorial)
3. Install python-dotenv:

        pip3 install -U python-dotenv
4. Clone this repository into a directory of your choice e.g. your home directory at `~/`:

        git clone git@github.com:vectrexman/mouse-trap-monitor.git

### Running the script

From anywhere (substituring the locaton as relevant):

    python3 ~/mouse-trap-monitor/start.py

Or from within the directory that you cloned `mouse-trap-monitor`:

    python3 ./start.py

### Dependencies

#### Origins

This project is built on the excellent work undertaken as part of these projects:

Based on [PiHut IFTTT Tutorial](https://thepihut.com/blogs/raspberry-pi-tutorials/using-ifttt-with-the-raspberry-pi) which 
is in turn based on [CamJam Edukit 2](https://github.com/CamJam-EduKit/EduKit2/blob/master/CamJam%20Edukit%202%20-%20RPi.GPIO/Code/5-PIR.py)

#### Python Package Dependencies

    pip3 install -U python-dotenv
        
(https://pypi.org/project/python-dotenv/)

## Appendix

Project formally known as GaragePI. Re-named it to make it more specific for other peoples potential (re)use!