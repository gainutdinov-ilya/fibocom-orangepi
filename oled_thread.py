import time
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import os
import threading


class AsyncOledHelper:

    def __handle_counters(self):
        self.lineTimer += 1
        if self.lineTimer >= self.width:
            self.lineTimer = 0
            if not self.containerFixed:
                self.textContainerCounter += 1
            time.sleep(0.3)
            if self.textContainerCounter >= len(self.textContainer):
                self.textContainerCounter = 0

    def get_offset(self, text):
        temporaryImage = Image.new("1", (self.width, self.height))
        temporaryDraw = ImageDraw.Draw(temporaryImage)
        textLen = temporaryDraw.textlength(text, self.font)
        textPixelByStep = textLen / (self.width) + 0.5
        if textLen <= self.width:
            return 0
        elif self.lineTimer > self.width / 2:
            return textPixelByStep * (self.width - self.lineTimer)
        else:
            return textPixelByStep * self.lineTimer

    def drawText(self, text):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.draw.text((0 - self.get_offset(text), 0), text, font=self.font, fill=255)
        self.draw.rectangle((0, 32, self.lineTimer, 30), outline=0, fill=255)
        self.disp.image(self.image)
        self.disp.show()


    def __thread_worker(self):
        while True:
            if len(self.textContainer) <= self.textContainerCounter or len(self.textContainer) == 0:
                self.textContainerCounter = 0
                time.sleep(self.sleepTime)
                continue
            text = self.textContainer[self.textContainerCounter]
            self.drawText(text)
            self.__handle_counters()
            time.sleep(self.sleepTime)
        
    def fixText(self, counter):
        self.textContainerCounter = counter
        self.containerFixed = True

    def relaseText(self):
        self.textContainerCounter = 0
        self.containerFixed = False

    def addText(self, text):
        self.textContainer.append(text)


    def editText(self, text, index):
        self.textContainer[index] = text

    def getTextContainer(self):
        return self.textContainer

    def __init__(self, font="Roboto-Regular.ttf", speed = 1, sleepTime = 0):
        #Init I2C && OLED
        self.i2c = busio.I2C(SCL, SDA)
        self.disp = adafruit_ssd1306.SSD1306_I2C(128, 32, self.i2c)
        self.disp.fill(0)
        self.disp.show()
        self.width = self.disp.width
        self.height = self.disp.height
        #Init Pillow Objects
        self.image = Image.new("1", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        runtime_dir = os.getcwd()
        font_path = os.path.join(runtime_dir,font)
        self.font = ImageFont.truetype(font_path, 30, encoding="unic")
        #Data
        self.textContainer = []
        self.textContainerCounter = 0
        self.lineTimer = 0
        self.lineTimerSpeed = speed
        self.sleepTime = sleepTime
        self.containerFixed = False
        #StartThread
        self.thread = threading.Thread(target=self.__thread_worker, args=[])
        self.thread.start()


if __name__ == "__main__":
    a = AsyncOledHelper()
    while True:
        text = input("EnterText: ")
        a.addText(text)