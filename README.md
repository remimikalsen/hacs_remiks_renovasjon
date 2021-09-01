# Remiks renovasjon 
Custom component to fetch the next Remiks garbage collection dates for Tromsø and Karlsøy in Norway. This component is in no way affiliated with or endoresed by Remiks.

## Installation
Copy the files to the custom_components folder under Home Assistant config folder, or install via HACS by using the URL of this repository.

To activate the integration, add the following section in your configuration.yaml and edit to customize:

```
remiks_renovasjon:
  street: "Tomasjordvegen"
  street_number: "129"
  track: ['Optisk sortert avfall', 'Glass og metallemballasje', 'Posesupplering']
```

**street:**\
In Tromsø county, spell streetnames with vegen. In Karlsøy county, spell streetname with veien. Don't include the street number in the street config option.

**street_number:** \
Your street number. For example 12 or 25B.

**track:** \
A list of garbage collecting events you would like to track. There will be a sensor created for each event.
Supported events are: Optisk sortert avfall, Glass og metallemballasje and Posesupplering.


[Did you find this useful? Buy me a coffee!](https://paypal.me/remimikalsen)
