# img_viewer.py


import PySimpleGUI as sg
import time
import pickle

import os.path


# First the window layout in 2 columns


buttonsColumn = [
    [
       sg.Text("Data")
    ],
    [
       sg.Button("New Hunt", key="newHunt"), 
       sg.Button("Load Hunt", key="loadHunt"),
       sg.Button("Save",key="save"),
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
    saveFile(name, 0, [0])
 
    
def saveFile(name, time, counterList):
    path = os.path.abspath("saves") + "/" + name + '.tmr'
    with open(path, "wb") as f:  # Usa "wb" para modo de escritura binaria
        # Empaqueta el tiempo, el tamaño de counterList y counterList en un objeto
        data = (time, counterList)
        # Serializa y guarda el objeto en formato binario
        pickle.dump(data, f)
 


def selectFile():
        # Define the layout for the GUI
    layout = [
        [sg.Text('Select a file to load')],
        [sg.Input(), sg.FileBrowse(file_types=(("TMR Files", "*.tmr"),))], # FileBrowse button to open the file dialog
        [sg.OK(), sg.Cancel()] # OK and Cancel buttons
    ]

    # Create the window
    window = sg.Window('File Selector', layout)

    # Event loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        if event == 'OK':
            file_path = values[0] # the first element in values is the file path
            if file_path: # if a file was selected
                print(f'You selected: {file_path}')
                break

    window.close()
    return file_path



def loadFile():
    name = selectFile()
    if(name == ''):
        return   None
    fileName, _ =os.path.splitext( os.path.basename(name) ) # Mejora para obtener el nombre del archivo
    with open(name, "rb") as f:  # Abre el archivo en modo binario para lectura
        # Deserializa los datos del archivo
        time, counterList = pickle.load(f)
    
    return (fileName, time, counterList)
 

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
    if running:
        return  elapsedTime + (time.time() - initTime)
    else:
        return elapsedTime - initTime

def parseTime(val): 
    return time_convert( val)
    
def main():
    global initTime
    global running
    global elapsedTime
    window = sg.Window("Shiny Timer", layout)
    name = ""
    counterList = [0]

    while True:

        event, values = window.read(timeout = 0)
        time = getTime() 
 
        if event == "Exit" or event == sg.WIN_CLOSED:
            break 
        elif event == "newHunt":
            name = getGameName()
            window["Game_Name"].update(name)
            createFile(name)
        elif event == "loadHunt":
            res = loadFile()
            if(res is not None):
                name = res[0] 
                time =  res[1]  
                elapsedTime = res[1]  
                counterList = res[2] 
                window["Game_Name"].update(name)
 
        elif event == "start_pause":
            start_pause_Timer() 
        elif event == "reset":
            resetTimer()
            counterList = [0] 
        elif event == "nextCounter":
            counterList.append(0)  
        elif event == "removeOne":
            counterList[-1] -= 1  
        elif event == "addOne":
            counterList[-1] += 1
        elif event == "save":
            if(name ==''):
                name = getGameName()
                window["Game_Name"].update(name)
                createFile(name)
                
            saveFile(name, time, counterList)

        window["Currrent_Resets"].update(counterList[-1])
        window["Total_Resets"].update(sum(counterList))

        # if initTime != 0:
        window["Current_Time"].update(parseTime(time))
        # elif initTime == 0 and elapsedTime == 0:
        #     window["Current_Time"].update("00:00:00")

                          
    window.close()

if __name__ == '__main__':

    main()




