import time
from datetime import datetime

import keyboard
import pyautogui
from PIL import ImageGrab
import ctypes

# startX = 546
# startY = 316

# buttonRpos = (979, 1167)
# buttonLpos = (159, 1140)
# buttonStartpos = (503, 1131)
# buttonSelectpos = (659, 1122)
# buttonAPos = (973, 2123)

f = open("emulators.txt", "r")
emulatorsTab = eval(f.read())
f.close()
print(emulatorsTab, "COORDS")

emulators = []

f = open("count.txt", "r")
count = eval(f.read())
f.close()
print(count, "COUNT")

for emul in emulatorsTab:

    f = open(f"EMUL-{emul}-pixels.txt", "r")
    pixelCoords = eval(f.read())
    f.close()
    print(pixelCoords, "COORDS")

    f = open(f"EMUL-{emul}-pixelColor.txt", "r")
    pixelColor = eval(f.read())
    f.close()
    print(pixelColor, "COLOR")

    f = open(f"EMUL-{emul}-colorPos.txt", "r")
    colorPos = eval(f.read())
    f.close()
    print(colorPos, "COLOR POS")

    f = open(f"EMUL-{emul}-APos.txt", "r")
    APos = eval(f.read())
    f.close()
    print(APos, "APOS")


    emulators.append({"name": emul, "pixelCoords": pixelCoords, "pixelColor": pixelColor, "colorPos": colorPos, "APos": APos, "lastTime": datetime.now()})


print(emulators)



def pressButton(pos, duration=0):
    pyautogui.click(pos[0], pos[1], duration=duration)


def checkColor(x, y):
    return pyautogui.pixel(x, y)


def onFound():
    pass


def checkCloseColor(color1, color2):
    isClose = False
    avg2 = (color2[0] + color2[1] + color2[2]) / 3
    avg1 = (color1[0] + color1[1] + color1[2]) / 3

    if color1 == color2 or avg2 - 5 <= avg1 <= avg2 + 5:
        isClose = True

    return isClose


def checkCloseColor2(pos, color):
    return pyautogui.pixelMatchesColor(pos[0], pos[1], color, 5)


def saveFile(fileName, value):
    f = open(fileName, 'w')
    f.write(str(value))
    f.close()


find = False
lastTime = datetime.now()
minuteTime = datetime.now()
countMinute = 0

time.sleep(2)

keyboard.press('tab')

while not find:
    if keyboard.is_pressed('q'):
        keyboard.release('tab')
        break
    if (datetime.now() - minuteTime).seconds >= 60:
        minuteTime = datetime.now()
        message = f"1 MINUTE PASSED : {countMinute  } ESSAIES \n"
        print(message)
        countMinute = 0
        f = open("minute-average.txt", 'a')
        f.write(message )
        f.close()

    for emulator in emulators:
        pressButton(emulator['APos'])
        keyboard.press('x')
        if (datetime.now() - emulator["lastTime"]).seconds > 15:
            print('FOUND')
            find = True
            onFound()

        #print('COLOR CHECKED ', checkColor(emulator["colorPos"][0], emulator["colorPos"][1]), 'INITIAL COLOR ', emulator["pixelColor"])
        if checkCloseColor2(emulator["colorPos"], emulator["pixelColor"]):
            count += 1
            countMinute += 1
            saveFile('count.txt', count)
            print('NOMBRE ESSAIS : ', count)
            print('POUR SORTIR DE LA BOUCLE : q')
            for i in range(len(emulator["pixelCoords"])):
                if keyboard.is_pressed('q'):
                    keyboard.release('tab')
                    break
                pressButton(emulator["pixelCoords"][i])
            emulator["lastTime"] = datetime.now()
            #print('RERUN')
