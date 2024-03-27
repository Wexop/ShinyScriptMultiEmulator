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

time.sleep(2)

while not find:
    print('NOMBRE ESSAIS : ', count)
    if keyboard.is_pressed('q'):
        break
    print('POUR SORTIR DE LA BOUCLE : q')
    for emulator in emulators:
        pressButton(emulator['APos'])
        keyboard.press('x')

        if (datetime.now() - emulator["lastTime"]).seconds > 40:
            print('FOUND')
            find = True
            onFound()

        #print('COLOR CHECKED ', checkColor(emulator["colorPos"][0], emulator["colorPos"][1]), 'INITIAL COLOR ', emulator["pixelColor"])
        if checkCloseColor2(emulator["colorPos"], emulator["pixelColor"]):
            count += 1
            saveFile('count.txt', count)
            for i in range(len(emulator["pixelCoords"])):
                if keyboard.is_pressed('q'):
                    break
                pressButton(emulator["pixelCoords"][i])
            emulator["lastTime"] = datetime.now()
            print('RERUN')
