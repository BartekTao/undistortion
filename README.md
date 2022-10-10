# undistortion

ues mqtt to get imgs, and undistort them

1. for mac: `brew install mosquitto`
2. if you want to run DEBUG = True, please download the example imgs from E3 to img folder
3. remember to run `pip3 install -r requirements.txt` on first clone
4. run `python3 main.py`

## TODO

1. Code review and add some comments.  
   (We need to understand each line of the code)
   (where should use try catch and write log)
2. clean requirements.txt

## DONE

1. Get imgs from broker. I can not get any imgs now...
   * Should add team number as a topic suffix. ex: `deep_learning_lecture_5`
   * Sub and Pub topic are different!! Sub `server_response_5` to get echo, sub `secret_photo_5` to get secret photo, and pub `deep_learning_lecture_5` to sent request. (ref: config.ini)
2. Why sample code need to save newcameramtx to config file? only needs to be calculated once, because imgs size are the same

## note

1. how to create broker? If we know this, we can create a more complete test.

## other resource

### python array

```python
x = [[1, 2, 3, 4],
     [5, 6, 7, 8],
     [9, 10, 11, 12],
     [13, 14, 15, 16]]

x[:, 0] = [1, 5, 9, 13]
x[:, 2] = [3, 7, 11, 15]
x[:, 1:3] = [[2, 3],
             [6, 7],
             [10, 14]]
# 分號控制範圍，1:4 => 1~3
# 沒有數字的話代表， :3 => 0~2， 3: => 3~最後

x = np.array([[3,4],
              [5,6]])

# T: matrix transpose
# 三維 四維 轉至矩陣https://blog.csdn.net/qq_36758914/article/details/105488508
# https://stackoverflow.com/questions/42308270/python-numpy-mgrid-and-reshape
x.T
[[3, 5],
 [4, 6]]

# z.reshape(-1) => -1 代表length of z
# z.reshape(x, y) => 將z reshape 成x * y 的矩陣

```

### python class know how

https://www.796t.com/content/1544582523.html

### MQTT doc

https://mosquitto.org/documentation/

### MQTT example

https://officeguide.cc/python-paho-library-mqtt-client-tutorial-examples/

### undistort function 差異

https://www.jianshu.com/p/6daa8dbbfa30

### cornerSubPix

https://blog.csdn.net/Sunshine_in_Moon/article/details/45440111

### undistort example

https://tw.pythontechworld.com/article/detail/1Yejcu1gNWsC