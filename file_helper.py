import cv2
import base64
import pickle

def saveConfig(config):
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def coverToCV2(data):
    imdata = base64.b64decode(data)
    buf = pickle.loads(imdata)
    image = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    return image