import unittest

import cv2
import numpy as np
import main
import undistortion

class Test_find_points(unittest.TestCase):
    def setUp(self):
        self.ks = [[678.5387178062471, 0.0, 410.9027884589412], [0.0, 678.5882606360775, 294.304178000495], [0.0, 0.0, 1.0]]
        self.dist = [[-0.5262013660764194, 0.5014531101663418, 1.8268674016352275e-06, -0.002115787783761801, -0.6426896902184697]]
        self.newcameramtx = [[677.4078369140625, 0.0, 410.2179569441432], [0.0, 677.7400512695312, 293.93630139720153], [0.0, 0.0, 1.0]]

    def test_find_points(self):
        main.DEBUG = True
        ret, mtx, dist, rvecs, tvecs, newcameramtx = undistortion.find_points(main.patternsize)
        self.assertTrue((mtx == self.ks).all())
        self.assertTrue((dist == self.dist).all())
        self.assertTrue((newcameramtx == self.newcameramtx).all())

class TestUndistortion(unittest.TestCase):
    def setUp(self):
        self.ks = np.array([[678.5387178062471, 0.0, 410.9027884589412], [0.0, 678.5882606360775, 294.304178000495], [0.0, 0.0, 1.0]])
        self.dist = np.array([[-0.5262013660764194, 0.5014531101663418, 1.8268674016352275e-06, -0.002115787783761801, -0.6426896902184697]])
        self.newcameramtx = np.array([[677.4078369140625, 0.0, 410.2179569441432], [0.0, 677.7400512695312, 293.93630139720153], [0.0, 0.0, 1.0]])
    def test_undistortion(self):
        img = undistortion.undistort('./test/2022-09-29_20-53-00_0.png', self.ks, self.dist, self.newcameramtx)
        undistortImg = cv2.imread('./test/D_2022-09-29_20-53-00_0.png')
        self.assertTrue((img == np.array(undistortImg)).all())