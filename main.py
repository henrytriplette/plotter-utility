import PySimpleGUI as sg
import configparser
import subprocess

import hp7475a

# Read Configuration
config = configparser.ConfigParser()
config.read('config.ini')

def main():

    sg.change_look_and_feel('Reddit')

    menu = [
            [sg.Text('Launch Programs')],
            # [sg.Button('Open Blender', key='blender')],
            # [sg.Button('Open VNC Viewer', key='vnc')],
            [sg.Button('Open Illustrator', key='illustrator')],
            [sg.Button('Open Photoshop', key='photoshop')],
            [sg.Button('Open Inkscape', key='inkscape')],

            [sg.Text('Open Folders')],
            [sg.Button('Open Home', key='folder_home')],
            # [sg.Button('Open 3D', key='folder_3d')],
            # [sg.Button('Open Vigowriter', key='folder_vigowriter')],
            [sg.Button('Open p5.js', key='folder_p5js')],
    ]

    utility = [
        [sg.Text('Utility SVG')],
        [sg.Text('Input SVG'), sg.Input(key='inputSVG'), sg.FileBrowse(file_types=(('SVG', '*.svg'),),)],
        [sg.Text('-- SVG --')],
        [sg.Button('Scale A4 Center', key='utility_scaleA4')],
        [sg.Button('Visualize path structure', key='utility_visualizeSVG')],
        [sg.Button('Optimize paths', key='utility_optimizeSVG')],
        [sg.Text('-- HPGL --')],
        [sg.Button('SVG to HPGL', key='utility_convertHPGL')],
    ]

    hp = [
        [sg.Text('HP 7475a')],
        [sg.Text('Input HPGL'), sg.Input(key='inputHPGL'), sg.FileBrowse(file_types=(('HPGL', '*.hpgl'),),)],
        [sg.Text('Comm Port'), sg.InputText(default_text="COM6", key="utility_comPort")],
        [sg.Text('Baud Rate'), sg.Combo(['9600', '4800'], default_value='9600', key="utility_baudRate")],
        [sg.Text('-- Send --')],
        [sg.Button('Start Plot', key='utility_startPlot')],
    ]

    footer = [
            [sg.Text('_' * 80)],
            [sg.Cancel(key='quit')],
    ]

    layout = [
                [sg.Column(menu), sg.Column(utility), sg.Column(hp)],
                [sg.Column(footer)]
            ]

    window = sg.Window('AxiDraw Utility', layout)


    while (True):

        # This is the code that reads and updates your window
        event, values = window.Read(timeout=100)

        if event == 'Exit' or event is None:
            break

        if event == 'quit':
            break

        # Utility
        if event == 'utility_scaleA4':
            if values['inputSVG']:
                outputFile = values['inputSVG'][:-4] + '-A4Scaled.svg'
                subprocess.Popen('vpype read "' + str(values['inputSVG']) + '" scale --to 21cm 29cm write --page-format a4 --center "' + str(outputFile) + '"')
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
                subprocess.Popen('vpype read "' + str(values['inputSVG']) + '" write --device hp7475a --page-format a4 --landscape --center "' + str(outputFile) + '"')
            else:
                sg.popup_error('Please select a valid .svg file')


        # Software
        if event == 'blender':
            if config['software']['blender']:
                subprocess.Popen(config['software']['blender'])
                print('Opening blender')
        if event == 'vnc':
            if config['software']['vnc']:
                subprocess.Popen(config['software']['vnc'])
                print('Opening vnc')
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
        if event == 'utility_startPlot':
            if values['inputHPGL']:
                hp7475a.sendToHp7475a(str(values['inputHPGL']), str(values['utility_comPort']), str(values['utility_baudRate']) )
            else:
                sg.popup_error('Please select a valid .hpgl file')


    window.Close()   # Don't forget to close your window!

if __name__ == '__main__':
    main()
