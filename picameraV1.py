# import cv2
# cam = cv2.VideoCapture(0)
# while True:
#     ret, img = cam.read()
#     vis = img.copy()
#     cv2.imshow('getCamera', vis)
#     if cv2.waitKey(10) == ord('q'):
#         break
# cv2.destroyAllWindows()

import cv2
import numpy as np
import math
import random

# 校正corners，使得corners點依序從左上->右下
def cornersSort(corners):
    '''
    012
    345
    678
    dx>dy
    x1-x0>0
    y0=y1

    630
    741
    852
    dy>dx
    y1-y0>0
    x0=x1

    876
    543
    210
    dx>dy
    x1-x0<0
    y0=y1

    258
    147
    036
    dy>dx
    y1-y0<0
    x0=x1
    '''
    oldlist = list(corners)  # 把numpy array轉成list
    for i in range(len(oldlist)):
        oldlist[i] = int(oldlist[i][0][0]), int(oldlist[i][0][1])
    newlist = []
    dx = abs(oldlist[1][0] - oldlist[0][0])
    dy = abs(oldlist[1][1] - oldlist[0][1])
    if dx > dy:
        if oldlist[1][0] - oldlist[0][0] > 0:
            for i in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
                newlist.append(corners[i])
            return np.array(newlist)
        elif oldlist[1][0] - oldlist[0][0] < 0:
            for i in [8, 7, 6, 5, 4, 3, 2, 1, 0]:
                newlist.append(corners[i])
            return np.array(newlist)
    elif dx < dy:
        if oldlist[1][1] - oldlist[0][1] > 0:
            for i in [6, 3, 0, 7, 4, 1, 8, 5, 2]:
                newlist.append(corners[i])
            return np.array(newlist)
        elif oldlist[1][1] - oldlist[0][1] < 0:
            for i in [2, 5, 8, 1, 4, 7, 0, 3, 6]:
                newlist.append(corners[i])
            return np.array(newlist)
    print('sort失敗，return原始corners')
    return corners

# cap = cv2.VideoCapture('E:\python-training/rico\覘標正常.mp4')
# cap = cv2.VideoCapture('E:\python-training/rico\覘標全黑.mp4')
# cap = cv2.VideoCapture('E:\python-training/rico\覘標偏暗.mp4')
# cap = cv2.VideoCapture('E:\python-training/rico\覘標rico帥.MOV')
# cap = cv2.VideoCapture('E:\python-training/rico/覘標遮一點.mp4')
# cap = cv2.VideoCapture('E:\python-training/rico/覘標上下左右移動.mp4')
# cap = cv2.VideoCapture('E:\python-training/rico/覘標上下翻轉.mp4')
# cap = cv2.VideoCapture('E:\python-training/rico/覘標天旋地轉.mp4')
# cap = cv2.VideoCapture('E:\python-training/rico/覘標x軸移動50cm.mp4')
# cap = cv2.VideoCapture('E:\python-training/rico/覘標x軸移動40cm.mp4')
# cap = cv2.VideoCapture('E:\python-training/rico/覘標x軸移動有尺01.mp4')
# cap = cv2.VideoCapture('E:\python-training/rico/覘標x軸移動有尺02.mp4')
# cap = cv2.VideoCapture('E:\python-training/rico/覘標x軸移動有尺整整10公分.mp4')
cap = cv2.VideoCapture(0)  # 實時取得鏡頭

isfirstframe = True
firstcenterxy = (0, 0)
xrate, yrate = 0, 0
cblength = 4  # 覘標邊長 4cm * 4cm
while True:
    ret0, frame = cap.read()
    if ret0:
        pass
        # cv2.imshow('video', frame)
        # if cv2.waitKey(1) == ord('q'):
        #     break
        # continue
    else:
        break
    # if cv2.waitKey(10) == ord('q'):  # 若鍵盤按q，則結束
    #     exit()
    patternSize = (3, 3)  # 內部點 3 * 3
    ret1, corners = cv2.findChessboardCorners(frame, patternSize)  # 找角點

    if ret1:
        # 有找到corners角點就校正，使得corners點依序從左上->右下
        corners = cornersSort(corners)

        # -----------
        cornersxy = list(corners)
        for i in range(len(cornersxy)):
            cornersxy[i] = int(cornersxy[i][0][0]), int(cornersxy[i][0][1])
        # print(cornersxy)  # [(225, 233), (273, 232), (320, 230), (228, 280), (274, 279), (320, 278), (230, 326), (275, 324), (321, 323)]

        if isfirstframe:
            firstcenterxy = cornersxy[4]  # 取得偵測到的第一幀的圓心座標
            isfirstframe = False
            # xrate = cblength / ((abs(cornersxy[2][0] - cornersxy[0][0]) + abs(cornersxy[8][0] - cornersxy[6][0])) / 2)  # x軸每像素為xrate公分 這樣是錯的 要乘上cos
            # yrate = cblength / ((abs(cornersxy[6][1] - cornersxy[0][1]) + abs(cornersxy[8][1] - cornersxy[2][1])) / 2)  # y軸每像素為yrate公分 這樣是錯的 要乘上sin
            px35x, px35y = abs(cornersxy[5][0] - cornersxy[3][0]), abs(cornersxy[5][1] - cornersxy[3][1])  # 計算第3&5點之間的xy各有多少像素
            anglex = math.atan(px35y / px35x) if px35x != 0 else math.pi / 2  # 計算第3&5點連線離x軸的傾斜角度
            xlength = cblength * math.cos(anglex)  # 計算第3&5點之間的實際水平距離(cm)

            px17x, px17y = abs(cornersxy[7][0] - cornersxy[1][0]), abs(cornersxy[7][1] - cornersxy[1][1])  # 計算第1&7點之間的xy各有多少像素
            angley = math.atan(px17y / px17x) if px17x != 0 else math.pi / 2  # 計算第1&7點連線離y軸的傾斜角度
            ylength = cblength * math.sin(angley)  # 計算第1&7點之間的實際鉛直距離(cm)

            xrate = xlength / px35x  # x軸每像素為xrate公分
            yrate = ylength / px17y  # y軸每像素為yrate公分
            print(f'xrate: {xrate} cm')
            print(f'yrate: {yrate} cm')

        paint = cv2.drawChessboardCorners(image=frame, corners=corners, patternSize=patternSize, patternWasFound=ret1)  # 把角點圈出來
        cv2.circle(frame, cornersxy[4], 10, (0, 0, 250), 2)  # 中心點圈起來
        cv2.line(frame, cornersxy[0], cornersxy[2], (0, 250, 0), 2)  # 四個角點連線
        cv2.line(frame, cornersxy[0], cornersxy[6], (0, 250, 0), 2)
        cv2.line(frame, cornersxy[8], cornersxy[2], (0, 250, 0), 2)
        cv2.line(frame, cornersxy[8], cornersxy[6], (0, 250, 0), 2)
        font = cv2.FONT_HERSHEY_TRIPLEX  # 設置字體
        cv2.putText(frame, "Deformation (x,y,z) cm= ", (20, 360), font, 1, (0, 0, 250))  # 顯示文字在圖上
        cv2.putText(frame, f'{((cornersxy[4][0] - firstcenterxy[0]) * xrate):7.2f}', (20, 400), font, 1, (0, 0, 250))
        cv2.putText(frame, f'{((cornersxy[4][1] - firstcenterxy[1]) * yrate):7.2f}', (140, 400), font, 1, (0, 0, 250))
        cv2.putText(frame, 'None', (280, 400), font, 1, (0, 0, 250))
        # -----------
    else:
        # 沒找到corners角點就continue
        print(f'{random.randint(1, 100)}有畫面，但沒找到覘標！')
        # continue
    cv2.imshow('video', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows()
