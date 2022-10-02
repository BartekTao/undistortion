import os
import cv2
import paho.mqtt.client as mqtt
import logging
import json
import threading
import main
import undistortion

class Subscribe(threading.Thread):
    def __init__(self, topic, broker):
        threading.Thread.__init__(self)
        self.killswitch = threading.Event()
        self.client = mqtt.Client()
        self.topic = topic
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(broker)

    def on_connect(self, client, userdata, msg, rc):
        logging.info(f'connected with code: {rc}')
        self.client.subscribe(self.topic)

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
                os.makedirs('./q2', exist_ok=True)
                for i in range(len(cmds['data'])):
                    # TODO4: save iamge to ./q2, so you have to decode msg
                    image = cmds['data'][i]
                    filename = 'photo_' + str(i) + '.png'
                    cv2.imwrite(os.path.join('./q2', filename), image)

            if 'dist_data' in cmds:
                # TODO5: you have to decode msg
                image = cmds['dist_data']
                cv2.imwrite('dist_image.png', image)

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
        self.client.publish(self.topic, json.dumps(data))