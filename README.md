# Micropython button

Micropython button code for Arduino, ESP8266, ESP32. Allows to process various button events: simple press, double press, long press and others


How to use
-
There are several options for using the button

Simplest:
    Override the onPressed() procedure, this event will fire when pressed immediately.
    You can also override the onRepeat() procedure,
    it will work over and over again when you hold down the button.
    This will create an analogue of a computer keyboard button.

Second way:
    Override the procedures onSinglePressed(), onDoublePressed(),
    onLongPressed(), onVeryLongPressed(), onSomethingPressed(),
    thereby receiving events with a simple single, double, long, very long press,
    and also get any combination of single, long and very long presses,
    that is, something similar to Morse code sequences    

Advantages
-
The button code does not contain wait operators like time.sleep(),
therefore, tracking button events does not slow down the main loop of the controller
and allows you to process other events without delay 
