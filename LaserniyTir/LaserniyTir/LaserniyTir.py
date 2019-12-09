import cv2
import numpy as np
import time

if __name__ == '__main__':
    def nothing(*arg):
        pass

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
frame = cv2.resize(frame, (1440, 900))

kernel = np.ones((5,5),np.uint8)
img = frame.copy()
mode = 0
modeopenclose = 0
while True:
    if mode == 0:
        ret, frame = cap.read()
        cv2.imshow('Camera Position Adjustment Mode', frame)
    else:
        ret, frame = cap.read()
        CopFrame = frame.copy()
        frame = cv2.resize(frame, (1440, 900))
        h1 = cv2.getTrackbarPos('h1', 'Settings')
        s1 = cv2.getTrackbarPos('s1', 'Settings')
        v1 = cv2.getTrackbarPos('v1', 'Settings')

        h2 = cv2.getTrackbarPos('h2', 'Settings')
        s2 = cv2.getTrackbarPos('s2', 'Settings')
        v2 = cv2.getTrackbarPos('v2', 'Settings')

        #min = np.array((h1, s1, v1), np.uint8)
        min = np.array((165, 144, 204), np.uint8)
        #max = np.array((h2, s2, v2), np.uint8)
        max = np.array((237, 172, 255), np.uint8)
        Copfilter = cv2.inRange(CopFrame, min, max)
        filter = cv2.inRange(frame, min, max)
        dilation = cv2.dilate(filter,kernel,iterations = 2)
        #-----------Поиск контуров--------------------------------------------------------------------
        contours, hierarchy = cv2.findContours(dilation.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #contours, hierarchy = cv2.findContours(threshold.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #---------------------------------------------------------------------------------------------
        if len(contours) > 0:
            for idx, cnt in enumerate(contours):
                x,y,w,h = cv2.boundingRect(cnt)
                #img = cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                #----------Моменты (нахождение центроида площади и тд)------------
                M = cv2.moments(cnt)
                if M['m00'] > 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    img = cv2.circle(img, (cx, cy), 3, (0, 0, 255), 1)
                    #c, r, d = img.shape
                    #print(c)
                    #print(r)
                    #img = cv2.rectangle(img, (r//2-200,c//2-250), (r//2+200,c//2+250), (0,255,0), 2)
                    time.sleep(1/1)
                #-----------------------------------------------------------------
                #print('yes')
                if modeopenclose == 1:
                    cv2.imshow('Settings',Copfilter)
                    cv2.imshow('frame', CopFrame)
                cv2.imshow('open session', img)
        else:
            #print('no')
            if modeopenclose == 1:
                cv2.imshow('Settings',Copfilter)
                cv2.imshow('frame', CopFrame)
            cv2.imshow('open session', img)

    key = cv2.waitKey(5) & 0xFF
    #cv2.imshow('frame', frame)
    if key == ord('q'): break #Выход
    elif key == ord('m'): #Переключение режимов
        if mode == 0:
            mode = 1
            cv2.destroyAllWindows()
        else:
            mode = 0
            cv2.destroyAllWindows()
    elif key == ord('r'): img = frame.copy() #Сброс результата
    elif key == ord('c'): #Закрытие и открытие отладочных окон в режиме игры
        if modeopenclose == 0:
            modeopenclose = 1
            cv2.destroyAllWindows()
            cv2.namedWindow("Settings") #cv2.WINDOW_NORMAL cv2.WINDOW_AUTOSIZE
            cv2.createTrackbar('h1', 'Settings', 255, 255, nothing)
            cv2.createTrackbar('s1', 'Settings', 255, 255, nothing)
            cv2.createTrackbar('v1', 'Settings', 255, 255, nothing)
 
            cv2.createTrackbar('h2', 'Settings', 255, 255, nothing)
            cv2.createTrackbar('s2', 'Settings', 255, 255, nothing)
            cv2.createTrackbar('v2', 'Settings', 255, 255, nothing)
        else:
            modeopenclose = 0
            cv2.destroyAllWindows()
            
    elif key == ord('s'): cv2.imwrite('Resultat.png', img) #Сохранение результата

cap.release()
cv2.destroyAllWindows()