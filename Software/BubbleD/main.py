"""
Author: Divya Pal
Institute: Physikalisches Institut, Universität Bonn
Modified: Mar 2022
"""

if __name__ == '__main__':
    import sys
    import os
    from PyQt5.QtWidgets import QApplication
    from configparser import ConfigParser
    from packages.set_arguments import dir_path, args

    # Starting the application
    app = QApplication(sys.argv)
    app.setApplicationName('Bubble Chamber Display')
    app.setApplicationVersion('1.0')

    config = ConfigParser()
    dir_path(args.config)   # Checking if path exists
    if args.table == '2':
        cfg_path = os.path.join(args.config, 'config_table2.ini')
    else:
        cfg_path = os.path.join(args.config, 'config_table1.ini')

    try:
        with open(cfg_path) as config_file:
            config.read_file(config_file)
            print('Configuration loaded from ', cfg_path)

    except IOError:   # Load default configs and write config.ini
        if args.table == '2':
            import packages.config_table2 as cfg
        else:
            import packages.config_table1 as cfg
        config = cfg.write_config(cfg_path)
        print('Loaded default configuartion and written', cfg_path)

    if args.controller == 'True':
        from packages.io_control import IOcontrol
        win = IOcontrol(args.port, config)
    elif args.controller == 'False':
        print("Starting GUI without external controller")
        from packages.gui_control import GUIcontrol
        win = GUIcontrol(config)
    ret = app.exec_()
    win.close()
    sys.exit(ret)
