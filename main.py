import numpy as np
import json
import mqtt_helper
import configparser
import time
import undistortion

DEBUG = False
patternsize = (7, 7)
config = configparser.ConfigParser()
config.read('config.ini')

if __name__ == '__main__':
    # subscribe broker
    sub_topics = [config['broker']['topic_sub_respone'], config['broker']['topic_sub_photo']]
    mainThread = mqtt_helper.Subscribe(sub_topics, config['broker']['ip'])
    mainThread.start()
    time.sleep(2)

    # publish test message to broker
    pub = mqtt_helper.Publish(config['broker']['topic_pub'], config['broker']['ip'])
    data = {'text': "test hello." }
    pub.publish(data)

    # publish photo request message to broker
    data = {'request': "photo" }
    pub.publish(data)
    
    # publish secret message to broker
    data = {'request': "EC234_NOL" }
    pub.publish(data)
    
    # wait for img download
    # TODO
    time.sleep(5)

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