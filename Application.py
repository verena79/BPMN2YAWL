from ast import parse
import PySimpleGUI as sg;
from Parser import parser

layout = [[sg.T("")],
          [sg.Text("Choose a file: ", size=(15,1)), sg.Input(), sg.FileBrowse(key="-IN-")],
          [sg.Text("Name your process: ", size=(15,1)), sg.Input(key="Path"), sg.Text("Hint: Add '.yawl' to your Name")],
          [sg.Button("Submit")],
          [sg.Text("Choose a file and name your process. Then click submit it to generate the YAWL Process XML")]
          ]

###Building Window
window = sg.Window('BPMN2YAWL', layout, size=(700,150))

# Create an event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event == "Submit" :
        print(values["-IN-"], values["Path"])
        parser(values["-IN-"], values["Path"])
       

window.close()


