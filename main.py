# img_viewer.py


import PySimpleGUI as sg
import time
import os.path


# First the window layout in 2 columns


buttonsColumn = [
    [
       sg.Text("Load Data")
    ],
    [
       sg.Button("New Hunt", key="newHunt"), 
       sg.Button("Load Hunt", key="loadHunt")
    ],
    [ 
       sg.HSeparator()
    ],
    [
       sg.Text("Timer Controls")
    ],
    [
        sg.Button("Start/pause Timer", key="start_pause"),
        sg.Button("Reset Timer", key="reset")
    ],
    [
       sg.Text("Encounter Controls")
    ],
    [
        sg.Button("Found!!",key="nextCounter"),
        sg.Button("-1", key="removeOne"),
        sg.Button("+1", key="addOne"),
    ], 

]

# For now will only show the name of the file that was chosen

infoColumn = [
    [sg.Text("Game: "), sg.Text(size=(40, 1), key="Game_Name")],
    [sg.Text("Curren time: "), sg.Text(size=(40, 1), key="Current_Time")],
    [sg.Text("Total Resets: "), sg.Text(size=(40, 1), key="Total_Resets")],
    [sg.Text("Current Resets: "), sg.Text(size=(40, 1), key="Currrent_Resets")]
]


# ----- Full layout -----

layout = [
    [
        sg.Column(buttonsColumn),
        sg.VSeperator(),
        sg.Column(infoColumn),
    ]
]


# ----- Input layout -----

inputLayout = [
    [
        sg.In(size=(25, 1), enable_events=True, key="name"),
        sg.Button("OK", key="inputName")
    ]
]


def getGameName():
    inputWindow = sg.Window("Enter name", inputLayout)
        
    while True:
        event, values = inputWindow.read()
        gameName = values["name"]
        if event == "inputName" and gameName != "":
            inputWindow.close()
            break
            
    return gameName


initTime = 0
elapsedTime = 0
running = False

def start_pause_Timer():
    global elapsedTime
    global initTime
    global running
    print(time_convert(elapsedTime))
    if not running:
        running = True
        initTime = time.time()
    else:
        elapsedTime = elapsedTime + time.time() - initTime
        running = False
        initTime = 0


def resetTimer():
    global elapsedTime
    global initTime
    global running


    if running:
        initTime = time.time()
        elapsedTime = 0
    else:
        initTime = 0
        elapsedTime = 0
    

def createFile(name):
    path = os.path.abspath("saves") + "/" + name
    f = open(path,"w+")
    f.write("00:00:00\n")
    f.write("1\n")
    f.write("0\n")
    f.close()
    
def saveFile(name, time, counterList):
    path = os.path.abspath("saves") + "/" + name
    f = open(path,"w")
    f.write(time+"\n")
    f.write(str(len(counterList))+"\n")
    for a in counterList:
        f.write(str(a)+"\n")
    f.close()


def loadFile():
    return 0
    

def time_convert(inputTime):
    m = inputTime // 60
    s = inputTime % 60
    h = m // 60
    m = m % 60
    s_str = str(int(s))
    if len(s_str) == 1:
        s_str = '0' + s_str
    m_str = str(int(m))
    if len(m_str) == 1:
        m_str = '0' + m_str
    h_str = str(int(h))
    if len(h_str) == 1:
        h_str = '0' + h_str
    return  h_str + ":" + m_str + ":" + s_str

def getTime():
    global initTime
    global elapsedTime
    
    return time_convert( elapsedTime + (time.time() - initTime))
    
def main():
    window = sg.Window("Shiny Timer", layout)
    name = ""
    counterList = [0]

    while True:

        event, values = window.read(timeout = 0)
        time = window["Current_Time"].DisplayText

        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        
        elif event == "newHunt":
            name = getGameName()
            window["Game_Name"].update(name)
            createFile(name)
        elif event == "loadHunt":
            loadFile()
        elif event == "start_pause":
            start_pause_Timer()
        elif event == "reset":
            resetTimer()
            counterList = [0]
        elif event == "nextCounter":
            counterList.append(0)
            saveFile(name, time, counterList)
        elif event == "removeOne":
            counterList[-1] -= 1
            saveFile(name, time, counterList)
        elif event == "addOne":
            counterList[-1] += 1
            saveFile(name, time, counterList)

        window["Currrent_Resets"].update(counterList[-1])
        window["Total_Resets"].update(sum(counterList))

        if initTime != 0:
            window["Current_Time"].update(getTime())
        elif initTime == 0 and elapsedTime == 0:
            window["Current_Time"].update("00:00:00")

                          
    window.close()

if __name__ == '__main__':

    main()




