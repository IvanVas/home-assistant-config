# Home Assistant Configuration

** This is a work in progress **

This repository contains my configuration for [Home Assistant](https://www.home-assistant.io/).

I'm running Home Assistant on a [Intel Core I7-8565U I5-8265U Quad Core](https://www.aliexpress.com/item/32850708878.html) with 32GB of ram and 1tb NVMe SSD. Its essentially an Intel Nuc knock-off.

I run Home Assistant Core on [k3s](https://k3s.io/) along with a handful of other services, checkout my [home repository](https://github.com/imduffy15/home) for all the infrastructure provisioning automation.

## Devices

### Lighting

I use a range of WiFi lights that have esp8266 chips and use the [tuya cloud](https://www.tuya.com/) platform. I flash these with [tasmota](https://github.com/arendst/Tasmota). Primarily I'm using a Phillips hue emulation for control via Amazon Alexa, additionally, all devices are configured as MQTT clients and report to Home Assistant via this.

#### Bulbs

 ~~- [Novostella Smart Bulb B22 RGBCW 600lm](https://www.amazon.co.uk/gp/product/B07DN4NLKM) - General indoor bulb~~
 
 ~~- [Novostella B22 LED Tunable Smart Bulb RGBCW 1300lm](https://www.amazon.co.uk/gp/product/B07SB4Q4JT) - Indoor bulb for areas that require more light~~
 
 ~~- [Novostella E27 RGB Alexa Light Bulbs 900lm](https://www.amazon.co.uk/gp/product/B07NQMFJMJ) - Bulb for some of my lamps~~
 
 ~~- [Novostella RGB LED Smart Spotlight 20 W 2 LED Floodlight](https://www.amazon.de/gp/product/B07VNR9XW7) - Outdoor flood light installed at the back of the house for lighting up the garden~~
 
 ~~- [Avatar Smart LED Bulbs E14](https://www.amazon.de/dp/B07W6Z6KPG) - Bulb for some more lamps~~
 
 ~~- [Avatar GU10 Smart Bulb](https://www.amazon.co.uk/gp/product/B082F7NWWB) - Outdoor GU10 up/down fittings at the front and side of the house~~

All the above bulbs are no longer flashable with tasmota, please look at preflashed bulbs instead, Athom provide a range of B22 and E27 bulbs https://www.aliexpress.com/item/4001281509550.html

#### LED Strips

 - [BTF-LIGHTING WS2811 5m DC12V 60leds/m](https://www.amazon.co.uk/BTF-LIGHTING-300LEDs-Addressable-Flexible-Non-waterproof/dp/B01CNL6K52) - My go to LED strip
 - ~~[H803 WIFI LED WIFI Controller](https://www.aliexpress.com/item/32854807170.html) - controller for the WS2811 strips, its based on a ESP12 chip and runs [WLED](https://github.com/Aircoookie/WLED)~~

https://shop.allnetchina.cn/products/quinled-dig-uno-led-controller and https://shop.allnetchina.cn/products/quinled-dig-quad-digital-led-controller from https://quinled.info/ are more stable and more reliable

Checkout https://quinled.info/2018/10/03/power-supply-selection/ for information on power supplies

Check out https://quinled.info/2019/06/03/what-digital-5v-12v-rgbw-led-strip-to-buy/ for information on buying LED strips

### Networking

 - [Ubiquiti EdgeMAX EdgeRouter X - ER-X](https://linitx.com/product/ubiquiti-unifi-in-wall-802.11ac-wave-2-wi-fi-access-point---uap-iw-hd/14588) - I've went back and forth between this and the Unifi USG, figured the EdgeRouter was better value for money. Been happy with it so far, gone between Stock firmware and OpenWRT a few times but have settled on the stock firmware
 - [Ubiquiti UniFi In-Wall 802.11ac Wave 2 Wi-Fi Access Point - UAP-IW-HD](https://linitx.com/product/ubiquiti-unifi-in-wall-802.11ac-wave-2-wi-fi-access-point---uap-iw-hd/15499) * 6
 - [Ubiquiti UniFi 24 Port 250W PoE Gigabit Network Switch US-24-250W](https://linitx.com/product/ubiquiti-unifi-in-wall-802.11ac-wave-2-wi-fi-access-point---uap-iw-hd/14252) - Switch, for the moment I only have one of them, will likely be adding more. Slightly disappointed that I didn't get something with L3 functionality as intervlan communications must go back to the router
 - [Ubiquiti UniFi Cloud Key Controller Gen2 Plus](https://linitx.com/product/ubiquiti-unifi-in-wall-802.11ac-wave-2-wi-fi-access-point---uap-iw-hd/15498) - originally purchased to manage my unifi gear but is now unused as the unifi controller software runs along side Home Assistant. If anyone in Ireland/UK is interested in a second hand barely used one let me know.

### Television

 - [TvHeadEnd](https://tvheadend.org/) - Runs along side home assistant. Provides Live TV over the network
 - [Geniatech MyGica® DVB-T2/T](https://www.amazon.co.uk/gp/product/B01BU4UIOW) * 2 - For viewing [Soarview](https://www.saorview.ie/)
 - [Telestar DIGIBIT R 1 HD SAT Reciever](https://www.amazon.co.uk/gp/product/B008OVPYCQ) - For viewing [freesat](https://www.freesat.co.uk/)
 - [Triax Quattro LNB](https://www.triax.uk/products/satellite/lnb-units/classic-lnb/universal-quattro-lnb-tqtd)
 - [LTE QR12 14dBi Gain UHF Aerial](https://www.triax.uk/products/terrestrial/aerial-antennas/uhf-antennas/lte-qr-12-t-ch-21-60-14dbi-gain-lte-800-protected-antenna-aerial)
 - [Nvidia Shield](https://www.amazon.co.uk/gp/product/B07Z6QQZPF) - Connects to the TVs and uses Kodi to access TvHeadend, Netflix and Amazon Prime.
 - [LG CX](https://www.lg.com/us/tvs/lg-oled65cxpua-oled-4k-tv) [LG BX](https://www.lg.com/us/tvs/lg-oled65bxpua-oled-4k-tv) - Decision hasn't been made yet but it will be one of these LG tvs.

### Security

 - [Vanderbilt SPC](https://vanderbiltindustries.com/spc) - Alarm System
 - [DS-2CD2365G1-I 6MP](https://www.hikvision.com/en/products/IP-Products/Network-Cameras/Pro-Series-EasyIP-/DS-2CD2365G1-I/) - CCTV Cameras
 - [DS-7604NI-K1/4P/4TB](https://www.hikvision.com/en/products/IP-Products/Network-Video-Recorders/Pro-Series/ds-7604ni-k1-4p-b-0/) - NVR
 - (DoorBird IP Video Door Station D1101V)[https://www.doorbird.com/downloads/datasheet/datasheet_d1101_surface_en.pdf] - Doorbell

### Appliances

Haven't had a chance to play with these yet but they are apparently all WiFi enabled.

 - [Bosh WAT286H0GB Washing Machine](https://www.bosch-home.ie/productlist/washers-and-dryers/washing-machines/front-loading-washing-machines/WAT286H0GB)
 - [Bosh WTWH7660GB Dryer](https://www.bosch-home.ie/productlist/washers-and-dryers/tumble-dryers/heat-pump-dryers/WTWH7660GB)
 - [Bosh SMI68TS06E Dishwasher](https://www.bosch-home.ie/productlist/SMI68TS06E)
 - [Neff B47FS34HOB](https://www.neff-home.com/ie/products-list/ovens-and-compact-ovens/ovens/single-steam-ovens/B47FS34H0B)

### Misc

 - [Rockrobo S5](https://www.amazon.com/Roborock-Robotic-Connectivity-Navigating-Capacity/dp/B0792BWMV4) - Vacuum cleaner, runs [Valetudo RE](https://github.com/rand256/valetudo)
 - [Smart WiFi Power Strip](https://www.amazon.co.uk/gp/product/B07D2FN1P5) - Power Strip, Tuya Cloud based so runs Tasmota
 - [Drayton Wiser Smart Thermostat Dual Zone Heating and Hot Water Control](https://www.amazon.co.uk/Drayton-Wiser-Thermostat-Heating-Control/dp/B075GS4WFK?ref_=ast_sto_dp) - Boiler programmer and Thermostat
 - [M5StickC](https://m5stack.com/products/stick-c) - ESP32 chip, bluetooth, WiFi and IR more so used for prototyping things
 - [Sonoff RF Bridge](https://sonoff.tech/product/accessories/433-rf-bridge) - primarily used for communicating with blind motors and some RF buttons.
 - [Dooya DM25LE](https://www.aliexpress.com/item/32614830824.html) - Blind motors
 - [Broadlink RM-Mini3](https://www.amazon.co.uk/Broadlink-RM-Mini3-Universal-Controller-Compatible-Black/dp/B01G1PZUK2) - WiFi IR bridge, I would likely be better of replacing this with an M5StickC
 - [TECKIN Smart Sockets 13A](https://www.amazon.co.uk/gp/product/B07JFJQ3ZP) - Smart Plugs, again tuya cloud based so running Tamosta. I wouldn't recommend buying these as the chip has changed in newer versions and flashing them is no longer possible.
 - [OralB bluetooth toothbrush](https://www.amazon.co.uk/s?k=oralb+bluetooth&ref=nb_sb_noss) - Toothbrush, see https://twitter.com/imduffy15/status/1256731450231132160
