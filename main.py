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
    # subscribe broker
    mainThread = mqtt_helper.Subscribe(config['broker']['topic'], config['broker']['ip'])
    mainThread.start()
    time.sleep(2)

    # publish test message to broker
    pub = mqtt_helper.Publish(config['broker']['topic'], config['broker']['ip'])
    data = {'text': "test hello." }
    pub.publish(data)

    # publish photo request message to broker
    data = {'request': "photo" }
    pub.publish(data)

    if DEBUG:
        imgPath = './img'
    else:
        imgPath = './download'

    # set ks, and dist to config
    undistortion.find_points(patternsize, imgPath)

    # get ks, dist and newcameramtx from config
    ks = np.array(json.loads(config['intrinsic']['ks']))
    dist = np.array(json.loads(config['intrinsic']['dist']))
    newcameramtx = np.array(json.loads(config['intrinsic']['newcameramtx']))

    undistortion.undistortImgs(imgPath, ks, dist, newcameramtx)

    mainThread.stop()