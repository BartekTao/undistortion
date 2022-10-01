import main

def saveConfig():
    with open('config.ini', 'w') as configfile:
        main.config.write(configfile)