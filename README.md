rh
==

RaspHousy is a home automation software system that runs on RaspberryPi.

This is the vision:
  Replace your home's heating thermostat and the watering control for your lawn with a highly configurable system
  that also provides extensive metrics and can be configured / controlled / monitored remotely.

Some objectives:
* Do away with the thermostat and provide the option to read temps from several places in order to optimize heating.
* Control watering valves directly, also doing away with the "sprinkler timer".
* Provide detailed statistics about temperatures in various places of your property, including historic data.
* Other metrics such as humidity and any other measurement that can be added to the 1-wire network.
* Web-based interface for monitoring and control.

Stretch goals:
* If no local rain sensor is available, read weather online to decide if watering should be suspended.
* Provide sector control for heating (via some sort of valve for each heating outlet in your home) so that you may 
  only heat the sectors you're using (e.g. only bedrooms at night) and to even out heat distribution.
* Android app, in addition to web-based control.
* Some sort of centralized secure and anonymized web-hosting to avoid opening ports to your local network.

Status:
As of december 2013, I have parts of the basic hardware operational (RPi connected to the relay module), and basic software to manually control the relays. Next up: RESTful API for sensors and relays, hooking up the 1-wire network, simple website that uses the API for manual control.


For the first version, the requirements are going to be quite specific:

Hardware:
* RaspberryPi Model B Rev 2.0
* SainSmart 8xRelay module
* Dallas semiconductor DS9490R: 1-wire USB adaptor
* Dallas semiconductor DS18S20: 1-wire temperature sensors (9-bit resolution)
* Transistors and resistors to drive the "active-low" relay module with RPi's GPIO pins in active-high mode
* Breadboard, jumper-header wires to connect everything

Software:
* Raspbian (you may be able to use other distros)
* Python 2.7.x
* Google's Protocol Buffers and Python bindings
* WiringPi2, a library replicating Wiring (for Arduino) functionality for the RaspberryPi
* web.py for the RESTful API interfacing with sensors and relays.
* Nagios for alerts and monitoring.
* Cacti for historic data and displays.

Some of these requirements may change as development progresses.
I'll be adding some sort of release notes, and howto's in the form of blog posts as I build the system.
If there's interest, Q&A may be added as well.

I hope this is useful to someone. I'm sure having a lot of fun building it!

Cheers,
--Alberto

About me: I'm a software engineer at Google, and have basic knowledge about electronics. I'm basing my work on many others' previous experience, so I don't claim authorship to most of the procedures here.

DISCLAIMERS:
Try any of this at your own risk; if the system becomes sentient ant tries to kill you in your sleep don't blame me.
I do claim authorship of all code in this repo since (apart from the libraries used), I have written all of it from scratch. That said, I'll try to give credit where it's due for advice and inspiration; if you're the author of any procedure, quote, or software here that I haven't mentioned, please let me know and I'll be happy to oblige.
