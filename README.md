## Pico Climate Monitoring Device - Semester Final Project - SWE 6823

This folder contains the code for the climate monitoring device comprising my final 
project, built using a Raspberry Pi Pico and MicroPython. The device utilizes a 3.5" 
LCD screen by Waveshare for display and an AM2302 environment sensor for gathering 
temperature and humidity data. It also includes two momentary switches for toggling 
display brightness and switching between screens.

Features

    Displays current temperature and humidity readings
    5-level adjustable screen brightness
    24-hour data graph display
    Updates display output approximately every 7 seconds

Hardware Components

    Raspberry Pi Pico
    3.5" LCD screen by Waveshare
    AM2302 environment sensor (connected to gpio 2)
    2x momentary switch buttons (connected to gpio 4 and gpio 7)

Credits

The code in this project is a combination of original work and code reused from 
the PicoPendant project published by GitHub user MZachmann. Due accreditation has 
been ensured by including comments in each file to describe the file contents in 
this context. This referenced external code resource was released under the MIT 
license, and is available at the following URL: https://github.com/MZachmann/PicoPendant. 
Original comments have been left intact; apologies if this causes in any confusion
in reviewing the code.