import numpy as np
import json
import mqtt_helper
import configparser
import time
import undistortion

DEBUG = True
patternsize = (7, 7)
config = configparser.ConfigParser()
config.read('config.ini')

if __name__ == '__main__':
    mainThread = mqtt_helper.Subscribe(config['broker']['topic'], config['broker']['ip'])
    mainThread.start()

    time.sleep(1)

    pub = mqtt_helper.Publish(config['broker']['topic'], config['broker']['ip'])
    data = { 'payload' : {'text': "test hello." } }
    pub.publish(json.dumps(data))

    time.sleep(1)

    data = { 'payload' : {'request': "photo" } }
    pub.publish(json.dumps(data))

    ks = np.array(json.loads(config['intrinsic']['ks']))
    dist = np.array(json.loads(config['intrinsic']['dist']))

    undistortion.undistortImgs('./img', ks, dist)

    mainThread.stop()