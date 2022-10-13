import cv2
import numpy as np
import json
import mqtt_helper
import configparser
import undistortion
import threading
import queue
import time

DEBUG = False
patternsize = (7, 7)
config = configparser.ConfigParser()
config.read('config.ini')

lock = threading.Lock()
imgs_queue = queue.Queue()

if __name__ == '__main__':
    # subscribe broker
    sub_topics = [config['broker']['topic_sub_respone'], config['broker']['topic_sub_photo']]
    mainThread = mqtt_helper.Subscribe(sub_topics, config['broker']['ip'])
    mainThread.start()

    # you can only publish messages after subscribing
    # waiting for connection
    lock.acquire()
    print("connected")
    lock.release()

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

    # set ks, and dist to config
    undistortion.find_points(patternsize)

    # get ks, dist and newcameramtx from config
    ks = np.array(json.loads(config['intrinsic']['ks']))
    dist = np.array(json.loads(config['intrinsic']['dist']))
    newcameramtx = np.array(json.loads(config['intrinsic']['newcameramtx']))

    data = {'request': "dist_photo" }
    pub.publish(data)

    time.sleep(3)

    img = undistortion.undistort('./download/dist_image.png', ks, dist, newcameramtx)
    cv2.imwrite("./undistort_img/D_dist_image.png", img)

    mainThread.stop()