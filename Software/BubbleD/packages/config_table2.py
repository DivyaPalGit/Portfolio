"""
Author: Divya Pal
Institute: Physikalisches Institut, Universität Bonn
Modified: Mar 2022
Purpose: This creastes a config.ini file in case it doesn't exist.
"""

from configparser import ConfigParser


def write_config(path):
    config = ConfigParser()
    config['Defaults'] = {'table': '2'}

    config['Paths'] = {'gui': './designer/GUI_Layout.ui',
                       'icon': 'icon.png',
                       'images': './images/Film 2411_2510',
                       }
    config['GUIParamters'] = {'gui_display': '1280x800',    # '1920x1080'
                              'proj_display': '3840x2160',  # '1920x1080'
                              'num_views': '3',
                              'num_images': '100',
                              'x_min': '-1000',
                              'x_max': '1000',
                              'y_min': '-1000',
                              'y_max': '1000',
                              'table_start': '695',
                              'table_stop': '1415',
                              'image_scale': 1.1,
                              'dy_v1': '680',
                              'dy_v2': '680',
                              'dy_v3': '680',
                              'dx_v1': '150',
                              'dx_v2': '150',
                              'dx_v3': '150',
                              }

    config['TeensyPins'] = {'port': '/dev/ttyACM0',
                            'next_slide': '7',      # '13'
                            'previous_slide': '8',  # '11'
                            'view1': '2',
                            'view2': '3',
                            'view3': '4',
                            'select_view': '9',
                            'poti_x': '1',          # '3'
                            'poti_y': '2',          # '4'
                            'joy_x': '3',           # '1'
                            'joy_y': '4',           # '2'
                            'led1': '10',           # '7'
                            'led2': '11',           # '6'
                            'led3': '12',           # '5'
                            }

    config['InputPanel'] = {'joy_tolx': '0.22',
                            'joy_toly': '0.22',
                            'joy_midx': '0.5',
                            'joy_midy': '0.5',
                            'joy_stepx': '1000',    #
                            'joy_stepy': '500',     # 500= ~20cm
                            'poti_tolx': '0.01',
                            'poti_toly': '0.01',
                            'poti_stepx': '1',
                            'poti_stepy': '1',
                            'joy_polx': '+',        # Valid +/-
                            'joy_poly': '-',
                            'poti_polx': '+',
                            'poti_poly': '-'
                            }

    try:
        with open(path, 'w') as configfile:
            config.write(configfile)
    except IOError:
        print(f'Unable to write in {path}')
        print('Starting software without writing config_table2.ini!')

    return config
