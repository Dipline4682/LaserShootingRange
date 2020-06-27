import cv2
import numpy as np

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

#temp = cv2.VideoCapture(0)
##-------------функция для сброса флагов(отображения результатов во время игры) --------------------
def sbros(Flag_Sbros_Podschet):
    global i, font, color, dlya_otcheta_v_niz, count
    if Flag_Sbros_Podschet == True:
        i = 0
        color = 0
        dlya_otcheta_v_niz = 0
        count = 0
        Flag_Sbros_Podschet = False
        return Flag_Sbros_Podschet
##--------------------------------------------------------------
def SettingYarkosty(frame, h1, s1, v1, h2, s2, v2):##функция для выделения обьекта(настройка под яркость помещения)
    # преобразуем RGB картинку в HSV модель
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    min = np.array((h1, s1, v1), np.uint8)
    max = np.array((h2, s2, v2), np.uint8)
    mask = cv2.inRange(hsv, min, max)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    return result

def ObnarujenieTochki(bitmask, orig, Lh1, Ls1, Lv1, Lh2, Ls2, Lv2, VerhniqLeviyYgolX, VerhniqLeviyYgolY, NigniyPraviyYgolX, NigniyPraviyYgolY, cap):##Функция засвеченной области
    global i, font, color, dlya_otcheta_v_niz, count
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
                orig = cv2.circle(orig, (cx, cy), 1, (0, 0, 255), 1)
                i = i + 1
                count = count + 1
                dlya_otcheta_v_niz = dlya_otcheta_v_niz + 15
                color = color + 50
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
                
    #result = cv2.bitwise_and(frame, frame, mask=mask)
    return orig