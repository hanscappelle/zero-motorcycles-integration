# Zero Motorcycles Home Assistant Integration

[![GitHub Release][releases-shield]][releases]
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

This project is an attempt to create an integration to consume services provided by
Zero Motorcycles for their 3rd gen electric motorcycles that come with integrated
cellular connection and cloud service.

## How

All you need for this integration to work is your login. That is the username
and password you use for the official Zero Motorcycles app.

Currently not available in default HACS repo because that requires me to make a brand first. 

For now you either have to install it manually by dropping the custom_components
folder contents into your HA installation. Or by adding this repo as a custom
repo within HACS. For that, within HACS just select "add repo" then pick "integration"
as type and enter a name and the url of this repo. Or read here https://hacs.xyz/docs/faq/custom_repositories/

Then you can add a new integration, search for "Zero" to find this one:

![add integration](screenshots/Screenshot%202023-07-30%20at%2013.22.26.png)

Next you'll get a quick installation wizard, enter your credentials here:

![configuration wizard](screenshots/Screenshot%202023-07-30%20at%2013.22.36.png)

Once done this integration should be visible:

![shows integration](screenshots/Screenshot%202023-07-30%20at%2013.23.09.png)

An example of all the data it fetches. Note that in later releases sensor names
have been adapted to include unit numbers so that these can be created for all
units in case someone owns more than 1 zero motorcycle.

![fetched data example](screenshots/Screenshot%202023-07-30%20at%2013.19.36.png)

## Why?

Because we can!

## Limitations

This is literally my first Home Assistant integration so there is still a lot to
do and as of now there are still some limitations. Here is an attempt to describe those:

* Coordindator is hardcoded to update every 5 minutes, if you need more you'll have to
change that manually for now. For this search for the `(minutes=5)`line in the `coordinator.py`
file and change it to what you prefer.

## Upcoming features

* parse numeric values (if needed that is)
* allow user to configure update interval from UI

## Version History

# 0.4.0

* created device_tracker for location
* simplified sensor names + fix for multiple units
* get version from manifest instead of constants
* ignored yaml setup since not supported


# 0.3.0

* added binary sensors
* added device class to most sensors

# 0.2.0

* renamed sensors to be unique per unit number
* fetch values for all unit numbers

# 0.1.0

initial release

## About

Here is a picture of my 14.4 kWh Zero SRF premium with charge tank for 12 kW
maximum charging power (if conditions are met).

![motorcycle picture](https://i.ibb.co/zmYvXtP/DSCF0397.jpg)

## Notice

I have since sold this motorcycle (went to France!) and now mostly ride a 2021
Energice SS9+ with 21.5 kWh battery and 24 kW charge speed.

## Resources

A good code example for sensors and device_trackers is the Porsche Connect integration 
with sources available at https://github.com/CJNE/ha-porscheconnect 
