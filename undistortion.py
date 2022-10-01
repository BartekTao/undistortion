import os
import cv2
import numpy as np
import glob
import main
import file_helper

def find_points(checker, imgsPath):
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp=np.zeros((checker[0]*checker[1], 3), np.float32)
    objp[:, :2]=np.mgrid[0:checker[0], 0:checker[0]].T.reshape(-1, 2)

    objpoints=[]
    imgpoints=[]
    
    images = glob.glob(imgsPath + '/*.png')
    for fname in images:
        img = cv2.imread(fname)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, checker, None)
        if ret==True:
            objpoints.append(objp)
            cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners)
            img = cv2.drawChessboardCorners(img, checker, corners, ret)
        # cv2.imshow('img',img)
        # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape, None, None)
    
    main.config['intrinsic']['ks'] = str(mtx.tolist())
    main.config['intrinsic']['dist'] = str(dist.tolist())
    file_helper.saveConfig()

    return ret, mtx, dist, rvecs, tvecs

def undistort(imgPath, mtx, dist, alpha=0):
    img = cv2.imread(imgPath)
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, img.shape[:2], alpha, img.shape[:2])
    undistortImg = cv2.undistort(img, mtx, dist, None, newcameramtx)
    return undistortImg

def undistortImgs(imgsPath, mtx, dist, alpha=0):
    images = glob.glob(imgsPath + '/*.png')
    for pname in images:
        img = undistort(pname, mtx, dist, alpha)
        fname = os.path.basename(pname)
        output_name = './undistort_img/D_' + fname
        cv2.imwrite(output_name, img)

if __name__ == '__main__':
    ret, mtx, dist, rvecs, tvecs = find_points(main.patternsize, "./img")
    undistortImgs('./img', mtx, dist)