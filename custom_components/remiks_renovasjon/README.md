# Remiks renovasjon 
Custom component to fetch the next Remiks garbage collection dates for Tromsø and Karlsøy in Norway. This component is in no way affiliated with or endoresed by Remiks.

## Installation
Copy the files to the custom_components folder under Home Assistant config folder, or install via HACS by using the URL of this repository.

To activate the integration, add the following section in your configuration.yaml and edit to customize:

```
remiks_renovasjon:
  streets: ["tomasjordvegen-129"]
  following: ["Optisk sortert avfall", "Glass og metallemballasje", "Posesupplering"]
  days_notice: 1
```

Also add the following to configuration.yaml get the sensors and binary sensors:

```
binary_sensor:
  - platform: remiks_renovasjon

sensor:
  - platform: remiks_renovasjon
```
If you already have a binary_sensor and sensor section, don't duplicate, just add the platform to both sections.



**streets:**\
A list of streets you'd like to get garbage collecting dates for. 
Go to the [Remiks search page](https://www.remiks.no/privat-husholdning/finn-din-tommedag/) in order to find the correct format for your address.
* Search for and click on your address
* Copy the part of the URL that corresponds to your address, for example:
* If the info page for your address is https://www.remiks.no/min-side/tomasjordvegen-129/, you must use "tomasjordvege-129" in the config.


**following:** \
A list of garbage collecting events you would like to follow. 
Supported events are: Optisk sortert avfall, Glass og metallemballasje and Posesupplering.
You will get sensor with the next date and a binary_sensor for each pair of event + street.

**days_notice:** \
Specify how many days in advance of the next garbage collecting date you'd like the binary_sensors to be activated.
1 means that the binary_sensors will turn on the day before. You can for instance use this to run an automation every night at 22h checking if you need to prepare for next days garbage collection.


[Did you find this useful? Buy me a coffee!](https://paypal.me/remimikalsen)
