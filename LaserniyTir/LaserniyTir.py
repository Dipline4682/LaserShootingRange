###ಠ_ಠ = 4
###print(ಠ_ಠ)
import cv2
import numpy as np
import math
import time
import ModuleYarkosti as MY

if __name__ == '__main__':
    def nothing(*arg):
        pass

##----Изменение размера с сохранением соотношения сторон-----
scale_percent = 500 # Процент от изначального размера
def SizeImg (IMAGES):
    width = int(IMAGES.shape[1] * scale_percent / 100)
    height = int(IMAGES.shape[0] * scale_percent / 100)
    dim = (width, height)
    TargetSizeImage = cv2.resize(IMAGES, dim, interpolation = cv2.INTER_AREA)
    return TargetSizeImage
##---------------------------------------------------------------

####--------------------ОБЩИЕ ПЕРЕМЕННЫЕ------------------------
font = cv2.FONT_HERSHEY_SIMPLEX ## Шрифт для вывода текста
BitMaska = 0 ##Переменная с которой будем вырезать засвеченный лазер
Resultat_Otstrela_Flag = False##Переменная для переключения режима во время игры что бы просмотреть результат
Copy_Bit_Maska_Resize = 0 ## Увеличенное игровое окно
Exit = False ## переменная для кнопки выхода
####---------------------------------------------------

####-------------------- ПЕРЕМЕННЫЕ ФЛАГИ ДЛЯ МОДУЛЬНОЙ ФУНКЦИИ----------------
#Flag_Show_Line = False
Flag_Sbros_Podschet = False ## Сброс для подсчёта попаданий(то что отображает номер выстрела)

####---------------------------------------------------

###-----------------------ПЕРЕМЕННыЕ ДЛЯ КНОПОК----------------------
ModFps = False ## Включить выключить ФПС(изначально выкл)
## Переменные для выбора мешени
ModViborMisheni = 0 ## Переменная для выбора мешени(4 режима)0-двойное нажатие на старт 1 - Выбераем верхний угол 2 - Выбераем правый угол 3 - соглашаемся и начинаем играть или отменяем
step = 0
VerhniqLeviyYgolX = 0
VerhniqLeviyYgolY = 0
NigniyPraviyYgolX = 0
NigniyPraviyYgolY = 0
## Переменные для переключения окна настройки
ModSettings = False
h1 = 0
h2 = 255
s1 = 0 
s2 = 255
v1 = 0
v2 = 255
Lh1 = 0
Lh2 = 255
Ls1 = 0 
Ls2 = 255
Lv1 = 0
Lv2 = 255
## Переманные для того что бы узнать размеры верезанного обьекта и создать новое окно
WindowGame = np.zeros((0,0,3), np.uint8) ## Создаём новое окно для игры.(что бы вставить туда вырезенный обьект)
WGRow, WGCol, WGChsnel = 0, 0, 0
## Переключение ползунков hsv / Lazer в окне настройки
Mod_HSV_Lazer = False
##------------------------------------------------------------------

##------------Создание главного окна для отрисовки интерфейса-----------
def INTERFEYS(frames):
    Iterfeys = frames  ##Присваиваем переменной интерфейс кадр что бы потом можно было обработать информацию с фрейм
    #GloalWindow = np.zeros((480,640,3), np.uint8)
    ##рисуем кнопку FPS
    cv2.rectangle(Iterfeys,(540, 0),(640,480),(0,0,0),-1)
    cv2.rectangle(Iterfeys,(540, 0),(640,40),(0,255,0),2)
    cv2.putText(Iterfeys, 'IPS: on/off',(542, 23), font, 0.5,(0,255,0),2,cv2.LINE_AA)
    ##рисуем кнопку выделения мишение
    cv2.rectangle(Iterfeys,(540, 45),(640,85),(0,255,0),2)##по х = 540 y = 45 (нижний угол х = 640 у = 85)
    cv2.putText(Iterfeys, 'Start',(572, 70), font, 0.6,(0,255,0),2,cv2.LINE_AA)
    ## Кнопка настроек
    #cv2.rectangle(Iterfeys,(540, 90),(640,130),(255,0,0),2)
    #cv2.putText(Iterfeys, 'Settings',(555, 116), font, 0.6,(255,0,0),1,cv2.LINE_AA)
    ## Кнопка Выхода
    cv2.rectangle(Iterfeys,(540, 135),(640,175),(0,255,0),2)
    cv2.putText(Iterfeys, 'Exit',(574, 161), font, 0.6,(0,255,0),2,cv2.LINE_AA)
    return Iterfeys
##------------------------------------------

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

##----------------функция обратного вызова мыши---------------- 
def OneKlik(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:##Двойной щелчок ЛКМ
        global ModFps, ModViborMisheni, VerhniqLeviyYgolX, VerhniqLeviyYgolY ##обязательно обьявляем переменные как глобальные или не будут работать
        global NigniyPraviyYgolX, NigniyPraviyYgolY, ModSettings, h1, h2, s1, s2, v1, v2, WindowGame, Mod_HSV_Lazer
        global Lh1, Lh2, Ls1, Ls2, Lv1, Lv2, WGRow, WGCol, WGChsnel, Exit, Flag_Sbros_Podschet
        ###---------------------Кнопка ФПС----------------------------------------------------
        if ((y > 0) and (y < 40)) and ((x > 540) and (x < 640)) and ModSettings == False: ## область кнопки ФПС
            if ModFps == False: ModFps = True
            else: ModFps = False
        ###------------------------------------------------------------------------------------
        ###---------------------КНОПКА СТАРТ------------------------------------------------------
        elif ((y > 45) and (y < 85)) and ((x > 540) and (x < 640)) and ModSettings == False: ## область кнопки старт
            if ModViborMisheni == 0:
                ModViborMisheni = 1 ## Включён выбор верхнего левого угла
            elif ModViborMisheni == 3: ## Последний шаг когда нажата кнопка старт включает режим игры 
                ##(Здесь пишем код связыный с повторным нажатием кнопки старт)
                cv2.destroyAllWindows() ## убераем окно
                Flag_Sbros_Podschet = True
                Flag_Sbros_Podschet = MY.sbros(Flag_Sbros_Podschet)
                ##-----Вырезаем изображение и присваеваем его глобальной переменной в новое окно----------------
                carved = cut(frame, VerhniqLeviyYgolX, VerhniqLeviyYgolY, NigniyPraviyYgolX, NigniyPraviyYgolY)
                WGRow, WGCol, WGChsnel = carved.shape
                WindowGame = np.zeros((WGRow,WGCol,3), np.uint8) ## Создаём новое окно для игры.(что бы вставить туда вырезенный обьект)
                WindowGame = carved
                ##-----------------------------------------------------------------------------------
                #cv2.imshow('asd', WindowGame)
                ModViborMisheni = -1

        ## Присваиваем переменным кординаты угла
        elif ModViborMisheni == 1 and (x < 540): 
            ## Присваивание переменной кординаты верхнего левого угла
            VerhniqLeviyYgolX = x
            VerhniqLeviyYgolY = y
            ModViborMisheni = 2 ## Включён выбор нижнего правого угла
        elif ModViborMisheni == 2 and (x < 540):
            ## Присваивание переменной кординаты нижнего правого угла
            NigniyPraviyYgolX = x
            NigniyPraviyYgolY = y
            ## Проверка на то что углы были выбраны правильно
            if (VerhniqLeviyYgolX > NigniyPraviyYgolX) or (VerhniqLeviyYgolY > NigniyPraviyYgolY):
                ModViborMisheni = 1
            else: ModViborMisheni = 3
        ## Кнопка отмены
        elif ((y > 45) and (y < 85)) and ((x > 0) and (x < 100)) and ModViborMisheni == 3:
            ModViborMisheni = 0
        ##---------------------------------------------------------------------------------------------
        ###---------------------Кнопка настроек----------------------------------------------------
        elif ((y > 90) and (y < 130)) and ((x > 540) and (x < 640)): ## область кнопки настроек
            if ModSettings == False:
                cv2.destroyAllWindows()
                cv2.namedWindow("Settings") ## Создаём окно настройки с ползунками
                ## ПОЛЗУНКИ ДЛЯ НАСТРОКИ ЯРКОСТИ
                cv2.createTrackbar('h1', 'Settings', h1, 255, nothing)
                cv2.createTrackbar('s1', 'Settings', s1, 255, nothing)
                cv2.createTrackbar('v1', 'Settings', v1, 255, nothing)
                cv2.createTrackbar('h2', 'Settings', h2, 255, nothing)
                cv2.createTrackbar('s2', 'Settings', s2, 255, nothing)
                cv2.createTrackbar('v2', 'Settings', v2, 255, nothing)
                
                ModSettings = True
            else:
                cv2.destroyAllWindows()
                ModSettings = False
            
        elif (((y > 0) and (y < 85)) and ((x > 540) and (x < 640))) and (ModSettings == True): ## область кнопки hsv / Lazer в окне настройки
            if Mod_HSV_Lazer == False:
                cv2.destroyAllWindows()
                cv2.namedWindow("Settings") ## Создаём окно настройки с ползунками
                ## ПОЛЗУНКИ ДЛЯ НАСТРОКИ ЯРКОСТИ ЛАЗЕРА
                cv2.createTrackbar('Lh1', 'Settings', Lh1, 255, nothing)
                cv2.createTrackbar('Ls1', 'Settings', Ls1, 255, nothing)
                cv2.createTrackbar('Lv1', 'Settings', Lv1, 255, nothing)
                cv2.createTrackbar('Lh2', 'Settings', Lh2, 255, nothing)
                cv2.createTrackbar('Ls2', 'Settings', Ls2, 255, nothing)
                cv2.createTrackbar('Lv2', 'Settings', Lv2, 255, nothing)
                Mod_HSV_Lazer = True
            else:
                cv2.destroyAllWindows()
                cv2.namedWindow("Settings") ## Создаём окно настройки с ползунками
                ## ПОЛЗУНКИ ДЛЯ НАСТРОКИ ЯРКОСТИ
                cv2.createTrackbar('h1', 'Settings', h1, 255, nothing)
                cv2.createTrackbar('s1', 'Settings', s1, 255, nothing)
                cv2.createTrackbar('v1', 'Settings', v1, 255, nothing)
                cv2.createTrackbar('h2', 'Settings', h2, 255, nothing)
                cv2.createTrackbar('s2', 'Settings', s2, 255, nothing)
                cv2.createTrackbar('v2', 'Settings', v2, 255, nothing)
                #print('X: ', x, ' Y: ', y)
                Mod_HSV_Lazer = False
        elif (((y > 135) and (y < 175)) and ((x > 540) and (x < 640))):
            Exit = True
        ###------------------------------------------------------------------------------------
    #elif event == cv2.EVENT_LBUTTONUP:##Когда кнопка мышки отпущена ЛКМ
        #print()
        #print(x, ' ', y)
##-------------------------------------------------------------

###-------переменные для камеры--------------------------------
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
BitMaska = frame ## Первое изображение для устранения ошибки
##------------------------------------------------------------
row, col, g = frame.shape #Находим размеры кадра например 480х640 с глубиной каналов в 3 цвета (RGB в зависимости от градации)

###cv2.namedWindow("Main menu")
###cv2.createTrackbar('ox', 'Main menu', h1, 640, nothing)
###cv2.createTrackbar('oy', 'Main menu', s1, 480, nothing)

while True:
    StartProgramm = cv2.getTickCount() ###Переменная для вычесления производительности время выполнения программы
    ret, frame = cap.read() ## считываем кадр с камеры и присваиваем фрейm
    reset = frame ## Первое изображение для устранения ошибки
    Iterfeys = INTERFEYS(frame.copy())
    

    ###----------------Условие для включение выбора мишени-------------------------------
    if ModViborMisheni == 1:
        cv2.putText(Iterfeys, 'Select top left corner',(185, 45), font, 0.6,(255,150,50),2,cv2.LINE_AA)
    elif ModViborMisheni == 2:
        cv2.putText(Iterfeys, 'Select the bottom right corner',(175, 445), font, 0.6,(255,150,50),2,cv2.LINE_AA)
    elif ModViborMisheni == 3: ## отображение надписи и кнопки
        cv2.rectangle(Iterfeys,(VerhniqLeviyYgolX, VerhniqLeviyYgolY),(NigniyPraviyYgolX,NigniyPraviyYgolY),(255,0,0),2)
        cv2.rectangle(Iterfeys,(0, 45),(100,85),(0,0,0),-1)
        cv2.rectangle(Iterfeys,(0, 45),(100,85),(0,255,0),2)##по х = 540 y = 45 (нижний угол х = 640 у = 85)
        cv2.putText(Iterfeys, 'Back',(25, 70), font, 0.6,(0,255,0),2,cv2.LINE_AA)
    ##---------------------------------------------------------------------------------

    ##---------------------Переключение между окнами настройки и главным меню------------------
    if ModSettings == True:
        if Mod_HSV_Lazer == False:
            ## СЧИТЫВАНИЕ ЗНАЧЕНИЙ С ПОЛЗУНКОВ ДЛЯ НАСТРОКИ ЯРКОСТИ
            h1 = cv2.getTrackbarPos('h1', 'Settings') ##Считывание с ползунка
            s1 = cv2.getTrackbarPos('s1', 'Settings') ##Считывание с ползунка
            v1 = cv2.getTrackbarPos('v1', 'Settings') ##Считывание с ползунка
            h2 = cv2.getTrackbarPos('h2', 'Settings') ##Считывание с ползунка
            s2 = cv2.getTrackbarPos('s2', 'Settings') ##Считывание с ползунка
            v2 = cv2.getTrackbarPos('v2', 'Settings') ##Считывание с ползунка
            
        BitMaska = MY.SettingYarkosty(frame.copy(), h1, s1, v1, h2, s2, v2)
        cv2.rectangle(BitMaska,(540, 0),(640,480),(0,0,0),-1)
        ##------------------------------------------------------------------------------
        if Mod_HSV_Lazer == True:
            ##-------------Тестовая часть кода для подгонки элементов-----------------------
            ## СЧИТЫВАНИЕ ЗНАЧЕНИЙ С ПОЛЗУНКОВ ДЛЯ НАСТРОКИ ЯРКОСТИ ЯРКОСТИ
            Lh1 = cv2.getTrackbarPos('Lh1', 'Settings') ##Считывание с ползунка
            Ls1 = cv2.getTrackbarPos('Ls1', 'Settings') ##Считывание с ползунка
            Lv1 = cv2.getTrackbarPos('Lv1', 'Settings') ##Считывание с ползунка
            Lh2 = cv2.getTrackbarPos('Lh2', 'Settings') ##Считывание с ползунка
            Ls2 = cv2.getTrackbarPos('Ls2', 'Settings') ##Считывание с ползунка
            Lv2 = cv2.getTrackbarPos('Lv2', 'Settings') ##Считывание с ползунка
            #cv2.putText(BitMaska, 'Lazer',(Lh1, Lh2), font, 0.6,(255,0,0),1,cv2.LINE_AA)
        BitMaska = MY.SettingYarkosty(BitMaska.copy(), Lh1, Ls1, Lv1, Lh2, Ls2, Lv2)
        ##------------------------------------------------------------------------------

        ##-------------Отрисовка Кнопки выхода в меню-----------------------------------------------
        cv2.rectangle(BitMaska,(540, 90),(640,130),(0,255,0),2)
        cv2.putText(BitMaska, 'Menu',(571, 117), font, 0.6,(0,255,0),2,cv2.LINE_AA)
        ##------------------------------------------------------------------------------

        ##-------------Отрисовка Кнопки переключения настройки освещения(Освещение/Точка лазера)-----
        cv2.rectangle(BitMaska,(540, 0),(640,85),(0,255,0),2)
        cv2.putText(BitMaska, 'h/s/v',(566, 29), font, 0.6,(0,255,0),2,cv2.LINE_AA)
        cv2.putText(BitMaska, '------',(543, 45), font, 0.6,(0,255,0),2,cv2.LINE_AA)
        cv2.putText(BitMaska, 'Lazer',(567, 66), font, 0.6,(0,255,0),2,cv2.LINE_AA)
        

        cv2.setMouseCallback('Settings',OneKlik) ## проверяем было ли вызванно событие мышки например двойной клик
        cv2.imshow('Settings', BitMaska) ## Окно настроек
    else:
        ##-------------Отрисовка Кнопки входа в настройки-----------------------------------

        cv2.rectangle(Iterfeys,(540, 90),(640,130),(0,255,0),2)
        cv2.putText(Iterfeys, 'Settings',(555, 116), font, 0.6,(0,255,0),2,cv2.LINE_AA)
        ##--------------------------------------------------------------------------------
        
        if ModViborMisheni == -1:## Игровой режим(тут пишем код уже во время игры)
            #print(BitMaska.shape)
            frame = cut(frame, VerhniqLeviyYgolX, VerhniqLeviyYgolY, NigniyPraviyYgolX, NigniyPraviyYgolY)
            BitMaska = MY.ObnarujenieTochki(frame, WindowGame, Lh1, Ls1, Lv1, Lh2, Ls2, Lv2, VerhniqLeviyYgolX, VerhniqLeviyYgolY, NigniyPraviyYgolX, NigniyPraviyYgolY, cap)

            if Resultat_Otstrela_Flag == False: ## отображает маленькое окно мишени
                cv2.imshow("Game window", BitMaska) ## Инровое окно
            #elif (Flag_Show_Line == True) and (Resultat_Otstrela_Flag == True): ## В разработке(будет отображать линии от попадания к номеру выстрела)
                #print()
            else: ## отображает большое окно мишени
                Copy_Bit_Maska_Resize = SizeImg(BitMaska.copy())
                cv2.imshow("Result", Copy_Bit_Maska_Resize) ## Игровое окно
            #cv2.imshow("WindowGame", WindowGame) ## Инровое окно
        else: ## Главное меню
            ####----------------Условие включение выключение ИПС-------------------------------
            if ModFps == True:
                StopProgramm = cv2.getTickCount()
                time = (StopProgramm - StartProgramm) / cv2.getTickFrequency()
                cv2.putText(Iterfeys, 'IPS: ' + str(time),(col - 150, row - 10), font, 0.5,(255,150,50),1,cv2.LINE_AA)
            ##---------------------------------------------------------------------------------
            ###отладка главного меню
            ###ox = cv2.getTrackbarPos('ox', 'Main menu') ##Считывание с ползунка
            ###oy = cv2.getTrackbarPos('oy', 'Main menu') ##Считывание с ползунка
            ###cv2.putText(Iterfeys, 'Exit',(ox, oy), font, 0.6,(255,0,0),2,cv2.LINE_AA)

            cv2.setMouseCallback('Main menu',OneKlik) ## проверяем было ли вызванно событие мышки например двойной клик
            cv2.imshow('Main menu', Iterfeys) ## Главное окно

    ##--------------------------------------------------------------------------------
    
    
    ##---------Условия нажатий кнопокклавиатуры-----------------------------------
    key = cv2.waitKey(1) & 0xFF
    #exit = cv2.getWindowImageRect("Main menu")
    #if key != 255:
     #   print(key)
       
    ### 233 Код буквы "й" (cv2.getWindowImageRect("Main menu") < (1,1,1,1)) - проверяет нажат ли крестик
    if key == ord('q') or (key == 233) or Exit == True: 
        StopProgramm = cv2.getTickCount()
        time = (StopProgramm - StartProgramm) / cv2.getTickFrequency()
        print('Время окончания: ', time)
        break #Выход
    
    elif key == 27 and ModViborMisheni == -1:
        cv2.destroyAllWindows()
        ModViborMisheni = 0
        ## ПОЛЗУНКИ ДЛЯ НАСТРОКИ ЯРКОСТИ ЛАЗЕРА
        cv2.createTrackbar('Lh1', 'Settings', Lh1, 255, nothing)
        cv2.createTrackbar('Ls1', 'Settings', Ls1, 255, nothing)
        cv2.createTrackbar('Lv1', 'Settings', Lv1, 255, nothing)
        cv2.createTrackbar('Lh2', 'Settings', Lh2, 255, nothing)
        cv2.createTrackbar('Ls2', 'Settings', Ls2, 255, nothing)
        cv2.createTrackbar('Lv2', 'Settings', Lv2, 255, nothing)
        cv2.destroyAllWindows()
                
        ## ПОЛЗУНКИ ДЛЯ НАСТРОКИ ЯРКОСТИ
        cv2.createTrackbar('h1', 'Settings', h1, 255, nothing)
        cv2.createTrackbar('s1', 'Settings', s1, 255, nothing)
        cv2.createTrackbar('v1', 'Settings', v1, 255, nothing)
        cv2.createTrackbar('h2', 'Settings', h2, 255, nothing)
        cv2.createTrackbar('s2', 'Settings', s2, 255, nothing)
        cv2.createTrackbar('v2', 'Settings', v2, 255, nothing)

    elif (key == ord('r') or key == 234) and ModViborMisheni == -1:### 233 Код буквы "к"
        if Resultat_Otstrela_Flag == False:
            #Copy_Bit_Maska_Resize = SizeImg(BitMaska.copy())
            Resultat_Otstrela_Flag = True
        else:
            Resultat_Otstrela_Flag = False
        cv2.destroyAllWindows()
    elif (key == ord('c') or key == 241) and ModViborMisheni == -1:### 233 Код буквы "с"
        cv2.destroyAllWindows()
        if Flag_Sbros_Podschet == False:
            Flag_Sbros_Podschet = True
            Flag_Sbros_Podschet = MY.sbros(Flag_Sbros_Podschet)
        ##-----Вырезаем изображение и присваеваем его глобальной переменной в новое окно----------------
        carved = cut(reset, VerhniqLeviyYgolX, VerhniqLeviyYgolY, NigniyPraviyYgolX, NigniyPraviyYgolY)
        WGRow, WGCol, WGChsnel = carved.shape
        WindowGame = np.zeros((WGRow,WGCol,3), np.uint8) ## Создаём новое окно для игры.(что бы вставить туда вырезенный обьект)
        WindowGame = carved
        ##-----------------------------------------------------------------------------------
    ## Условие ниже в разработке(показать скрыть линии от попадания к номеру выцстрела)
    #elif (key == ord('p') or key == 241) and ModViborMisheni == -1:### 233 Код буквы "з"
     #   if Flag_Show_Line == False: Flag_Show_Line = True
      #  else: Flag_Show_Line = True
    ##----------------------------------------------------------------------------

    
cap.release()
cv2.destroyAllWindows()