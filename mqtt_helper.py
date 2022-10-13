import os
import cv2
import paho.mqtt.client as mqtt
import logging
import json
import threading
import main
import file_helper

class Subscribe(threading.Thread):
    def __init__(self, topics, broker):
        main.lock.acquire()
        print("connecting to broker %s" % broker)
        threading.Thread.__init__(self)
        self.killswitch = threading.Event()
        self.client = mqtt.Client()
        self.topics = topics
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(broker)
        main.lock.release()

    def on_connect(self, client, userdata, msg, rc):
        logging.info(f'connected with code: {rc}')
        for topic in self.topics:
            self.client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        if main.DEBUG:
            data = json.loads(msg.payload)
            if 'text' in data:
                print(data['text'])
        else:
            cmds = json.loads(msg.payload)
            if 'text' in cmds:
                print(cmds)

            if 'data' in cmds:
                os.makedirs('./download', exist_ok=True)
                for i in range(len(cmds['data'])):
                    img = file_helper.coverToCV2(cmds['data'][i])
                    filename = 'photo_' + str(i) + '.png'
                    fullPath = os.path.join('./download', filename)
                    cv2.imwrite(fullPath, img)

                    # push image path to imgs_queue
                    main.imgs_queue.put(fullPath)

            if 'dist_data' in cmds:
                img = file_helper.coverToCV2(cmds['dist_data'])
                fullPath = './download/dist_image.png'
                cv2.imwrite(fullPath, img)

    def stop(self):
        self.killswitch.set()

    def run(self):
        try:
            self.client.loop_start()
            self.killswitch.wait()
        finally:
            self.client.loop_stop()

class Publish(object):
    def __init__(self, topic, broker):
        self.client = mqtt.Client()
        self.topic = topic
        self.client.connect(broker)

    def publish(self, data):
        return self.client.publish(self.topic, json.dumps(data))