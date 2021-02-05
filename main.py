import PySimpleGUI as sg
import configparser
import subprocess
import os

import hp7475a

# Read Configuration
config = configparser.ConfigParser()
config.read('config.ini')

def main():

    sg.theme('Topanga')

    link = [
            [sg.Text('Launch Programs', size=(15, 1))],
            [sg.Button('Open Illustrator', size=(25, 1), key='illustrator')],
            [sg.Button('Open Photoshop', size=(25, 1), key='photoshop')],
            [sg.Button('Open Inkscape', size=(25, 1), key='inkscape')],

            [sg.Text('Open Folders', size=(15, 1))],
            [sg.Button('Open Home', size=(25, 1), key='folder_home')],
            [sg.Button('Open p5.js', size=(25, 1), key='folder_p5js')],
    ]

    svg_utility = [
        [sg.Text('Input SVG', size=(15, 1)), sg.Input(key='inputSVG'), sg.FileBrowse(file_types=(('SVG', '*.svg'),),)],
        [sg.Text('-- SVG - svgo --')],
        [sg.Button('Optimize SVG', size=(25, 1), key='utility_svgoOptimize')],
        [sg.Text('-- SVG - vpype --')],
        [sg.Button('Scale A4 Center', size=(25, 1), key='utility_scaleA4')],
        [sg.Button('Visualize path structure', size=(25, 1), key='utility_visualizeSVG')],
        [sg.Button('Optimize paths', size=(25, 1), key='utility_optimizeSVG')],
        [sg.Text('-- HPGL --')],
        [
            sg.Text('Page Size', size=(15, 1)), sg.Combo(['tight', 'a6', 'a5', 'a4', 'a3', 'letter', 'legal', 'executive', 'tabloid'], default_value='a4', size=(15, 1), key="utility_pageSize"),
            sg.Text('Page Orientation', size=(15, 1)), sg.Combo(['portrait', 'landscape'], default_value='portrait', size=(15, 1), key="utility_pageOrientation")
        ],
        [sg.Button('SVG to HPGL', size=(25, 1), key='utility_convertHPGL')],
    ]

    hpgl_utility = [
        [sg.Text('Input HPGL', size=(15, 1)), sg.Input(key='inputHPGLUtility'), sg.FileBrowse(file_types=(('HPGL', '*.hpgl'),),)],
        [sg.Text('Set Pen Speed', size=(15, 1)), sg.Slider(range=(0,38), default_value=25, size=(20,15), orientation='horizontal', key="utility_penSpeed"), sg.Button('Change Pen Speed', size=(25, 1), key='utility_changePenSpeed')],
    ]

    hp = [
        [sg.Text('Input HPGL', size=(15, 1)), sg.Input(key='inputHPGL'), sg.FileBrowse(file_types=(('HPGL', '*.hpgl'),),)],
        [sg.Text('Comm Port', size=(15, 1)), sg.InputText(default_text="COM6", key="utility_comPort"), sg.Button('List Ports', size=(15, 1), key='utility_listPorts')],
        [sg.Text('Baud Rate', size=(15, 1)), sg.Combo(['9600', '4800'], default_value='9600', size=(43, 1), key="utility_baudRate")],
        [sg.Button('Start Plot', size=(25, 1), key='utility_startPlot')],
    ]

    # layout = [
    #             [sg.Column(menu), sg.Column(utility), sg.Column(hp)],
    #             [sg.Column(footer)]
    #         ]

    layout = [
                [sg.TabGroup(
                    [
                        [
                        sg.Tab('SVG Utility', svg_utility, tooltip='SVG Utility'),
                        sg.Tab('HPGL Utility', hpgl_utility, tooltip='HPGL Utility'),
                        sg.Tab('HP7475a', hp, tooltip='hp7475a Utility'),
                        sg.Tab('Links', link, tooltip='Links'),
                        ]
                    ])
                ],
                [sg.Cancel(key='quit')],
            ]

    window = sg.Window('AxiDraw Utility', layout)


    while (True):

        # This is the code that reads and updates your window
        event, values = window.Read(timeout=100)

        if event == 'Exit' or event is None:
            break

        if event == 'quit':
            break

        # Utility SVG
        if event == 'utility_svgoOptimize':
            if values['inputSVG']:
                subprocess.Popen('svgo "' + str(values['inputSVG']) + '"', shell=True)
            else:
                sg.popup_error('Please select a valid .svg file')
        if event == 'utility_scaleA4':
            if values['inputSVG']:
                outputFile = values['inputSVG'][:-4] + '-A4Scaled.svg'
                subprocess.Popen('vpype read "' + str(values['inputSVG']) + '" scaleto 20cm 28cm write --page-size a4 --center "' + str(outputFile) + '"')
            else:
                sg.popup_error('Please select a valid .svg file')
        if event == 'utility_visualizeSVG':
            if values['inputSVG']:
                # outputFile = values['inputSVG'][:-4]
                subprocess.Popen('vpype read "' + str(values['inputSVG']) + '" show --colorful')
            else:
                sg.popup_error('Please select a valid .svg file')
        if event == 'utility_optimizeSVG':
            if values['inputSVG']:
                outputFile = values['inputSVG'][:-4] + '-Optimized.svg'
                subprocess.Popen('vpype read "' + str(values['inputSVG']) + '" linemerge --tolerance 0.1mm linesort write "' + str(outputFile) + '"')
            else:
                sg.popup_error('Please select a valid .svg file')
        if event == 'utility_convertHPGL':
            if values['inputSVG']:
                outputFile = values['inputSVG'][:-4] + '-Converted.hpgl'
                if (values['utility_pageOrientation'] == 'landscape'):
                    subprocess.Popen('vpype read "' + str(values['inputSVG']) + '" write --device hp7475a --page-size ' + str(values['utility_pageSize']) + ' --landscape --center "' + str(outputFile) + '"')
                else:
                    subprocess.Popen('vpype read "' + str(values['inputSVG']) + '" write --device hp7475a --page-size ' + str(values['utility_pageSize']) + ' --center "' + str(outputFile) + '"')
            else:
                sg.popup_error('Please select a valid .svg file')

        # Utility HPGL
        if event == 'utility_changePenSpeed':
            if values['inputHPGLUtility']:
                with open(str(values['inputHPGLUtility'])) as r:
                  text = r.read().replace("SP1;", "VS"+ str(values['utility_penSpeed'][:-2]) +";SP1;").replace("VS;", "VS"+ str(values['utility_penSpeed'][:-2]) +";SP1;")
                  print(text)
                with open(str(values['inputHPGLUtility']), "w") as w:
                  w.write(text)
            else:
                sg.popup_error('Please select a valid .hpgl file')

        # Software
        if event == 'illustrator':
            if config['software']['illustrator']:
                subprocess.Popen(config['software']['illustrator'])
                print('Opening Illustrator')
        if event == 'photoshop':
            if config['software']['photoshop']:
                subprocess.Popen(config['software']['photoshop'])
                print('Opening photoshop')
        if event == 'inkscape':
            if config['software']['inkscape']:
                subprocess.Popen(config['software']['inkscape'])
                print('Opening inkscape')

        # Folders
        if event == 'folder_home':
            if config['folders']['home']:
                subprocess.Popen("%s %s" % ("explorer.exe", config['folders']['home']))
                print('Opening Home')
        if event == 'folder_p5js':
            if config['folders']['p5js']:
                subprocess.Popen("%s %s" % ("explorer.exe", config['folders']['p5js']))
                print('Opening p5.js')

        # HP7475a
        if event == 'utility_listPorts':
            hp7475a.listComPorts()
        if event == 'utility_startPlot':
            if values['inputHPGL']:
                hp7475a.sendToHp7475a(str(values['inputHPGL']), str(values['utility_comPort']), int(values['utility_baudRate']) )
            else:
                sg.popup_error('Please select a valid .hpgl file')

    window.Close()   # Don't forget to close your window!

if __name__ == '__main__':
    main()
