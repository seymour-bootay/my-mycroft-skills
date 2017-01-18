**Presence-Detection skill**
=============================


This skill uses Bluetooth Beacon Presence Detectors to track the location of a ble (Bluetooth Low Energy) beacon.  The detectors send data 
via mqtt to a Bluetooth Beacon Presence Detection Server that exposes an api to retrieve the current location of a specified  beacon.  
The specific implementation I am using is from [Happy Bubbles Technology](https://www.happybubbles.tech/) / [Happy Bubbles Github Repos](https://github.com/happy-bubbles)    


----------

Prerequisites
-------------
> - **BLE Beacon** - I am using an iBeacon as a keychain on my keys.
> - **Bluetooth Beacon Presence Detectors**  - hardware to detect if a ble beacon is in a room. [Happy Bubbles Presence Detectors](https://www.happybubbles.tech/presence/)
> - **Bluetooth Beacon Presence Detection Server** - software that subscribes to mqtt topic that the detectors report their current state to.
> - **MQTT Broker** - I am using [EMQ v2](http://emqtt.io/)

----------


Installation
------------
> - clone or copy into the skills directory (until skills store/hub is available).
> - copy the data from presence-detection.conf into your mycroft.conf file. 
>       - update the values you just copied into mycroft.conf
>           - **presence_system** is the type of presence system. Currently only happy-bubbles is supported but other options could be easily swapped in.
>           - **presence_url** is the url to retrieve the beacon data (api of the presence server).
----------


## Current State ##

Features
--------------------
 - **locate** *keys* 
  

 > **Note:**
> - **locate** is a LocateBeaconKeyword
> - ***keys***  is the name of the beacon, as configured on the presence server.  If the skill is unable to find a match in the response from the api it will tell you the beacon is not found.

----------------------------------

TODO
--------------------
- looking into adding functionality on the Mycroft-Android Phone/Wear project to allow android devices act as beacons.
- finding beacons is only the first step, I am looking into ways to help Mycroft be more context aware, as in when it receives commands from a specific location 
it will act appropriately.  A good example would be turn on light, if it knows what room your in you will not have to specify it.
