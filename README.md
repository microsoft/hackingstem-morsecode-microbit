# Introduction
Microcontroller code for Microsoft Hacking STEM Harnessing Electricity to Communicate lesson plan adapted for micro:bit

# Getting Started
1. Download lesson assets at http://aka.ms/hackingSTEM
1. Build your Telegraph! and attach your Speaker!
1. Use uflash and nudatus to flash code to [micro:bit](http://microbit.org/) microcontroller (See Flashing Controller)
1. Verify data interactions in Excel
1. Ready, Set, Science!

# Flashing Controller:
Microbit has a very limited amount of space for code, to flash this program you will need to "minimize" it, which strips out extraneous stuff (like comments). We recommend using nudatus to minimize and uflash to flash.

## Get uflash
  pip install uflash

## Get nudatus
  pip install nudatus

## Minimize Code
  nudatus morse_code.py morse_code.minified.py

## Flash Code
  uflash morse_code.minified.py

# Microsoft Data Streamer Resources
1. https://aka.ms/data-streamer-developer
1. https://aka.ms/data-streamer

# Make it your own!
This project is licensed under the MIT open source license, see License. The MIT license allows you to take this project and make awesome things with it! MIT is a very permissive license, but does require you include license and copyright from LICENSE in any derivative work for sake of attribution.

Fork away! Let us know what you build!

**This is an archived repository.**
