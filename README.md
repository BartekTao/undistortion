# undistortion

ues mqtt to get imgs, and undistort them

1. DEBUG = False => doesn't finish
2. if you want to run DEBUG = True, please download the example imgs from E3 to img folder
3. remember to run `pip3 install -r requirements.txt`

## TODO

1. Get imgs from broker. I can not get any imgs now...
2. Why sample code need to save newcameramtx to config file?
3. Code review and add some comments. (where should use try catch and write log)

## note

1. how to create broker? If we know this, we can create a more complete test.

## other resource

### python class know how

https://www.796t.com/content/1544582523.html

### MQTT doc

https://mosquitto.org/documentation/

### MQTT example

https://officeguide.cc/python-paho-library-mqtt-client-tutorial-examples/

### undistort function 差異

https://www.jianshu.com/p/6daa8dbbfa30