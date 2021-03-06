import PySimpleGUI as sg
import configparser
import subprocess
import os

import send2serial

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
            [sg.Button('Open DrawingBotV3', size=(25, 1), key='drawingbot')],

            [sg.Text('Open Folders', size=(15, 1))],
            [sg.Button('Open Home', size=(25, 1), key='folder_home')],
            [sg.Button('Open p5.js', size=(25, 1), key='folder_p5js')],
            [sg.Button('Open plotter-vision', size=(25, 1), key='plotterVision')],

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
            sg.Text('Page Size', size=(15, 1)), sg.Combo(['a4', 'a3'], default_value='a4', size=(15, 1), key="utility_pageSize"),
            sg.Text('SVG Scale', size=(15, 1)), sg.Combo(['none', 'a4', 'a3'], default_value='a4', size=(15, 1), key="utility_pageScale"),
            sg.Text('Page Orientation', size=(15, 1)), sg.Combo(['portrait', 'landscape'], default_value='portrait', size=(15, 1), key="utility_pageOrientation")
        ],
        [sg.Button('SVG to HPGL', size=(25, 1), key='utility_convertHPGL')],
    ]

    svg_utility_bulk = [
        [sg.Text('Input Folder', size=(15, 1)), sg.Input(key='inputSVGFolder'), sg.FolderBrowse(target=('inputSVGFolder'))],
        [sg.Text('-- SVG - svgo --')],
        [sg.Button('Optimize SVG', size=(25, 1), key='utility_svgoOptimizeBulk')],
        [sg.Text('-- HPGL --')],
        [
            sg.Text('Page Size', size=(15, 1)), sg.Combo(['a4', 'a3'], default_value='a4', size=(15, 1), key="utility_pageSizeBulk"),
            sg.Text('SVG Scale', size=(15, 1)), sg.Combo(['none', 'a4', 'a3'], default_value='a4', size=(15, 1), key="utility_pageScaleBulk"),
            sg.Text('Page Orientation', size=(15, 1)), sg.Combo(['portrait', 'landscape'], default_value='portrait', size=(15, 1), key="utility_pageOrientationBulk")
        ],
        [sg.Button('SVG to HPGL', size=(25, 1), key='utility_convertHPGLBulk')],
    ]

    hpgl_utility = [
        [sg.Text('Input HPGL', size=(15, 1)), sg.Input(key='inputHPGLUtility'), sg.FileBrowse(file_types=(('HPGL', '*.hpgl'),),)],
        [sg.Text('Set Pen Speed', size=(15, 1)), sg.Slider(range=(0,38), default_value=25, size=(20,15), orientation='horizontal', key="utility_penSpeed"), sg.Button('Change Pen Speed', size=(25, 1), key='utility_changePenSpeed')],
    ]

    vpype_flow_imager = [
        [sg.Text('Input Image', size=(15, 1)), sg.Input(key='inputVpypeFlowImagerImage'), sg.FileBrowse(file_types=(('IMG', '*.*'),),)],

        [sg.Text('Simplex noise coordinate multiplier. The smaller, the smoother the flow field.', size=(55, 1)),
         sg.Slider(range=(1,10), default_value=1, size=(20,15), orientation='horizontal', key="vfi_noise_coeff")], # FLOAT 0.001
        [sg.Text('Number of rotated copies of the flow field', size=(55, 1)),
         sg.Slider(range=(0,10), default_value=1, size=(20,15), orientation='horizontal', key="vfi_n_fields")], # INTEGER
        [sg.Text('Minimum flowline separation', size=(55, 1)),
         sg.Slider(range=(0,10), default_value=8, size=(20,15), orientation='horizontal', key="vfi_min_sep")], # FLOAT 0.8
        [sg.Text('Maximum flowline separation', size=(55, 1)),
         sg.Slider(range=(0,100), default_value=10, size=(20,15), orientation='horizontal', key="vfi_max_sep")], # FLOAT
        [sg.Text('Maximum flowline length', size=(55, 1)),
         sg.Slider(range=(0,100), default_value=40, size=(20,15), orientation='horizontal', key="vfi_max_length")], # FLOAT
        [sg.Text('The input image will be rescaled to have sides at most max_size px', size=(55, 1)),
         sg.Slider(range=(1,10), default_value=8, size=(20,15), orientation='horizontal', key="vfi_max_size")], # INTEGER 800
        [sg.Text('PRNG seed (overriding vpype seed)', size=(55, 1)),
         sg.Slider(range=(10,100), default_value=25, size=(20,15), orientation='horizontal', key="vfi_seed")], # INTEGER
        [sg.Text('Flow field PRNG seed (overriding the main --seed)', size=(55, 1)),
         sg.Slider(range=(0,100), default_value=25, size=(20,15), orientation='horizontal', key="vfi_flow_seed")], # INTEGER

        [sg.Button('Start processing image', size=(25, 1), key='utility_RunVpypeFlowImager')],
    ]

    plot = [
        [sg.Text('Input HPGL', size=(15, 1)), sg.Input(key='inputHPGL'), sg.FileBrowse(file_types=(('HPGL', '*.hpgl'),),)],
        [sg.Text('Comm Port', size=(15, 1)), sg.InputText(default_text="COM3", key="utility_comPort"), sg.Button('List Ports', size=(15, 1), key='utility_listPorts')],
        [sg.Text('Baud Rate', size=(15, 1)), sg.Combo(['9600', '4800'], default_value='9600', size=(43, 1), key="utility_baudRate")],
        [sg.Button('Start Plot on HP747a', size=(25, 1), key='utility_startPlot_7475a')],
        [sg.Button('Start Plot on Graphtech MP4200', size=(25, 1), key='utility_startPlot_mp4200')],
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
                        sg.Tab('SVG Bulk', svg_utility_bulk, tooltip='SVG Bulk Processing'),
                        sg.Tab('HPGL Utility', hpgl_utility, tooltip='HPGL Utility'),
                        sg.Tab('Vpype Flow Imager', vpype_flow_imager, tooltip='Vpype Flow Imager'),
                        sg.Tab('Serial Print', plot, tooltip='Print on HP 7475a or Graphtech MP4200'),
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

                # Scale svg to desired paper size
                args = 'vpype';
                args += ' read "' + str(values['inputSVG']) + '"'; #Read input svg

                if (values['utility_pageOrientation'] == 'landscape'):
                    if (values['utility_pageScale'] == 'a3'):
                        args += ' scaleto 40cm 27.7cm';
                    elif (values['utility_pageScale'] == 'a4'):
                        args += ' scaleto 27.7cm 19cm';
                else:
                    if (values['utility_pageScale'] == 'a3'):
                        args += ' scaleto 27.7cm 40cm';
                    elif (values['utility_pageScale'] == 'a4'):
                        args += ' scaleto 19cm 27.7cm';

                args += ' write --device hp7475a';

                args += ' --page-size ' + str(values['utility_pageSize']);

                if (values['utility_pageOrientation'] == 'landscape'):
                    args += ' --landscape';

                args += ' --center';
                args += ' "' + str(outputFile) + '"'

                rendering = subprocess.Popen(args)
                rendering.wait() # Hold on till process is finished

                # print(args)
                print('- Exported ' + str(outputFile))

            else:
                sg.popup_error('Please select a valid .svg file')


        # Utility SVG Bulk
        if event == 'utility_svgoOptimizeBulk':
            if values['inputSVGFolder']:

                for root, dirs, files in os.walk(values['inputSVGFolder']):
                    for filename in files:
                        if filename.lower().endswith(('.svg')):
                            file_path = os.path.join(root, filename)
                            outputFile = file_path[:-4] + '-Optimized.svg'

                            rendering = subprocess.Popen('svgo "' + str(file_path) + '" -o "' + outputFile + '"', shell=True)
                            rendering.wait() # Hold on till process is finished

                            rendering = subprocess.Popen('vpype read "' + str(outputFile) + '" linemerge --tolerance 0.1mm linesort write "' + str(outputFile) + '"')
                            rendering.wait() # Hold on till process is finished
            else:
                sg.popup_error('Please select a valid folder')

        if event == 'utility_convertHPGLBulk':
            if values['inputSVGFolder']:

                for root, dirs, files in os.walk(values['inputSVGFolder']):
                    for filename in files:
                        if filename.lower().endswith(('.svg')):
                            file_path = os.path.join(root, filename)
                            outputFile = file_path[:-4] + '-Converted.hpgl'

                            # Scale svg to desired paper size
                            args = 'vpype';
                            args += ' read "' + str(values['inputSVG']) + '"'; #Read input svg

                            if (values['utility_pageOrientationBulk'] == 'landscape'):
                                if (values['utility_pageScaleBulk'] == 'a3'):
                                    args += ' scaleto 40cm 27.7cm';
                                elif (values['utility_pageScaleBulk'] == 'a4'):
                                    args += ' scaleto 27.7cm 19cm';
                            else:
                                if (values['utility_pageScaleBulk'] == 'a3'):
                                    args += ' scaleto 27.7cm 40cm';
                                elif (values['utility_pageScaleBulk'] == 'a4'):
                                    args += ' scaleto 19cm 27.7cm';

                            args += ' write --device hp7475a';

                            args += ' --page-size ' + str(values['utility_pageSizeBulk']);

                            if (values['utility_pageOrientationBulk'] == 'landscape'):
                                args += ' --landscape';

                            args += ' --center';
                            args += ' "' + str(outputFile) + '"'

                            rendering = subprocess.Popen(args)
                            rendering.wait() # Hold on till process is finished

                            # print(args)
                            print('- Exported ' + str(outputFile))

            else:
                sg.popup_error('Please select a valid folder')


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

        # Vpype Flow Imager
        if event == 'utility_RunVpypeFlowImager':
            if values['inputVpypeFlowImagerImage']:
                outputFile = values['inputVpypeFlowImagerImage'][:-3] + '-.svg'

                # Generate parameters
                args = ''
                args += 'noise_coeff= ' + str(values['vfi_noise_coeff'])
                args += ' n_fields= ' + str(values['vfi_n_fields'])
                args += ' min_sep= ' + str(values['vfi_min_sep'])
                args += ' max_sep= ' + str(values['vfi_max_sep'])
                args += ' max_length= ' + str(values['vfi_max_length'])
                args += ' max_size= ' + str(values['vfi_max_size'])
                args += ' seed= ' + str(values['vfi_seed'])
                args += ' flow_seed= ' + str(values['vfi_flow_seed'])
                subprocess.Popen('vpype flow_img "' + str(values['inputVpypeFlowImagerImage']) + '" write "' + str(outputFile) + '"')
            else:
                sg.popup_error('Please select a valid .jpg file')
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
        if event == 'drawingbot':
            if config['software']['drawingbot']:
                subprocess.Popen(config['software']['drawingbot'])
                print('Opening drawingbot')

        # Folders
        if event == 'folder_home':
            if config['folders']['home']:
                subprocess.Popen("%s %s" % ("explorer.exe", config['folders']['home']))
                print('Opening Home')
        if event == 'folder_p5js':
            if config['folders']['p5js']:
                subprocess.Popen("%s %s" % ("explorer.exe", config['folders']['p5js']))
                print('Opening p5.js')
        if event == 'plotterVision':
            if config['folders']['plotterVision']:
                subprocess.Popen("%s %s" % ("explorer.exe", config['folders']['plotterVision']))
                print('Opening plotter vision')

        # HP7475a
        if event == 'utility_listPorts':
            send2serial.listComPorts()

        if event == 'utility_startPlot_7475a':
            if values['inputHPGL']:
                send2serial.sendToPlotter(str(values['inputHPGL']), str(values['utility_comPort']), int(values['utility_baudRate']), '7475a' )
            else:
                sg.popup_error('Please select a valid .hpgl file')
        if event == 'utility_startPlot_mp4200':
            if values['inputHPGL']:
                send2serial.sendToPlotter(str(values['inputHPGL']), str(values['utility_comPort']), int(values['utility_baudRate']), 'mp4200' )
            else:
                sg.popup_error('Please select a valid .hpgl file')

    window.Close()   # Don't forget to close your window!

if __name__ == '__main__':
    main()
