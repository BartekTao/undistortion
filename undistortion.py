import os
import cv2
import numpy as np
import glob
import main
import file_helper

alpha = 0

def find_points(checker):
    objp=np.zeros((checker[0]*checker[1], 3), np.float32)
    objp[:, :2]=np.mgrid[0:checker[0], 0:checker[0]].T.reshape(-1, 2)

    objpoints=[]
    imgpoints=[]
    
    if main.DEBUG:
        images = glob.glob('./img/*.png')
        for fname in images:
            img = cv2.imread(fname)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(img, checker, None)
            if ret==True:
                objpoints.append(objp)
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

            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(img, checker, None)
            if ret==True:
                objpoints.append(objp)
                imgpoints.append(corners)
    # mtx：相機內參；dist：畸變係數；revcs：旋轉矩陣；tvecs：平移向量
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img.shape, None, None)
    main.config['intrinsic']['ks'] = str(mtx.tolist())
    main.config['intrinsic']['dist'] = str(dist.tolist())
    main.config['intrinsic']['rvecs'] = str(dist.tolist())
    main.config['intrinsic']['tvecs'] = str(dist.tolist())

    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, img.shape, alpha, img.shape)
    main.config['intrinsic']['newcameramtx'] = str(newcameramtx.tolist())
    
    file_helper.saveConfig(main.config)

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

