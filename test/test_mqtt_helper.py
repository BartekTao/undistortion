import unittest
import mqtt_helper
import main

class TestBrokerConnection(unittest.TestCase):
    def setUp(self):
        broker = "test.mosquitto.org"
        self.mainThread = mqtt_helper.Subscribe("test", broker)
        self.has_connected = False

    def test_connection(self):  # test to check connection to broker
        self.mainThread.start()
        
        main.lock.acquire(3)
        self.has_connected = True
        main.lock.release()

        self.mainThread.stop()
        self.assertTrue(self.has_connected)

class TestPublish(unittest.TestCase):
    def setUp(self):
        broker = "test.mosquitto.org"
        self.publish = mqtt_helper.Publish("test", broker)
        self.has_connected = False

    def test_connection(self):  # test to publish msg to broker
        data = {"test": "test"}
        msgInfo = self.publish.publish(data)
        self.assertTrue(msgInfo.is_published())