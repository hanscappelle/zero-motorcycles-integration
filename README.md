# Zero Motorcycles Home Assistant Integration

This project is an attempt to create an integration to consume services provided by
Zero Motorcycles for their 3rd gen electric motorcycles that come with integrated
cellular connection and cloud service.

## How

All you need for this integration to work is your login. That is the username
and password you use for your app.

I'll try to have this published to HACS, if not you'll have to install it manually
by dropping the custom_components folder contents into your HA installation.

Then you can add a new integration, search for "Zero" to find this one:

![add integration](screenshots/Screenshot%202023-07-30%20at%2013.22.26.png)

Next you'll get a quick installation wizard, enter your credentials here:

![configuration wizard](screenshots/Screenshot%202023-07-30%20at%2013.22.36.png)

Once done this integration should be visible:

![shows integration](screenshots/Screenshot%202023-07-30%20at%2013.23.09.png)

An example of all the data it fetches:

![fetched data example](screenshots/Screenshot%202023-07-30%20at%2013.19.36.png)

## Why?

Because we can!

## Limitations

This is literally my first Home Assistant integration so there is still a lot to
do and as of now there are still some limitations. Here is an attempt to describe those:

* Coordindator is hardcoded to update every 5 minutes, if you need more you'll have to
change that manually for now.
* all sensors are non binary ones, some are likely just binary values but I haven't
provided those so far
* same for sensor classes, non are provided at this time

## Version History

# 0.2.0

renamed sensors to be unique per unit number and fetch values for all unit numbers

# 0.1.0

initial version

## About

Here is a picture of my 14.4 kWh Zero SRF premium with charge tank for 12 kW
maximum charging power (if conditions are met).

![motorcycle picture](https://i.ibb.co/zmYvXtP/DSCF0397.jpg)

## Notice

I have since sold this motorcycle (went to France!) and now mostly ride a 2021
Energice SS9+ with 21.5 kWh battery and 24 kW charge speed.