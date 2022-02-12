# Mouse Trap Monitor

A PIR Raspberry PI powered Python script to detect potential mouse movements.

## Hardware

This is what I used for this project, but most Raspberry PI models would work just as well providing they have GPIO to connect the PIR sensor to:

* Raspberry PI Zero WH (Wifi for networking and header for easy GPIO use but your use case may vary!)
* PIR sensor
* 3 Dupont jumper wires to connect them with
* (Optional) Case for PI and a coffee lid to protect the sensor!

## Software

### Running the script

From the git clone'd project directory:

    python3 ./start.py

### Dependencies

#### Origins

Based on [PiHut IFTTT Tutorial](https://thepihut.com/blogs/raspberry-pi-tutorials/using-ifttt-with-the-raspberry-pi) which 
is in turn based on [CamJam Edukit 2](https://github.com/CamJam-EduKit/EduKit2/blob/master/CamJam%20Edukit%202%20-%20RPi.GPIO/Code/5-PIR.py)

#### Python Package Dependencies

    pip3 install -U python-dotenv
        
(https://pypi.org/project/python-dotenv/)

## Appendix

Project formally known as GaragePI. Re-named it to make it more specific for others potential uses!