import pyautogui
from PIL import ImageGrab
from pynput.mouse import Listener, Button

pixels = []
APos = (0, 0)
pixelColor = (255, 255, 255)
pixelColorPos = (0, 0)

f = open('emulators.txt', 'r')
names = eval(f.read())
f.close()

if not names:
    names = []

emulName = input("Nom de l'émulateur que vous voulez modifier : ")


def saveEmulator(value, name):
    f = open(f"EMUL-{str(emulName)}-{name}", "w")
    f.write(str(value))
    f.close()


def save(value, name):
    f = open(name, "w")
    f.write(str(value))
    f.close()


if emulName not in names:
    names.append(emulName)
    save(names, 'emulators.txt')

config = input('Que voulez vous configurer ? a / color / pixels : ')


def on_click(x, y, button, pressed):
    if not pressed:
        return
    if button == Button.right:
        listener.stop()
        return

    pos = (x, y)
    print(pos)
    if config == 'a':
        APos = pos
        saveEmulator(pos, 'APos.txt')
        listener.stop()
    elif config == 'color':
        pixelColor = checkColor(x, y)
        print(pixelColor)
        saveEmulator(pixelColor, 'pixelColor.txt')
        saveEmulator(pos, 'colorPos.txt')
        listener.stop()
    else:
        pixels.append(pos)
        print(pixels)
        saveEmulator(pixels, 'pixels.txt')
        print('POUR STOP => CLIQUE DROIT')


def checkColor(x, y):
    return pyautogui.pixel(x, y)


with Listener(on_click=on_click) as listener:
    listener.join()
