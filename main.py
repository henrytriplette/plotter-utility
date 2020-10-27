import PySimpleGUI as sg
import configparser
import subprocess

# Read Configuration
config = configparser.ConfigParser()
config.read('config.ini')

def main():

    sg.change_look_and_feel('Reddit')

    menu = [
            [sg.Text('Launch Programs')],
            # [sg.Button('Open Blender', key='blender')],
            # [sg.Button('Open VNC Viewer', key='vnc')],
            # [sg.Button('Open VigoWriter', key='vigowriter')],
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
        [sg.Input(key='inputSVG'), sg.FileBrowse()],
        [sg.Button('Scale A4 Center', key='utility_scaleA4')],
        [sg.Button('Visualize path structure', key='utility_visualizeSVG')],
        [sg.Button('Optimize paths', key='utility_optimizeSVG')],
    ]

    hp = [
        [sg.Text('HP 7475a')],
        [sg.Button('SVG to HPGL', key='utility_convertHPGL')],
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
                print('utility_scaleA4')
        if event == 'utility_visualizeSVG':
            if values['inputSVG']:
                # outputFile = values['inputSVG'][:-4]
                subprocess.Popen('vpype read "' + str(values['inputSVG']) + '" show --colorful')
                print('utility_visualizeSVG')
        if event == 'utility_optimizeSVG':
            if values['inputSVG']:
                outputFile = values['inputSVG'][:-4] + '-Optimized.svg'
                subprocess.Popen('vpype read "' + str(values['inputSVG']) + '" linemerge --tolerance 0.1mm linesort write "' + str(outputFile) + '"')
                print('utility_optimizeSVG')
        if event == 'utility_convertHPGL':
            if values['inputSVG']:
                outputFile = values['inputSVG'][:-4] + '-Converted.hpgl'
                subprocess.Popen('vpype read "' + str(values['inputSVG']) + '" write --device hp7475a --page-format a4 --landscape --center "' + str(outputFile) + '"')
                print('utility_convertHPGL')


        # Software
        if event == 'blender':
            if config['software']['blender']:
                subprocess.Popen(config['software']['blender'])
                print('Opening blender')
        if event == 'vnc':
            if config['software']['vnc']:
                subprocess.Popen(config['software']['vnc'])
                print('Opening vnc')
        if event == 'vigowriter':
            if config['software']['vigowriter']:
                subprocess.Popen(config['software']['vigowriter'])
                print('Opening vigowriter')
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
        if event == 'folder_3d':
            if config['folders']['3d']:
                subprocess.Popen("%s %s" % ("explorer.exe", config['folders']['3d']))
                print('Opening 3d')
        if event == 'folder_vigowriter':
            if config['folders']['vigowriter']:
                subprocess.Popen("%s %s" % ("explorer.exe", config['folders']['vigowriter']))
                print('Opening vigowriter')
        if event == 'folder_p5js':
            if config['folders']['p5js']:
                subprocess.Popen("%s %s" % ("explorer.exe", config['folders']['p5js']))
                print('Opening p5.js')

        if event == 'upload':
            print('Begin FTP file Upload')

    window.Close()   # Don't forget to close your window!

if __name__ == '__main__':
    main()
