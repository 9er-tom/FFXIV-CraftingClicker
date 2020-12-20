import tkinter as tk
import screenIO
import threading
import configparser as cnf
import ast


def openCursorSetWindow():
    newWindow = tk.Toplevel(master=window)
    newWindow.title("Set Button Positions")
    # newWindow.geometry("100x100")
    newWindow.focus()

    tk.Label(newWindow,
             text="Make sure your macros are placed on your hotbar and your crafting window is reset to its default position").grid(
        row=0, column=0)

    tk.Label(newWindow, text="Hover over your single Macro and press F1").grid(row=1, column=0)
    singlePosLabel = tk.Label(newWindow, text=f"Position: {screenIO.singleMacroPos}")
    singlePosLabel.grid(row=1, column=1)

    tk.Label(newWindow, text="Hover over your first double Macro and press F2").grid(row=2, column=0)
    doublePos1Label = tk.Label(newWindow, text=f"Position: {screenIO.doubleMacroPos1}")
    doublePos1Label.grid(row=2, column=1)

    tk.Label(newWindow, text="Hover over your second double Macro and press F3").grid(row=3, column=0)
    doublePos2Label = tk.Label(newWindow, text=f"Position: {screenIO.doubleMacroPos2}")
    doublePos2Label.grid(row=3, column=1)

    tk.Label(newWindow, text="Hover over the \"Synthesize\" Button and press F4").grid(row=4, column=0)
    craftPosLabel = tk.Label(newWindow, text=f"Position: {screenIO.craftBtnPos}")
    craftPosLabel.grid(row=4, column=1)

    def setSingleMacroPos(event):
        screenIO.setMousePos("singleMacro")
        singlePosLabel["text"] = f"Position: {screenIO.singleMacroPos}"

        config["Positions"]["singleMacroPos"] = f"({screenIO.singleMacroPos[0]}, {screenIO.singleMacroPos[1]})"
        with open(filename, "w") as configfile:
            config.write(configfile)

    def setDoubleMacroPos1(event):
        global configfile
        screenIO.setMousePos("doubleMacro1")
        doublePos1Label["text"] = f"Position: {screenIO.doubleMacroPos1}"

        config["Positions"]["doubleMacroPos1"] = f"({screenIO.doubleMacroPos1[0]}, {screenIO.doubleMacroPos1[1]})"
        with open(filename, "w") as configfile:
            config.write(configfile)

    def setDoubleMacroPos2(event):
        global configfile
        screenIO.setMousePos("doubleMacro2")
        doublePos2Label["text"] = f"Position: {screenIO.doubleMacroPos2}"

        config["Positions"]["doubleMacroPos2"] = f"({screenIO.doubleMacroPos2[0]}, {screenIO.doubleMacroPos2[1]})"
        with open(filename, "w") as configfile:
            config.write(configfile)

    def setCratPos(event):
        global configfile
        screenIO.setMousePos("craft")
        craftPosLabel["text"] = f"Position: {screenIO.craftBtnPos}"

        config["Positions"]["craftPos"] = f"({screenIO.craftBtnPos[0]}, {screenIO.craftBtnPos[1]})"
        with open(filename, "w") as configfile:
            config.write(configfile)

    def onClose():
        if screenIO.craftBtnPos != (0, 0) and (screenIO.singleMacroPos != (0, 0) or (
                screenIO.doubleMacroPos1 != (0, 0) and screenIO.doubleMacroPos2 != (0, 0))):
            frame.pack()
        newWindow.destroy()

    newWindow.bind("<F1>", setSingleMacroPos)
    newWindow.bind("<F2>", setDoubleMacroPos1)
    newWindow.bind("<F3>", setDoubleMacroPos2)
    newWindow.bind("<F4>", setCratPos)

    newWindow.protocol("WM_DELETE_WINDOW", onClose)


def singleMacroCraft():
    reps = repetitionEntry.get()
    dur = singleMacroDurEntry.get()

    repetitionEntry["bg"] = "white"
    singleMacroDurEntry["bg"] = "white"

    if reps:
        if dur:
            screenIO.reps = int(reps)
            screenIO.macroDuration = float(dur)

            config["CraftParams"]["reps"] = reps
            config["CraftParams"]["singleDur"] = dur

            with open(filename, "w") as configfile:
                config.write(configfile)

            thread = threading.Thread(target=screenIO.singleMacroCraft)
            thread.start()
            # screenIO.singleMacroCraft()
        else:
            singleMacroDurEntry["bg"] = "pink"
    else:
        repetitionEntry["bg"] = "pink"


def doubleMacroCraft():
    reps = repetitionEntry.get()
    dur1 = doubleMacro1DurEntry.get()
    dur2 = doubleMacro2DurEntry.get()

    if reps:
        if dur1 and dur2:
            screenIO.reps = int(reps)
            screenIO.doubleMacroDuration1 = float(dur1)
            screenIO.doubleMacroDuration2 = float(dur2)

            config["CraftParams"]["reps"] = reps
            config["CraftParams"]["doubleDur1"] = dur1
            config["CraftParams"]["doubleDur2"] = dur2

            with open(filename, "w") as configfile:
                config.write(configfile)

            thread = threading.Thread(target=screenIO.doubleMacroCraft)
            thread.start()
        else:
            singleMacroDurEntry["bg"] = "pink"
    else:
        repetitionEntry["bg"] = "pink"


if __name__ == '__main__':

    filename = "config.ini"
    config = cnf.ConfigParser()

    try:
        open(filename)
    except:
        config.add_section("Positions")
        config.set("Positions", "singleMacroPos", "(0,0)")
        config.set("Positions", "doubleMacroPos1", "(0,0)")
        config.set("Positions", "doubleMacroPos2", "(0,0)")
        config.set("Positions", "craftPos", "(0,0)")

        config.add_section("CraftParams")
        config.set("CraftParams", "reps", "0")
        config.set("CraftParams", "singleDur", "0")
        config.set("CraftParams", "doubleDur1", "0")
        config.set("CraftParams", "doubleDur2", "0")

        with open(filename, "w") as configfile:
            config.write(configfile)

    config.read(filename)

    screenIO.singleMacroPos = ast.literal_eval(config["Positions"]["singleMacroPos"])
    screenIO.doubleMacroPos1 = ast.literal_eval(config["Positions"]["doubleMacroPos1"])
    screenIO.doubleMacroPos2 = ast.literal_eval(config["Positions"]["doubleMacroPos2"])
    screenIO.craftBtnPos = ast.literal_eval(config["Positions"]["craftPos"])

    window = tk.Tk()
    window.title("FFXIV CraftingClicker")
    window.geometry("450x200")

    frame = tk.Frame()

    cursorSetWindowBtn = tk.Button(window, text="Set Button Positions", command=openCursorSetWindow)

    tk.Label(frame, text="Crafting Repetitions").grid(row=1, column=0)
    repetitionEntry = tk.Entry(frame)
    repetitionEntry.insert(0, config["CraftParams"]["reps"])

    tk.Label(frame).grid(row=2, column=0)

    tk.Label(frame, text="Single Macro Duration").grid(row=3, column=0)
    singleMacroDurEntry = tk.Entry(frame)
    singleMacroDurEntry.insert(0, config["CraftParams"]["singleDur"])

    tk.Button(frame, text="Start Single Macro Craft!", command=singleMacroCraft).grid(row=4, column=0)

    tk.Label(frame).grid(row=5, column=0)

    tk.Label(frame, text="First Double Macro Duration").grid(row=6, column=0)
    doubleMacro1DurEntry = tk.Entry(frame)
    doubleMacro1DurEntry.insert(0, config["CraftParams"]["doubleDur1"])

    tk.Label(frame, text="Second Double Macro Duration").grid(row=7, column=0)
    doubleMacro2DurEntry = tk.Entry(frame)
    doubleMacro2DurEntry.insert(0, config["CraftParams"]["doubleDur2"])

    tk.Button(frame, text="Start Double Macro Craft!", command=screenIO.doubleMacroCraft).grid(row=8, column=0)

    cursorSetWindowBtn.pack()

    if screenIO.craftBtnPos != (0, 0) and (screenIO.singleMacroPos != (0, 0) or (
            screenIO.doubleMacroPos1 != (0, 0) and screenIO.doubleMacroPos2 != (0, 0))):
        frame.pack()

    repetitionEntry.grid(row=1, column=1)
    singleMacroDurEntry.grid(row=3, column=1)
    doubleMacro1DurEntry.grid(row=6, column=1)
    doubleMacro2DurEntry.grid(row=7, column=1)

    progressLabel = tk.Label(frame).grid(row=9, column=0)
    tk.Label(frame, text="Made by ComfyLenny", fg="grey").grid(row=10, column=0)

    window.mainloop()
