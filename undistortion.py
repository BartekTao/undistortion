import json
import os
import cv2
import numpy as np
import glob
import main
import file_helper

alpha = 0

def find_points(checker):
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp=np.zeros((checker[0]*checker[1], 3), np.float32)
    objp[:, :2]=np.mgrid[0:checker[0], 0:checker[0]].T.reshape(-1, 2)

    objpoints=[]
    imgpoints=[]
    
    if main.DEBUG:
        images = glob.glob('./img/*.png')
        for fname in images:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, checker, None)
            if ret==True:
                objpoints.append(objp)
                # search winSize = 5*2+1 = 11
                cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), criteria)
                imgpoints.append(corners)
                # img = cv2.drawChessboardCorners(img, checker, corners, ret)
                # cv2.imshow('img',img)
                # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    else:
        # must receive 10 imgs
        for _ in range(10):
            # wait until get next image path
            fullPath = main.imgs_queue.get()
            img = cv2.imread(fullPath)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, checker, None)
            if ret==True:
                objpoints.append(objp)
                # search winSize = 5*2+1 = 11
                cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), criteria)
                imgpoints.append(corners)

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape, None, None)
    main.config['intrinsic']['ks'] = str(mtx.tolist())
    main.config['intrinsic']['dist'] = str(dist.tolist())

    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, img.shape[:2], alpha, img.shape[:2])
    main.config['intrinsic']['newcameramtx'] = str(newcameramtx.tolist())
    
    file_helper.saveConfig()

    return ret, mtx, dist, rvecs, tvecs, newcameramtx

def undistort(imgPath, mtx, dist, newcameramtx):
    img = cv2.imread(imgPath)
    undistortImg = cv2.undistort(img, mtx, dist, None, newcameramtx)
    return undistortImg

def undistortImgs(imgsPath, mtx, dist, newcameramtx):
    images = glob.glob(imgsPath + '/*.png')
    for pname in images:
        img = undistort(pname, mtx, dist, newcameramtx)
        fname = os.path.basename(pname)
        output_name = './undistort_img/D_' + fname
        cv2.imwrite(output_name, img)

if __name__ == '__main__':
    main.DEBUG = True
    ret, mtx, dist, rvecs, tvecs, newcameramtx = find_points(main.patternsize)
    undistortImgs('./img', mtx, dist, newcameramtx)