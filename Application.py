from ast import parse
import PySimpleGUI as sg;
from TestParse import parser

layout = [[sg.T("")],
          [sg.Text("Choose a file: "), sg.Input(), sg.FileBrowse(key="-IN-")],
          [sg.Text("Name your process: "), sg.Input(key="Path")],
          [sg.Button("Submit")],
          [sg.Text("Choose a file and name your process. Then click submit it to generate the YAWL Process XML")]
          ]

###Building Window
window = sg.Window('BPMN2YAWL', layout, size=(600,150))

# Create an event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event == "Submit" :
        print(values["-IN-"], values["Path"])
        parser(values["-IN-"], values["Path"])
       

window.close()


