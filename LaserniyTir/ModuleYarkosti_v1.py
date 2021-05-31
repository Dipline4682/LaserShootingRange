import cv2
import numpy as np

def nothing(*arg):
        pass
##----------------функция для вырезки выделенной области---------------- 
def cut(img, VerhniqLeviyYgolX, VerhniqLeviyYgolY, NigniyPraviyYgolX, NigniyPraviyYgolY):
    #print('***', img.shape)
    x = VerhniqLeviyYgolX
    x1 = VerhniqLeviyYgolX+NigniyPraviyYgolX-VerhniqLeviyYgolX
    y = VerhniqLeviyYgolY
    y1 = VerhniqLeviyYgolY+NigniyPraviyYgolY-VerhniqLeviyYgolY
    img1 = img[y:y1, x:x1] #y - откуда; y1 - Сколько пикселей; x - откуда; x1 - сколько пикселей
    return img1
##-------------------------------------------------------------

font = cv2.FONT_HERSHEY_SIMPLEX ## Шрифт для вывода текста
i = 0
color = 0
dlya_otcheta_v_niz = 0
count = 0
kernel = np.ones((3,3),np.uint8)
summa = 0
Kol_Vistrelow = 8
#temp = cv2.VideoCapture(0)
##=================Отрисовка подсчёта результата выстрелов=============
###-----для настройки-----------------------------------
next_back = 0
def setSettings_Window_misheny(val):
    global Kol_Vistrelow
    Kol_Vistrelow = val
###----------------------------------------------------


#####====================================ФУНКЦИЯ АВТОПОДСЧЁТА============================================
def Show_Podschet(orig, Auto_Podschet_WindowGame, ASh1, ASs1, cx, cy, dlya_otcheta_v_niz, i):#, ASv1, ASh2, ASs2, ASv2, cx, cy):
    global summa
    r, c, g = Auto_Podschet_WindowGame.shape
    #aaaa = Auto_Podschet_WindowGame
    #hsv = cv2.cvtColor(Auto_Podschet_WindowGame.copy(), cv2.COLOR_BGR2RGB)
    #hsv = cv2.cvtColor(Auto_Podschet_WindowGame.copy(), cv2.COLOR_BGR2HSV)
    #blur = cv2.GaussianBlur(hsv,(5,5),0)
    #min = np.array((ASh1, ASs1, ASv1), np.uint8)
    #max = np.array((ASh2, ASs2, ASv2), np.uint8)
    #mask = cv2.inRange(blur, min, max)
    #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    hsv = cv2.cvtColor(Auto_Podschet_WindowGame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(hsv,(3,3),0)
    mask = cv2.Canny(blur,ASh1,ASs1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #print(len(contours))
    if len(contours) > 0:
        #aaaa = orig = cv2.drawContours(aaaa, contours, -1, (0,255,0), 2)
        #cv2.imshow('aaaa', aaaa)
        for contour in contours:
        #for idx, contour in enumerate(contours): ##-----Проходимся по списку контуров
            area = cv2.contourArea(contour)
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
            #print('area',area)
            #print('approx',len(approx))
            if (len(approx) > 12) and (300 < area < 30000):
                #test = cv2.drawContours(orig, contours, -1, (0,255,0), 1)
                #cv2.imshow('test', test)
                #dist = cv2.pointPolygonTest(cnt,(cx,cy),True)
                #if i == 16:
                    #cv2.rectangle(orig,(c-100, r-10),(c-80,r),(0,0,0),-1)
                    #cv2.putText(orig, str(summa),(c-98, r-3), font, 0.2,(255,150,50),1,cv2.LINE_AA)
                if ((cv2.pointPolygonTest(contours[1],(cx,cy),True) < 0)):# or (cv2.pointPolygonTest(contours[2],(cx,cy),True) < 0)):# and (idx == 1 or idx == 2):
                    cv2.rectangle(orig,(c-12, dlya_otcheta_v_niz),(c,dlya_otcheta_v_niz+10),(0,0,0),-1)
                    cv2.putText(orig, '0',(c-10, dlya_otcheta_v_niz+7), font, 0.2,(255,150,50),1,cv2.LINE_AA)
                    if i == Kol_Vistrelow:
                        cv2.rectangle(orig,(c-100, r-10),(c-80,r),(0,0,0),-1)
                        cv2.putText(orig, str(summa),(c-98, r-3), font, 0.2,(255,150,50),1,cv2.LINE_AA)
                    #print('NET')
                    return orig
                elif ((cv2.pointPolygonTest(contours[3],(cx,cy),True) < 0)):
                    summa = summa + 2
                    cv2.rectangle(orig,(c-12, dlya_otcheta_v_niz),(c,dlya_otcheta_v_niz+10),(0,0,0),-1)
                    cv2.putText(orig, '2',(c-10, dlya_otcheta_v_niz+7), font, 0.2,(255,150,50),1,cv2.LINE_AA)
                    if i == Kol_Vistrelow:
                        cv2.rectangle(orig,(c-100, r-10),(c-80,r),(0,0,0),-1)
                        cv2.putText(orig, str(summa),(c-98, r-3), font, 0.2,(255,150,50),1,cv2.LINE_AA)
                    #print('popal v 2')
                    return orig
                elif ((cv2.pointPolygonTest(contours[5],(cx,cy),True) < 0)):
                    summa = summa + 3
                    cv2.rectangle(orig,(c-12, dlya_otcheta_v_niz),(c,dlya_otcheta_v_niz+10),(0,0,0),-1)
                    cv2.putText(orig, '3',(c-10, dlya_otcheta_v_niz+7), font, 0.2,(255,150,50),1,cv2.LINE_AA)
                    if i == Kol_Vistrelow:
                        cv2.rectangle(orig,(c-100, r-10),(c-80,r),(0,0,0),-1)
                        cv2.putText(orig, str(summa),(c-98, r-3), font, 0.2,(255,150,50),1,cv2.LINE_AA)
                    #print('popal v 3')
                    return orig
                elif ((cv2.pointPolygonTest(contours[7],(cx,cy),True) < 0)):
                    summa = summa + 4
                    cv2.rectangle(orig,(c-12, dlya_otcheta_v_niz),(c,dlya_otcheta_v_niz+10),(0,0,0),-1)
                    cv2.putText(orig, '4',(c-10, dlya_otcheta_v_niz+7), font, 0.2,(255,150,50),1,cv2.LINE_AA)
                    if i == Kol_Vistrelow:
                        cv2.rectangle(orig,(c-100, r-10),(c-80,r),(0,0,0),-1)
                        cv2.putText(orig, str(summa),(c-98, r-3), font, 0.2,(255,150,50),1,cv2.LINE_AA)
                    #print('popal v 4')
                    return orig
                elif ((cv2.pointPolygonTest(contours[9],(cx,cy),True) < 0)):
                    summa = summa + 5
                    cv2.rectangle(orig,(c-12, dlya_otcheta_v_niz),(c,dlya_otcheta_v_niz+10),(0,0,0),-1)
                    cv2.putText(orig, '5',(c-10, dlya_otcheta_v_niz+7), font, 0.2,(255,150,50),1,cv2.LINE_AA)
                    if i == Kol_Vistrelow:
                        cv2.rectangle(orig,(c-100, r-10),(c-80,r),(0,0,0),-1)
                        cv2.putText(orig, str(summa),(c-98, r-3), font, 0.2,(255,150,50),1,cv2.LINE_AA)
                    #print('popal v 5')
                    return orig
                elif ((cv2.pointPolygonTest(contours[11],(cx,cy),True) < 0)):
                    summa = summa + 6
                    cv2.rectangle(orig,(c-12, dlya_otcheta_v_niz),(c,dlya_otcheta_v_niz+10),(0,0,0),-1)
                    cv2.putText(orig, '6',(c-10, dlya_otcheta_v_niz+7), font, 0.2,(255,150,50),1,cv2.LINE_AA)
                    if i == Kol_Vistrelow:
                        cv2.rectangle(orig,(c-100, r-10),(c-80,r),(0,0,0),-1)
                        cv2.putText(orig, str(summa),(c-98, r-3), font, 0.2,(255,150,50),1,cv2.LINE_AA)
                    #print('popal v 6')
                    return orig
                elif ((cv2.pointPolygonTest(contours[13],(cx,cy),True) < 0)):
                    summa = summa + 7
                    cv2.rectangle(orig,(c-12, dlya_otcheta_v_niz),(c,dlya_otcheta_v_niz+10),(0,0,0),-1)
                    cv2.putText(orig, '7',(c-10, dlya_otcheta_v_niz+7), font, 0.2,(255,150,50),1,cv2.LINE_AA)
                    if i == Kol_Vistrelow:
                        cv2.rectangle(orig,(c-100, r-10),(c-80,r),(0,0,0),-1)
                        cv2.putText(orig, str(summa),(c-98, r-3), font, 0.2,(255,150,50),1,cv2.LINE_AA)
                    #print('popal v 7')
                    return orig
                elif ((cv2.pointPolygonTest(contours[15],(cx,cy),True) < 0)):
                    summa = summa + 8
                    cv2.rectangle(orig,(c-12, dlya_otcheta_v_niz),(c,dlya_otcheta_v_niz+10),(0,0,0),-1)
                    cv2.putText(orig, '8',(c-10, dlya_otcheta_v_niz+7), font, 0.2,(255,150,50),1,cv2.LINE_AA)
                    if i == Kol_Vistrelow:
                        cv2.rectangle(orig,(c-100, r-10),(c-80,r),(0,0,0),-1)
                        cv2.putText(orig, str(summa),(c-98, r-3), font, 0.2,(255,150,50),1,cv2.LINE_AA)
                    #print('popal v 8')
                    return orig
                elif ((cv2.pointPolygonTest(contours[16],(cx,cy),True) <= 0)):
                    summa = summa + 9
                    cv2.rectangle(orig,(c-12, dlya_otcheta_v_niz),(c,dlya_otcheta_v_niz+10),(0,0,0),-1)
                    cv2.putText(orig, '9',(c-10, dlya_otcheta_v_niz+7), font, 0.2,(255,150,50),1,cv2.LINE_AA)
                    if i == Kol_Vistrelow:
                        cv2.rectangle(orig,(c-100, r-10),(c-80,r),(0,0,0),-1)
                        cv2.putText(orig, str(summa),(c-98, r-3), font, 0.2,(255,150,50),1,cv2.LINE_AA)
                    #print('popal v 9')
                    return orig
                else:#if ((cv2.pointPolygonTest(contours[17],(cx,cy),True) > 0)):
                    summa = summa + 10
                    cv2.rectangle(orig,(c-12, dlya_otcheta_v_niz),(c,dlya_otcheta_v_niz+10),(0,0,0),-1)
                    cv2.putText(orig, '10',(c-12, dlya_otcheta_v_niz+7), font, 0.2,(255,150,50),1,cv2.LINE_AA)
                    if i == Kol_Vistrelow:
                        cv2.rectangle(orig,(c-100, r-10),(c-80,r),(0,0,0),-1)
                        cv2.putText(orig, str(summa),(c-98, r-3), font, 0.2,(255,150,50),1,cv2.LINE_AA)
                    #print('popal v 10')
                    return orig
    return orig
###=============================================================================================================   
###==================================для окна настройки балов=================================================
def Setting_Show_Podschet(orig, ASh1, ASs1, ASv1):#, ASh2, ASs2, ASv2):#, Fair_X, Fair_Y, h1, s1, v1, h2, s2, v2):
    global idx, i
    reta = orig
    #hsv = cv2.cvtColor(orig, cv2.COLOR_BGR2RGB)
    #hsv = cv2.cvtColor(orig, cv2.COLOR_BGR2HSV)
    hsv = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(hsv,(3,3),0)
    mask = cv2.Canny(blur,ASh1,ASs1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    #mask = cv2.Canny(hsv,ASh1,ASs1)
    #min = np.array((ASh1, ASs1, ASv1), np.uint8)
    #max = np.array((ASh2, ASs2, ASv2), np.uint8)
    #mask = cv2.inRange(blur, min, max)
    #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    kontur = len(contours)
    #print(len(contours))
    if len(contours) > 0:
        for cnt in contours:
        #for idx, cnt in enumerate(contours): ##-----Проходимся по списку контуров
            area = cv2.contourArea(cnt)
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            #print(cnt)
            if (len(approx) > 15) and (300 < area < 30000):
                #dist = cv2.pointPolygonTest(cnt,(100,100),False)
                if ASv1 < len(contours):
                    orig = cv2.drawContours(orig, contours[ASv1], -1, (0,255,0), 1)
                #orig = cv2.drawContours(orig, contours, -1, (0,255,0), 2)
                    cv2.imshow('orig', orig)
    cv2.imshow('mask', mask)
    return kontur
##=====================================================================


##-------------функция для сброса флагов(отображения результатов во время игры) --------------------
Flag_sbros_dlya_modulya = False
def sbros(Flag_Sbros_Podschet):
    global i, font, color, dlya_otcheta_v_niz, count, Flag_sbros_dlya_modulya, summa
    if Flag_Sbros_Podschet == True:
        i = 0
        color = 0
        dlya_otcheta_v_niz = 0
        count = 0
        summa = 0
        Flag_Sbros_Podschet = False
        return Flag_Sbros_Podschet
##--------------------------------------------------------------

def SettingYarkosty(frame, h1, s1, v1, h2, s2, v2):##функция для выделения обьекта(настройка под яркость помещения)
    # преобразуем RGB картинку в HSV модель
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    min = np.array((h1, s1, v1), np.uint8)
    max = np.array((h2, s2, v2), np.uint8)
    mask = cv2.inRange(hsv, min, max)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    #ret,result = cv2.threshold(result,127,255,cv2.THRESH_BINARY)
    return result

def ObnarujenieTochki(bitmask, orig, Lh1, Ls1, Lv1, Lh2, Ls2, Lv2, VerhniqLeviyYgolX, VerhniqLeviyYgolY, NigniyPraviyYgolX, NigniyPraviyYgolY, cap, Auto_Podschet_WindowGame,  ASh1, ASs1):#, ASv1, ASh2, ASs2, ASv2):##Функция засвеченной области
    global i, font, color, dlya_otcheta_v_niz, count, Kordinadi_vistrela
    ## Где bitmask - изображение где ищем засвеченую область;
    ## orig - оригинальное изображение куда будет наносится результат выстрела и потом возвращаться;
    ## Lh1, Ls1, Lv1, Lh2, Ls2, Lv2 - значения для фиьльтрации
    # преобразуем RGB картинку в HSV модель
    hsv = cv2.cvtColor(bitmask, cv2.COLOR_BGR2RGB)
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    min = np.array((Lh1, Ls1, Lv1), np.uint8)
    #min = np.array((255, 0, 150), np.uint8)
    max = np.array((Lh2, Ls2, Lv2), np.uint8)
    mask = cv2.inRange(hsv, min, max)
    #cv2.imshow('test', mask)
    ##-----------Поиск контуров--------------------------------------------------------------------
    contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    ##---------------------------------------------------------------------------------------------
    ##-----------Проверяем на то есть ли контуры в списке------------
    if len(contours) > 0:
        for idx, cnt in enumerate(contours): ##-----Проходимся по списку контуров
            x,y,w,h = cv2.boundingRect(cnt) ##-----Находим граничащие точки контура
            #----------Моменты (нахождение центроида площади и тд) рисуем центроид точки лазера------------
            M = cv2.moments(cnt)
            if M['m00'] > 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                if i < Kol_Vistrelow:
                    orig = cv2.circle(orig, (cx, cy), 1, (0, 0, 255), 1)
                    #Kordinadi_vistrela[0] = cx
                    #Kordinadi_vistrela[1] = cy
                    
                    #Show_Podschet(orig)
                    #WindowGameNoLine = cv2.circle(WindowGameNoLine, (cx, cy), 1, (0, 0, 255), 1)
                    i = i + 1
                    orig = Show_Podschet(orig, Auto_Podschet_WindowGame.copy(), ASh1, ASs1, cx, cy, dlya_otcheta_v_niz, i)#, ASv1, ASh2, ASs2, ASv2, cx, cy)
                    count = count + 1
                    dlya_otcheta_v_niz = dlya_otcheta_v_niz + 15
                    color = color + 50
                    ##if Flag_Show_Line == False:
                    if count == 1: ## B = Синий цвет отрисовки
                        #orig = cv2.circle(orig, (cx, cy), 1, (0, 0, 255), 1)
                        if color > 250:
                            color = 0
                        orig = cv2.line(orig,(2,dlya_otcheta_v_niz),(cx,cy),(color,0,0),1)
                        cv2.putText(orig, str(i),(2, dlya_otcheta_v_niz), font, 0.2,(color,0,0),1,cv2.LINE_AA)
                        count = 2
                    elif count == 2: ## G = Зелёный цвет отрисовки
                        if color > 250:
                            color = 0
                        orig = cv2.line(orig,(2,dlya_otcheta_v_niz),(cx,cy),(0,color,0),1)
                        cv2.putText(orig, str(i),(2, dlya_otcheta_v_niz), font, 0.2,(0,color,0),1,cv2.LINE_AA)
                        count = 3
                    elif count == 3:## R = Красный цвет отрисовки
                        if color > 250:
                            color = 0
                        orig = cv2.line(orig,(2,dlya_otcheta_v_niz),(cx,cy),(0,0,color),1)
                        cv2.putText(orig, str(i),(2, dlya_otcheta_v_niz), font, 0.2,(0,0,color),1,cv2.LINE_AA)
                        count = 0

                    j = 0 ##переменная для выхода из цыкла которая позволит поределить выбрасывать в меню или нет
                    while True:##цикл для того что бы убрать дребезг или повторный выстрел
                        #temp = cv2.VideoCapture(0)
                        __, img = cap.read()
                        img = cut(img, VerhniqLeviyYgolX, VerhniqLeviyYgolY, NigniyPraviyYgolX, NigniyPraviyYgolY)
                        hsvv = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        minn = np.array((Lh1, Ls1, Lv1), np.uint8)
                        maxx = np.array((Lh2, Ls2, Lv2), np.uint8)
                        maskk = cv2.inRange(hsvv, minn, maxx)
                        contourss, hierarchyy = cv2.findContours(maskk, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                        j = j + 1
                        if len(contourss) < 1 or j > 20:
                            #temp.release()
                            break
    #print(len(mas))
    #print(WindowGameNoLine)
    #cv2.imshow("WindowGameNoLine", WindowGameNoLine)
    #cv2.imshow("orig", orig)
    #result = cv2.bitwise_and(frame, frame, mask=mask)
    return orig #[WindowGameNoLine, orig]
