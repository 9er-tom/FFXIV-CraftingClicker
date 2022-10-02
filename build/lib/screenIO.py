import pyautogui

singleMacroPos = (0, 0)
doubleMacroPos1 = (0, 0)
doubleMacroPos2 = (0, 0)
craftBtnPos = (0, 0)

macroDuration = 0
doubleMacroDuration1 = 0
doubleMacroDuration2 = 0

reps = 0


def setMousePos(button: str):
    global singleMacroPos, doubleMacroPos1, doubleMacroPos2, craftBtnPos
    pos = pyautogui.position()
    if button == "singleMacro":
        singleMacroPos = pos
    elif button == "doubleMacro1":
        doubleMacroPos1 = pos
    elif button == "doubleMacro2":
        doubleMacroPos2 = pos
    elif button == "craft":
        craftBtnPos = pos


def singleMacroCraft():
    global reps, craftBtnPos
    for x in range(reps):
        pyautogui.mouseDown(craftBtnPos)
        pyautogui.sleep(0.2)
        pyautogui.mouseUp(craftBtnPos)
        pyautogui.sleep(1)
        pyautogui.mouseDown(singleMacroPos)
        pyautogui.sleep(0.2)
        pyautogui.mouseUp(singleMacroPos)
        pyautogui.sleep(macroDuration)


def doubleMacroCraft():
    global reps, craftBtnPos
    for x in range(reps):
        print("double craft", x)
        pyautogui.mouseDown(craftBtnPos)
        pyautogui.sleep(0.2)
        pyautogui.mouseUp(craftBtnPos)
        pyautogui.sleep(1)

        pyautogui.mouseDown(doubleMacroPos1)
        pyautogui.sleep(0.2)
        pyautogui.mouseUp(doubleMacroPos1)

        pyautogui.sleep(doubleMacroDuration1)

        pyautogui.mouseDown(doubleMacroPos2)
        pyautogui.sleep(0.2)
        pyautogui.mouseUp(doubleMacroPos2)

        pyautogui.sleep(doubleMacroDuration2)
