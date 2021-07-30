# Mouse Trap Monitor

As featured in issue 108 of [The MagPi Magazine (August 2021)](https://magpi.raspberrypi.org/issues/108) 
and on the [Raspberry PI Blog](https://www.raspberrypi.org/blog/humane-mouse-trap-the-magpi-108).

A PIR Raspberry PI powered Python script to detect potential mouse movements.

## What is it's purpose?

If you have a humane mouse trap, it is especially important to know whether there is a mouse in it. If there is and you don't check, then it will eventually run out of food and water which would be bad news for the mouse...

Checking the traps are boring and it is useful to know whether there is likely to be activity in remote locations e.g. a garage. This project was designed to help with that problem.

## How does it work?

The PIR sensor needs to ideally point at the (preferably) humane mouse trap. The below values are based on the default example.

* The PIR sensor will look for movement every 0.1 seconds.
* When movement is detected, it will add one to the counter and will wait for 30 seconds.
* After 24 hours (approx) it will fire off a request to IFTTT which in turn will trigger a request to Pushbullet. You will then get a notification on your phone telling you how many instances of movement have been detected in the last 24 hours. The counter is reset.

    If the movement is significantly higher than prevous days e.g. 20% higher then there is a chance there might be a mouse in the trap and it may be worth checking out!

> Example: In my case I was getting approx 800ish triggers a day. At 1036 I found that there was a mouse in the trap. Note that there is a degree of variation and nothing is exact so use your instincts.

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
5. From within your cloned directory e.g. `cd ~/mouse-trap-monitor` Copy the example `.env.example` file to `.env` and alter variables to your preference including putting in your IFTTT key *important*

        cp .env.example .env

    If you don't do this you will likely get errors as it won't know what values to use.

### Running the script

From anywhere (substituting the locaton as relevant):

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