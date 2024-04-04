import time
from machine import Pin

class Btn:
    def __init__(self, pin=-1, led=-1, pull=1):
            self.pull = pull;
            self.btnState = 0
            self.highState = int(self.pull==1)#1
            self.lowState =  not bool(self.highState)
            self.clickCount = 0
            self.debug = False
            self.buttonReleased = True
            self.strRes = ""
            self.lastBtnState = 0   
            self.lastDebounceTime = 0  
            self.debounceDelay = 50    
            self.doubleClickDelay = 200
            self.longPressDelay = 1000
            self.veryLongPressDelay = 5000
            self.blinkOnLongPress = True
            self.repeatCount = 0
            self.oldRepeatCount = 0
            self.repeatDelay = 500
            self.firstRepeatDelay = 1000
            self.blinkOnRepeat = True
            self.ledHigh = 1
            self.ledLow = 0
            self.ledOff_ms = 0
            self.ledOnDelay = 50
            self.L = 0
            self.oldLedState = False
            self.singlePressKey = "."
            self.longPressKey = "-"
            self.veryLongPressKey = "V"
            
            self.setPins(pin, led)
            self.ledOff()
            self.reading = self.btnPin.value()
            self.lastBtnState = self.reading
            self.tDown = time.ticks_ms()
            self.tUp = time.ticks_ms()

    def setPins(self, b, l):
            self.btnGpio = b
            if b >= 0:
                #pull_up = 1  #pull_down = 2
                self.btnPin =  Pin(b, Pin.IN, self.pull)       
            self.ledGpio = l
            if l >= 0:
                self.ledPin =  Pin(l, Pin.OUT)
        
    def tick(self): 
      if self.btnGpio<0:
            return
  
      self.reading = self.btnPin.value()
      
      if self.reading != self.lastBtnState:
            #сброс таймера дребезга
            self.lastDebounceTime = time.ticks_ms()

      if (((time.ticks_ms() - self.lastDebounceTime) > self.debounceDelay) and (self.reading != self.btnState)): 
            # изменилось состояние кнопки (момент нажатия или отпускания кнопки)
            self.btnState = self.reading
            #self.buttonReleased = (((self.btnState==self.highState) and (self.pull==1)) or ((self.btnState==self.lowState) and (self.pull==2)))
            self.buttonReleased = (self.btnState == self.highState)
            if self.buttonReleased:
                    # кнопка отпущена
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
                    # кнопка нажата
                    self.saveLed()
                    self.tDown = time.ticks_ms()
                    self.ledOn()
                    self.clickCount += 1            
                    if self.debug:
                            print("Button pressed ")
                    self.onPressed()               
      else:
          # не изменилось состояние кнопки
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
                t = time.ticks_ms() - self.tDown
                if t > (self.veryLongPressDelay + self.ledOnDelay):
                    pass 
                elif t > self.veryLongPressDelay:   
                    if self.blinkOnLongPress:
                        self.ledOff()
                elif t > (self.longPressDelay + self.ledOnDelay):   
                    pass 
                elif t > self.longPressDelay:   
                    if self.blinkOnLongPress:
                        self.ledOff()
                 
                if t < self.firstRepeatDelay + self.repeatDelay:
                    self.repeatCount = t  // self.firstRepeatDelay
                else:
                    self.repeatCount = (t - self.firstRepeatDelay) // self.repeatDelay + 1
                    
                if (self.repeatCount > self.oldRepeatCount):
                    print("repeatCount =", str(self.repeatCount), " t =", str(t))
                    self.onRepeat()
                    self.oldRepeatCount = self.repeatCount
                    if self.blinkOnRepeat:
                        self.ledOff()
                    
                self.ledOn() 

      self.lastBtnState = self.reading 
    
    def onPressed(self):
        pass

    def onReleased(self):
        pass
    
    def onSinglePressed(self):
        print("pin" + str(self.btnGpio) + ", простое нажатие, " + str(self.L) + " мс")

    def onDoublePressed(self):
        print("pin" + str(self.btnGpio) + ", двойное нажатие")
      
    def onLongPressed(self):
        print("pin" + str(self.btnGpio) + ", долгое нажатие, " + str(self.L) + " мс") 
      
    def onVeryLongPressed(self):
        print("pin" + str(self.btnGpio) + ", очень долгое нажатие, " + str(self.L) + " мс") 
      
    def onSomethingPressed(self):
        print("pin" + str(self.btnGpio) + ", действие не определено, res " + self.strRes) 
    
    def onRepeat(self):
        pass
        
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
            

# b = Btn(12, 13, 1)
# b.debug = True
# 
# 
# while True:
#     b.tick()                
# 
