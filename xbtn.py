import time
from machine import Pin

class Btn:
    # pin: pin, button connected to
    # pull: 1-PULLDOWN, 2-PULLUP
    # led: pin, LED connected to
    # led_inversed: if True, LED lights up when the button is released and goes out when pressed
    def __init__(self, pin=-1, led=-1, pull=1, led_inversed=False):
        
            # debounce delay
            self.debounceDelay = 50
            
            # double click delay
            self.doubleClickDelay = 200
            
            # long press delay
            self.longPressDelay = 1000
            
            # very long press delay
            self.veryLongPressDelay = 5000
            
            # should the LED blink after a long press?
            self.blinkOnLongPress = True
            
            # delay of repeated operation when holding the button
            self.repeatDelay = 500
            
            # delay of the first repeated operation when holding the button
            self.firstRepeatDelay = 1000
            
            # should the LED blink when repeated operation when holding the button?
            self.blinkOnRepeat = True

            # LEDs blinking delay
            self.ledOnDelay = 50
            
            # LEDs high level
            self.ledHigh = 1
            
            # LEDs low level
            self.ledLow = 0
            
            # debug True if you need to track some values
            self.debug = False
            
            # button state if it is released, not pressed
            self.highState = int(pull==1)
            
            # button state if it is pressed
            self.lowState =  not bool(self.highState)
            
            # button state
            self.btnState = 0
            
            # remembered state
            self.lastBtnState = 0
            
            # count of clicks
            self.clickCount = 0
            
            # flag button released
            self.buttonReleased = True
            
            # clicks sequence result
            self.strRes = ""
            
            # remembered time for debouncing
            self.lastDebounceTime = 0
            
            # number of operations while holding the button
            self.repeatCount = 0
            
            # remembered value
            self.oldRepeatCount = 0
            
            # remembered diode turn-off time
            self.ledOff_ms = 0
            
            # button hold duration
            self.L = 0
            
            # remembered value
            self.oldLedState = False
            
            # characters to form the result string
            self.singlePressKey = "."
            self.longPressKey = "-"
            self.veryLongPressKey = "V"
            
            self.btnGpio = pin
            if pin >= 0:
                self.btnPin =  Pin(pin, Pin.IN, pull)       
            self.ledGpio = led
            if led >= 0:
                self.ledPin =  Pin(led, Pin.OUT)
            if led_inversed:
                self.ledHigh = not bool(self.ledHigh)
                self.ledLow = not bool(self.ledLow)
            if (self.ledGpio>-1):
                self.ledPin.value(self.ledHigh)    
            self.ledOff()
            self.reading = self.btnPin.value()
            self.lastBtnState = self.reading
            self.tDown = time.ticks_ms()
            self.tUp = time.ticks_ms()

    def tick(self): 
      if self.btnGpio<0:
            return
  
      self.reading = self.btnPin.value()
      
      if self.reading != self.lastBtnState:
            # reset debounce timer
            self.lastDebounceTime = time.ticks_ms()

      if (((time.ticks_ms() - self.lastDebounceTime) > self.debounceDelay) and (self.reading != self.btnState)): 
            # button state has changed (the moment the button is pressed or released)
            self.btnState = self.reading
            self.buttonReleased = (self.btnState == self.highState)
            if self.buttonReleased:
                    # the button is released
                    self.tUp = time.ticks_ms()
                    self.ledOff()
                    self.L = self.tUp - self.tDown 
                    if self.L < self.longPressDelay:
                            self.strRes = self.strRes + self.singlePressKey  
                    else: 
                            if self.L < self.veryLongPressDelay: 
                                self.strRes = self.strRes + self.longPressKey
                            else: 
                                self.strRes = self.strRes + self.veryLongPressKey
                    if self.debug:
                            print("Button released after " + str(self.L) + " ms, res "  + self.strRes)
                    self.onReleased() 
            else: 
                    # the button is pressed
                    self.saveLed()
                    self.tDown = time.ticks_ms()
                    self.ledOn()
                    self.clickCount += 1            
                    if self.debug:
                            print("Button pressed ")
                    self.onPressed()               
      else:
          # button state has not changed
          if self.buttonReleased:
                self.oldRepeatCount = 0;
                if (time.ticks_ms() - self.tUp) > self.doubleClickDelay:
                        if (self.clickCount == 0): #Нет нажатия
                                pass
                        else:
                                if self.debug:
                                    print("Action required, res " + self.strRes)
                                if self.strRes == self.singlePressKey:
                                    self.onSinglePressed()
                                elif self.strRes == (self.singlePressKey + self.singlePressKey):
                                    self.onDoublePressed()
                                elif self.strRes == self.longPressKey:
                                    self.onLongPressed()
                                elif self.strRes == self.veryLongPressKey:
                                    self.onVeryLongPressed()
                                else:
                                    self.onSomethingPressed()
                        self.clickCount = 0
                        self.strRes = ""
                        
          else:
                self.L = time.ticks_ms() - self.tDown
                if self.L > (self.veryLongPressDelay + self.ledOnDelay):
                    pass 
                elif self.L > self.veryLongPressDelay:   
                    if self.blinkOnLongPress:
                        self.ledOff()
                elif self.L > (self.longPressDelay + self.ledOnDelay):   
                    pass 
                elif self.L > self.longPressDelay:   
                    if self.blinkOnLongPress:
                        self.ledOff()
                 
                if self.L < self.firstRepeatDelay + self.repeatDelay:
                    self.repeatCount = self.L  // self.firstRepeatDelay
                else:
                    self.repeatCount = (self.L - self.firstRepeatDelay) // self.repeatDelay + 1
                    
                if (self.repeatCount > self.oldRepeatCount):
                    self.oldRepeatCount = self.repeatCount
                    if self.blinkOnRepeat:
                        self.ledOff()
                    self.onRepeat()
                    
                self.ledOn() 

      self.lastBtnState = self.reading 
    
    def onPressed(self):
        pass

    def onReleased(self):
        pass
    
    def onSinglePressed(self):
        print("pin" + str(self.btnGpio) + ", simple click, " + str(self.L) + " ms")

    def onDoublePressed(self):
        print("pin" + str(self.btnGpio) + ", double click")
      
    def onLongPressed(self):
        print("pin" + str(self.btnGpio) + ", long click, " + str(self.L) + " ms") 
      
    def onVeryLongPressed(self):
        print("pin" + str(self.btnGpio) + ", very long click, " + str(self.L) + " ms") 
      
    def onSomethingPressed(self):
        print("pin" + str(self.btnGpio) + ", action not defined, res " + self.strRes) 
    
    def onRepeat(self):
        print("repeatCount =", str(self.repeatCount), " t =", str(self.L))
        
    def ledOn(self):
        if time.ticks_ms() - self.ledOff_ms < self.ledOnDelay:
            return
        if (self.ledGpio>-1):
            self.ledPin.value(self.ledHigh) 
             
    def ledOff(self):
        self.ledOff_ms = time.ticks_ms()
        if (self.ledGpio>-1):
            self.ledPin.value(self.ledLow)
             
    def saveLed(self): 
        if (self.ledGpio>-1):
            self.ledLow = self.ledPin.value()
            self.ledHigh = not bool(self.ledLow)
             
    def restoreLed(self):
        if (self.ledGpio>-1):
            self.ledPin.value(self.oldLedState)
            




