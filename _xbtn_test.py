# EN
# Copy this file and the xbtn.py file to the microcontroller.
# To use the button, it is better to create a descendant class based on the Btn class.
# For the descendant class, you need to override the procedures that are called when the button is clicked.
# There are several options for using the button
# 
# Simplest:
#     override the onPressed() procedure, this event will fire when pressed immediately
#     you can also override the onRepeat() procedure,
#     it will work over and over again when you hold down the button
#     This will create an analogue of a computer keyboard button.
# 
# Second way:
#     override the procedures onSinglePressed(), onDoublePressed(),
#     onLongPressed(), onVeryLongPressed(), onSomethingPressed(),
#     thereby receiving events with a simple single, double, long, very long press,
#     and also get any combination of single, long and very long presses,
#     that is, something similar to Morse code sequences    
# 
# The button code does not contain wait operators like time.sleep(),
# therefore, tracking button events does not slow down the main loop of the controller
# and allows you to process other events without delay
# 
#
# RU
# Скопируйте этот файл и файл xbtn.py на микроконтроллер.
# Для использования кнопки лучше создать класс потомок на основе класса Btn.
# Для класса потомка нужно переопределить процедуры, которые вызываются при нажатии кнопки.
# Возможно несколько вариантов использования кнопки
# 
# Самый простой:
#     переопределить процедуру onPressed(), это событие сработает при нажатии сразу
#     также можно переопределить процедуру onRepeat(),
#     она будет срабатывать раз за разом при удержании кнопки
#     Таким образом получится аналог кнопки компьютерной клавиатуры
# 
# Второй способ:    
#     переопределить процедуры onSinglePressed(), onDoublePressed(),
#     onLongPressed(), onVeryLongPressed(), onSomethingPressed(),
#     тем самым получать события при простом однократном, двукратном, долгом, очень долгом нажатии,
#     а также получить любую комбинацию из однократных, долгих и очень долгих нажатий,
#     то есть что-то похожее на последовательности азбуки Морзе
# 
# Код кнопки не содержит операторов ожидания типа time.sleep(),
# поэтому отслеживание событий кнопки не тормозит основной цикл работы контроллера
# и позволяет обрабатывать другие события без задержек

from xbtn import Btn

#------------------------------------------------------
class Btn1(Btn):
    def __init__(self, pin = -1, led = -1):
        super().__init__(pin=pin, led=led, pull=2)
        
    def onPressed(self):
        print(" button 1 is pressed ")

    def onRepeat(self):
        self.onPressed()

#------------------------------------------------------
class Btn2(Btn):
    def __init__(self, pin = -1, led = -1):
        super().__init__(pin=pin, led=led, pull=2)
        
    def onSinglePressed(self):
        print(" button 2 is pressed ")

    def onDoublePressed(self):
        print(" button 2 is double-pressed ")

#------------------------------------------------------
btn1 = Btn1(pin=12, led=2)
btn2 = Btn2(pin=13, led=2)

while True:
    btn1.tick()
    btn2.tick()    

