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

##===========Для выбора камеры
Camera = 0
Val_Camera = 0
for i in range(5):
    cap = cv2.VideoCapture(i)
    ret, frame = cap.read()
    if ret == True:
        Val_Camera = Val_Camera + 1

#cap = cv2.VideoCapture(0)
##========================================================================
##----Изменение размера с сохранением соотношения сторон-----
scale_percent = 400 # Процент от изначального размера
SizeResult = 4 ## Переменная для увеличсения окна
SizeResultTemp = 4
def SizeImg (IMAGES, scale_percent):
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
Exit = False ## переменная для кнопки выхода\

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
h1 = 8## Временно для вустановки значения сколько выстрелов сделат
h2 = 255##
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
Auto_Podschet_WindowGame = np.zeros((0,0,3), np.uint8) ## =======================
#WindowGameNoLine = np.zeros((0,0,3), np.uint8) ## Создаём новое окно для игры.(что бы вставить туда вырезенный обьект)
WGRow, WGCol, WGChsnel = 0, 0, 0
## Переключение ползунков hsv / Lazer в окне настройки
Mod_HSV_Lazer_Schet = 0
## Переменные для настройки контуров мишени
ASh1 = 0
ASh2 = 255
ASs1 = 0
ASs2 = 255
ASv1 = 0
ASv2 = 255
Flag_Setting_Window_AutoSchet = False ## флаг для включения нужного окна с ползунками. лазер хсв авто подсчёт
Mod_vibor_misheni_window_setting = 0 ## флаг для переключения между выборами углов
Setting_misheny_kontyr = 0 ### переменная для вырезки мишени поиска контуров
kontyr = 0 ##для отображения числа контуров в окне настройки
Flag_show_knopka_Save_window_settings = -1 #Для визуального просмотра нажалась ли кнопка сохранить
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
    if event == cv2.EVENT_LBUTTONUP:#cv2.EVENT_LBUTTONDBLCLK:##Двойной щелчок ЛКМ
        global ModFps, ModViborMisheni, VerhniqLeviyYgolX, VerhniqLeviyYgolY ##обязательно обьявляем переменные как глобальные или не будут работать
        global NigniyPraviyYgolX, NigniyPraviyYgolY, ModSettings, h1, h2, s1, s2, v1, v2, WindowGame, Auto_Podschet_WindowGame, Mod_HSV_Lazer_Schet, ASh1, ASs1, ASv1, ASh2, ASs2, ASv2
        global Lh1, Lh2, Ls1, Ls2, Lv1, Lv2, WGRow, WGCol, WGChsnel, Exit, Mod_vibor_misheni_window_setting, Flag_Sbros_Podschet, Flag_show_knopka_Save_window_settings, Setting_misheny_kontyr
        global Camera, cap, Val_Camera
        ###---------------------Кнопка ФПС----------------------------------------------------
        if ((y > 0) and (y < 40)) and ((x > 540) and (x < 640)) and (ModSettings == False) and (ModViborMisheni != 1) and (ModViborMisheni != 2) and (ModViborMisheni != 3): ## область кнопки ФПС
            if ModFps == False: ModFps = True
            else: ModFps = False
        ###------------------------------------------------------------------------------------

        ###---------------------КНОПКА СТАРТ------------------------------------------------------
        elif ((y > 45) and (y < 85)) and ((x > 540) and (x < 640)) and ModSettings == False: ## область кнопки старт
            #if ModViborMisheni == 0:
            #    ModViborMisheni = 1 ## Включён выбор верхнего левого угла
            if ModViborMisheni == 3: ## Последний шаг когда нажата кнопка старт включает режим игры
                ##(Здесь пишем код связыный с повторным нажатием кнопки старт)
                cv2.destroyAllWindows() ## убераем окно
                Flag_Sbros_Podschet = True
                Flag_Sbros_Podschet = MY.sbros(Flag_Sbros_Podschet)
                ##-----Вырезаем изображение и присваеваем его глобальной переменной в новое окно----------------
                carved = cut(frame, VerhniqLeviyYgolX+5, VerhniqLeviyYgolY+5, NigniyPraviyYgolX-5, NigniyPraviyYgolY-5)
                WGRow, WGCol, WGChsnel = carved.shape
                WindowGame = np.zeros((WGRow,WGCol,3), np.uint8) ## Создаём новое окно для игры.(что бы вставить туда вырезенный обьект)
                #Auto_Podschet_WindowGame = np.zeros((WGRow,WGCol,3), np.uint8) ## Переменные окна для определения счёта
                #Auto_Podschet_WindowGame = carved ## Переменные окна для определения счёта
                #WindowGameNoLine = np.zeros((WGRow,WGCol,3), np.uint8) ## Создаём новое окно для игры.(что бы вставить туда вырезенный обьект)
                #WindowGameNoLine = carved
                WindowGame = carved

                
                ##-----------------------------------------------------------------------------------
                #cv2.imshow('asd', WindowGame)
                ModViborMisheni = -1
        ### Присваиваем переменным кординаты угла
        #elif ModViborMisheni == 1 and (x < 540): 
            ## Присваивание переменной кординаты верхнего левого угла
            #VerhniqLeviyYgolX = x
            #VerhniqLeviyYgolY = y
            #ModViborMisheni = 2 ## Включён выбор нижнего правого угла
        #elif ModViborMisheni == 2 and (x < 540):
            ## Присваивание переменной кординаты нижнего правого угла
            #NigniyPraviyYgolX = x
            #NigniyPraviyYgolY = y
            ## Проверка на то что углы были выбраны правильно
            #if (VerhniqLeviyYgolX > NigniyPraviyYgolX) or (VerhniqLeviyYgolY > NigniyPraviyYgolY):
                #ModViborMisheni = 1
            #else: ModViborMisheni = 3
        ## Кнопка отмены
        #elif ((y > 45) and (y < 85)) and ((x > 0) and (x < 100)) and ModViborMisheni == 3:
            #VerhniqLeviyYgolX = 0
            #VerhniqLeviyYgolY = 0
            #NigniyPraviyYgolX = 0
            #NigniyPraviyYgolY = 0
            #ModViborMisheni = 0
        ##---------------------------------------------------------------------------------------------

        ###---------------------Кнопки окна настроек----------------------------------------------------
        
        elif ((y > 90) and (y < 130)) and ((x > 540) and (x < 640)) and (ModViborMisheni != 1) and (ModViborMisheni != 2):# and (ModViborMisheni != 3): ## область кнопки настроек
            if ModSettings == False:
                cv2.destroyAllWindows()
                cv2.namedWindow("Settings") ## Создаём окно настройки с ползунками
                ## ПОЛЗУНКИ ДЛЯ НАСТРОКИ ЯРКОСТИ
                cv2.createTrackbar('KolVistrelov', 'Settings', h1, 16, nothing)
                cv2.createTrackbar('s1', 'Settings', s1, 255, nothing)
                cv2.createTrackbar('v1', 'Settings', v1, 255, nothing)
                cv2.createTrackbar('h2', 'Settings', h2, 255, nothing)
                cv2.createTrackbar('s2', 'Settings', s2, 255, nothing)
                cv2.createTrackbar('v2', 'Settings', v2, 255, nothing)
                Mod_HSV_Lazer_Schet = 0
                ModSettings = True
            else:
                cv2.destroyAllWindows()
                Mod_vibor_misheni_window_setting = 0
                #ModViborMisheni = 3
                ModSettings = False
        elif (((y > 0) and (y < 40)) and ((x > 540) and (x < 640))) and (ModSettings == True): ## область кнопки hsv в окне настройки
            Mod_HSV_Lazer_Schet = 0
            cv2.destroyAllWindows()
            cv2.namedWindow("Settings") ## Создаём окно настройки с ползунками
            ## ПОЛЗУНКИ ДЛЯ НАСТРОКИ ЯРКОСТИ
            cv2.createTrackbar('KolVistrelov', 'Settings', h1, 16, nothing)
            cv2.createTrackbar('s1', 'Settings', s1, 255, nothing)
            cv2.createTrackbar('v1', 'Settings', v1, 255, nothing)
            cv2.createTrackbar('h2', 'Settings', h2, 255, nothing)
            cv2.createTrackbar('s2', 'Settings', s2, 255, nothing)
            cv2.createTrackbar('v2', 'Settings', v2, 255, nothing)
        elif (((y > 45) and (y < 85)) and ((x > 540) and (x < 640))) and (ModSettings == True): ## область кнопки Lazera в окне настройки 
            Mod_HSV_Lazer_Schet = 1
            cv2.destroyAllWindows()
            cv2.namedWindow("Settings") ## Создаём окно настройки с ползунками
            ## ПОЛЗУНКИ ДЛЯ НАСТРОКИ ЯРКОСТИ ЛАЗЕРА
            cv2.createTrackbar('Lh1', 'Settings', Lh1, 255, nothing)
            cv2.createTrackbar('Ls1', 'Settings', Ls1, 255, nothing)
            cv2.createTrackbar('Lv1', 'Settings', Lv1, 255, nothing)
            cv2.createTrackbar('Lh2', 'Settings', Lh2, 255, nothing)
            cv2.createTrackbar('Ls2', 'Settings', Ls2, 255, nothing)
            cv2.createTrackbar('Lv2', 'Settings', Lv2, 255, nothing)

        elif (((y > 135) and (y < 175)) and ((x > 540) and (x < 640))) and (ModSettings == True): ## Условие для кнопки автоподсчёта
            Flag_show_knopka_Save_window_settings = 0
            Mod_HSV_Lazer_Schet = 2
            Mod_vibor_misheni_window_setting = 0
            ModViborMisheni = 0
            cv2.destroyAllWindows()
            cv2.namedWindow("Settings") ## Создаём окно настройки с ползунками
            cv2.createTrackbar('ASh1', 'Settings', ASh1, 640, nothing)
            cv2.createTrackbar('ASs1', 'Settings', ASs1, 480, nothing)
            #cv2.createTrackbar('ASh1', 'Settings', ASh1, 255, nothing)
            #cv2.createTrackbar('ASs1', 'Settings', ASs1, 255, nothing)
            cv2.createTrackbar('Kontyri', 'Settings', ASv1, 255, nothing)
            cv2.createTrackbar('ASh2', 'Settings', ASh2, 16, nothing)
            cv2.createTrackbar('ASs2', 'Settings', ASs2, 255, nothing)
            cv2.createTrackbar('ASv2', 'Settings', ASv2, 255, nothing)
            if Mod_vibor_misheni_window_setting == 0:
                Mod_vibor_misheni_window_setting = 1 ## Включён выбор верхнего левого угла
        elif (((y > 180) and (y < 220)) and ((x > 540) and (x < 640))) and (ModSettings == True) and (Mod_HSV_Lazer_Schet == 2): ## Условие для кнопки сохранить параметры изображения 540, 180),(640,220
            Auto_Podschet_WindowGame = np.zeros((WGRow,WGCol,3), np.uint8) ## Переменные окна для определения счёта
            Auto_Podschet_WindowGame = Setting_misheny_kontyr
            Flag_show_knopka_Save_window_settings = 1
            ModViborMisheni = 3
        elif (((y > 180) and (y < 220)) and ((x > 540) and (x < 640))) and (ModSettings == True) and (Mod_HSV_Lazer_Schet != 2): ## Условие для кнопки камера выбор 540, 180),(640,220
            cap.release()
            cv2.destroyAllWindows()
            ## ПОЛЗУНКИ ДЛЯ НАСТРОКИ камеры
            cap = cv2.VideoCapture(Camera)
            #print(ret)
            #ret, frame = cap.read()
            if not cap.isOpened():
                raise IOError("Cannot open webcam")
            #print(ret)
            cv2.namedWindow("Settings") ## Создаём окно настройки с ползунками
            cv2.createTrackbar('Camera', 'Settings', Camera, Val_Camera-1, nothing)
            Mod_HSV_Lazer_Schet = 3
            #elif ModViborMisheni == 3: ## Последний шаг когда нажата кнопка старт включает режим игры 
                ##(Здесь пишем код связыный с повторным нажатием кнопки старт)
                #cv2.destroyAllWindows() ## убераем окно
                #Flag_Sbros_Podschet = True
                #Flag_Sbros_Podschet = MY.sbros(Flag_Sbros_Podschet)
                ##-----Вырезаем изображение и присваеваем его глобальной переменной в новое окно----------------
                #carved = cut(frame, VerhniqLeviyYgolX, VerhniqLeviyYgolY, NigniyPraviyYgolX, NigniyPraviyYgolY)
                #WGRow, WGCol, WGChsnel = carved.shape
                #WindowGame = np.zeros((WGRow,WGCol,3), np.uint8) ## Создаём новое окно для игры.(что бы вставить туда вырезенный обьект)
                #WindowGameNoLine = np.zeros((WGRow,WGCol,3), np.uint8) ## Создаём новое окно для игры.(что бы вставить туда вырезенный обьект)
                #WindowGameNoLine = carved
                #WindowGame = carved
                ##-----------------------------------------------------------------------------------
                #cv2.imshow('asd', WindowGame)
                #ModViborMisheni = -1
        ## Присваиваем переменным кординаты угла
        elif Mod_vibor_misheni_window_setting == 1 and (x < 540) and (ModSettings == True): 
            ## Присваивание переменной кординаты верхнего левого угла
            VerhniqLeviyYgolX = x
            VerhniqLeviyYgolY = y
            Mod_vibor_misheni_window_setting = 2 ## Включён выбор нижнего правого угла
        elif Mod_vibor_misheni_window_setting == 2 and (x < 540) and (ModSettings == True):
            ## Присваивание переменной кординаты нижнего правого угла
            NigniyPraviyYgolX = x
            NigniyPraviyYgolY = y
            ## Проверка на то что углы были выбраны правильно
            if ((VerhniqLeviyYgolX > NigniyPraviyYgolX) or (VerhniqLeviyYgolY > NigniyPraviyYgolY)):
                Mod_vibor_misheni_window_setting = 1
            else:
                #ModViborMisheni = 3
                Mod_vibor_misheni_window_setting = 3
            #print(x, ' ', y)

        ## =====================================================================================================
        elif (((y > 135) and (y < 175)) and ((x > 540) and (x < 640))) and (ModViborMisheni != 1) and (ModViborMisheni != 2) and (ModSettings == False):#and (ModViborMisheni != 3) 
            Exit = True
        ###------------------------------------------------------------------------------------
    #elif event == cv2.EVENT_LBUTTONUP:##Когда кнопка мышки отпущена ЛКМ
        #print()
        #print(x, ' ', y)
##-------------------------------------------------------------

###-------переменные для камеры--------------------------------
cap = cv2.VideoCapture(Camera)
ret, frame = cap.read()
BitMaska = frame ## Первое изображение для устранения ошибки
##------------------------------------------------------------
row, col, g = frame.shape #Находим размеры кадра например 480х640 с глубиной каналов в 3 цвета (RGB в зависимости от градации)

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
        cv2.rectangle(Iterfeys,(VerhniqLeviyYgolX, VerhniqLeviyYgolY),(NigniyPraviyYgolX,NigniyPraviyYgolY),(255,0,0),1)
        #cv2.rectangle(Iterfeys,(0, 45),(100,85),(0,0,0),-1)
        #cv2.rectangle(Iterfeys,(0, 45),(100,85),(0,255,0),2)##по х = 540 y = 45 (нижний угол х = 640 у = 85)
        #cv2.putText(Iterfeys, 'Back',(25, 70), font, 0.6,(0,255,0),2,cv2.LINE_AA)
    ##---------------------------------------------------------------------------------

    ##---------------------Переключение между окнами настройки и главным меню------------------
    if ModSettings == True:
###======================НИЖЕ ПИШЕМ КОД ДЛЯ ОКНА НАСТРОЙКИ==============================================
        if Mod_HSV_Lazer_Schet == 0: ## отображение для окна настройки хсв
            ## СЧИТЫВАНИЕ ЗНАЧЕНИЙ С ПОЛЗУНКОВ ДЛЯ НАСТРОКИ ЯРКОСТИ
            h1 = cv2.getTrackbarPos('KolVistrelov', 'Settings') ##Считывание с ползунка
            s1 = cv2.getTrackbarPos('s1', 'Settings') ##Считывание с ползунка
            v1 = cv2.getTrackbarPos('v1', 'Settings') ##Считывание с ползунка
            h2 = cv2.getTrackbarPos('h2', 'Settings') ##Считывание с ползунка
            s2 = cv2.getTrackbarPos('s2', 'Settings') ##Считывание с ползунка
            v2 = cv2.getTrackbarPos('v2', 'Settings') ##Считывание с ползунка
            MY.setSettings_Window_misheny(h1)
            BitMaska = MY.SettingYarkosty(frame.copy(), h1, s1, v1, h2, s2, v2)
        ##------------------------------------------------------------------------------
        elif Mod_HSV_Lazer_Schet == 1: ## Отображение кона настройки луча лазера
            ## СЧИТЫВАНИЕ ЗНАЧЕНИЙ С ПОЛЗУНКОВ ДЛЯ НАСТРОКИ ЯРКОСТИ ЯРКОСТИ
            Lh1 = cv2.getTrackbarPos('Lh1', 'Settings') ##Считывание с ползунка
            Ls1 = cv2.getTrackbarPos('Ls1', 'Settings') ##Считывание с ползунка
            Lv1 = cv2.getTrackbarPos('Lv1', 'Settings') ##Считывание с ползунка
            Lh2 = cv2.getTrackbarPos('Lh2', 'Settings') ##Считывание с ползунка
            Ls2 = cv2.getTrackbarPos('Ls2', 'Settings') ##Считывание с ползунка
            Lv2 = cv2.getTrackbarPos('Lv2', 'Settings') ##Считывание с ползунка
            BitMaska = MY.SettingYarkosty(frame.copy(), Lh1, Ls1, Lv1, Lh2, Ls2, Lv2)
        elif Mod_HSV_Lazer_Schet == 2:
            ASh1 = cv2.getTrackbarPos('ASh1', 'Settings') ##Считывание с ползунка
            ASs1 = cv2.getTrackbarPos('ASs1', 'Settings') ##Считывание с ползунка
            ASv1 = cv2.getTrackbarPos('Kontyri', 'Settings') ##Считывание с ползунка
            ASh2 = cv2.getTrackbarPos('ASh2', 'Settings') ##Считывание с ползунка
            ASs2 = cv2.getTrackbarPos('ASs2', 'Settings') ##Считывание с ползунка
            ASv2 = cv2.getTrackbarPos('ASv2', 'Settings') ##Считывание с ползунка
            #BitMaska = MY.SettingYarkosty(frame.copy(), ASh1, ASs1, ASv1, ASh2, ASs2, ASv2)
            BitMaska = frame.copy()
            ###----------------Условие для включение выбора мишени-------------------------------
            if Mod_vibor_misheni_window_setting == 1 and (ModSettings == True):
                cv2.putText(BitMaska, 'Select top left corner',(185, 45), font, 0.6,(255,150,50),2,cv2.LINE_AA)
            elif Mod_vibor_misheni_window_setting == 2 and (ModSettings == True):
                cv2.putText(BitMaska, 'Select the bottom right corner',(175, 445), font, 0.6,(255,150,50),2,cv2.LINE_AA)
            elif Mod_vibor_misheni_window_setting == 3 and (ModSettings == True): ## отображение области
                cv2.rectangle(BitMaska,(VerhniqLeviyYgolX, VerhniqLeviyYgolY),(NigniyPraviyYgolX,NigniyPraviyYgolY),(255,0,0),1)
                Setting_misheny_kontyr = cut(frame.copy(), VerhniqLeviyYgolX+5, VerhniqLeviyYgolY+5, NigniyPraviyYgolX-5, NigniyPraviyYgolY-5)
                
                kontyr = MY.Setting_Show_Podschet(Setting_misheny_kontyr, ASh1, ASs1, ASv1)#, ASh2, ASs2, ASv2)
                
            
             ##-------------##для отображения числа контуров-----------------------------------
            cv2.rectangle(BitMaska,(220, 440),(320,480),(128,128,128),-1)
            cv2.putText(BitMaska, str(kontyr),(260, 468), font, 0.6,(0,255,0),2,cv2.LINE_AA)
            ##------------------------------------------------------------------------------
        elif Mod_HSV_Lazer_Schet == 3:
            Camera = cv2.getTrackbarPos('Camera', 'Settings') ##Считывание с ползунка
            BitMaska = frame.copy()
    ##---------------------------------------------------------------------------------
            #cv2.putText(BitMaska, 'Lazer',(Lh1, Lh2), font, 0.6,(255,0,0),1,cv2.LINE_AA)
        #if Mod_HSV_Lazer == False: BitMaska = MY.SettingYarkosty(frame.copy(), h1, s1, v1, h2, s2, v2)
        #elif Mod_HSV_Lazer == True: BitMaska = MY.SettingYarkosty(BitMaska.copy(), Lh1, Ls1, Lv1, Lh2, Ls2, Lv2)
        #BitMaska = MY.SettingYarkosty(frame.copy(), h1, s1, v1, h2, s2, v2)
        #BitMaska = MY.SettingYarkosty(frame.copy(), Lh1, Ls1, Lv1, Lh2, Ls2, Lv2)

        ##------------------------------------------------------------------------------
        cv2.rectangle(BitMaska,(540, 0),(640,480),(0,0,0),-1)
        ##-------------Отрисовка Кнопки выхода в меню-----------------------------------------------
        cv2.rectangle(BitMaska,(540, 90),(640,130),(0,255,0),2)
        cv2.putText(BitMaska, 'Menu',(571, 117), font, 0.6,(0,255,0),2,cv2.LINE_AA)
        ##------------------------------------------------------------------------------

        ##=============отрисовка кнопки настроки авто подсчёта================
        cv2.rectangle(BitMaska,(540, 135),(640,175),(0,255,0),2)
        cv2.putText(BitMaska, 'AutoSchet',(543, 160), font, 0.6,(0,255,0),2,cv2.LINE_AA)

        if Mod_HSV_Lazer_Schet == 2:
            ## сохранить изображение мишени
            if Flag_show_knopka_Save_window_settings == 0:
                cv2.rectangle(BitMaska,(540, 180),(640,220),(0,255,0),2)
                cv2.putText(BitMaska, 'Save',(571, 205), font, 0.6,(0,255,0),2,cv2.LINE_AA)
        ##====================================================================

        ##-------------Отрисовка Кнопки переключения настройки освещения(Освещение/Точка лазера)-----
        cv2.rectangle(BitMaska,(540, 0),(640,40),(0,255,0),2) ## Кнопка ХСВ
        cv2.putText(BitMaska, 'h/s/v',(566, 25), font, 0.6,(0,255,0),2,cv2.LINE_AA)
        cv2.rectangle(BitMaska,(540, 45),(640,85),(0,255,0),2) ##Кнопка лазера настройка
        cv2.putText(BitMaska, 'Lazer',(567, 70), font, 0.6,(0,255,0),2,cv2.LINE_AA)
        ##-----------------для выбора камеры---------------------------------------
        if Mod_HSV_Lazer_Schet != 2:
            cv2.rectangle(BitMaska,(540, 180),(640,220),(0,255,0),2)
            cv2.putText(BitMaska, 'Camera',(555, 205), font, 0.6,(0,255,0),2,cv2.LINE_AA)
        
        cv2.setMouseCallback('Settings',OneKlik) ## проверяем было ли вызванно событие мышки например двойной клик
        cv2.imshow('Settings', BitMaska) ## Окно настроек
###================================================================================================================
###======================НИЖЕ ПИШЕМ КОД СВЯЗАННЫЙ С ГЛАВНЫМ ОКНОМ И ИГРОВЫМ ПРОЦЕСОМ===============================
    else:
        ##-------------Отрисовка Кнопки входа в настройки-----------------------------------

        cv2.rectangle(Iterfeys,(540, 90),(640,130),(0,255,0),2)
        cv2.putText(Iterfeys, 'Settings',(555, 116), font, 0.6,(0,255,0),2,cv2.LINE_AA)
        ##--------------------------------------------------------------------------------
        
        if ModViborMisheni == -1:## Игровой режим(тут пишем код уже во время игры)
            #print(BitMaska.shape)
            frame = cut(frame, VerhniqLeviyYgolX+5, VerhniqLeviyYgolY+5, NigniyPraviyYgolX-5, NigniyPraviyYgolY-5)
            BitMaska = MY.ObnarujenieTochki(frame, WindowGame, Lh1, Ls1, Lv1, Lh2, Ls2, Lv2, VerhniqLeviyYgolX, VerhniqLeviyYgolY, NigniyPraviyYgolX, NigniyPraviyYgolY, cap, Auto_Podschet_WindowGame.copy(),  ASh1, ASs1)#, ASv1, ASh2, ASs2, ASv2)
            #MY.Show_Podschet(test, ASh1, ASs1, ASv1, ASh2, ASs2, ASv2) Auto_Podschet_WindowGame
            if Resultat_Otstrela_Flag == False: ## отображает маленькое окно мишени
                cv2.imshow("Game window", BitMaska) ## Инровое окно
            else: ## отображает большое окно мишени
                SizeResult = cv2.getTrackbarPos('SizeResult', 'Result') ##Считывание с ползунка
                if (SizeResult * 100) > 0:
                    if SizeResult != SizeResultTemp:
                        SizeResultTemp = SizeResult
                        cv2.createTrackbar('SizeResult', 'Result', SizeResultTemp, 10, nothing)
                    scale_percent = SizeResult * 100
                else:
                    SizeResultTemp = 1
                    scale_percent = 100
                    cv2.createTrackbar('SizeResult', 'Result', SizeResultTemp, 10, nothing)
                Copy_Bit_Maska_Resize = SizeImg(BitMaska.copy(), scale_percent)
                #MY.Show_Podschet(Copy_Bit_Maska_Resize)
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
###================================================================================================================
    
    ##---------Условия нажатий кнопокклавиатуры-----------------------------------
    key = cv2.waitKey(1) & 0xFF
    #exit = cv2.getWindowImageRect("Main menu")
    #if key != 255:
    #    print(key)# ентр 13
       
    ### 233 Код буквы "й" (cv2.getWindowImageRect("Main menu") < (1,1,1,1)) - проверяет нажат ли крестик
    if key == ord('q') or (key == 233) or Exit == True: 
        StopProgramm = cv2.getTickCount()
        time = (StopProgramm - StartProgramm) / cv2.getTickFrequency()
        print('Время окончания: ', time)
        break #Выход
    
    elif key == 27 and ModViborMisheni == -1:
        cv2.destroyAllWindows()
        cv2.createTrackbar('SizeResult', 'Result', SizeResultTemp, 10, nothing)
        Resultat_Otstrela_Flag = False
        ModViborMisheni = 3
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
            cv2.destroyAllWindows()
            cv2.namedWindow("Result") ## Создаём окно настройки с ползунками
            cv2.createTrackbar('SizeResult', 'Result', SizeResultTemp, 10, nothing)
            #Copy_Bit_Maska_Resize = SizeImg(BitMaska.copy())
            Resultat_Otstrela_Flag = True
        else:
            cv2.destroyAllWindows()
            Resultat_Otstrela_Flag = False
    elif (key == ord('c') or key == 241) and ModViborMisheni == -1:### 233 Код буквы "с"
        if Flag_Sbros_Podschet == True:
            cv2.destroyAllWindows()
            cv2.namedWindow("Result") ## Создаём окно настройки с ползунками
            cv2.createTrackbar('SizeResult', 'Result', SizeResultTemp, 10, nothing)
        if Flag_Sbros_Podschet == False:
            Flag_Sbros_Podschet = True
            Flag_Sbros_Podschet = MY.sbros(Flag_Sbros_Podschet)
        ##-----Вырезаем изображение и присваеваем его глобальной переменной в новое окно----------------
        carved = cut(reset, VerhniqLeviyYgolX+5, VerhniqLeviyYgolY+5, NigniyPraviyYgolX-5, NigniyPraviyYgolY-5)
        WGRow, WGCol, WGChsnel = carved.shape
        WindowGame = np.zeros((WGRow,WGCol,3), np.uint8) ## Создаём новое окно для игры.(что бы вставить туда вырезенный обьект)
        #WindowGameNoLine = np.zeros((WGRow,WGCol,3), np.uint8) ## Создаём новое окно для игры.(что бы вставить туда вырезенный обьект)
        #WindowGameNoLine = carved
        WindowGame = carved
        ##-----------------------
        #MY.Setting_Show_Podschet(Setting_misheny_kontyr, ASh1, ASs1, ASv1, ASh2, ASs2, ASv2)
        #------------------------------------------------------------
        #test = cut(BitMaska.copy(), VerhniqLeviyYgolX+5, VerhniqLeviyYgolY+5, NigniyPraviyYgolX-5, NigniyPraviyYgolY-5)
        #Auto_Podschet_WindowGame = MY.Setting_Show_Podschet(test, ASh1, ASs1, ASv1, ASh2, ASs2, ASv2)

    
cap.release()
cv2.destroyAllWindows()
