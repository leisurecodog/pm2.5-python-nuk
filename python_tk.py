# -*- coding: utf-8 -*-
"""
Created on Thu May 23 13:54:31 2019

@author: user
"""
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from pm2dot5 import *
import threading

def hit_me():
    var.set('you hit me')
    
# it maps temp_value to colors 
def put_color(temp_value):
    if temp_value <=50:
        return "green2"
    
    if temp_value <=100:
        return "yellow"
    
    if temp_value <=150:
        return "dark orange"
    
    if temp_value <=200:
        return "red3"
    
    if temp_value <=300:
        return "purple3"
    
    return  "saddle brown"

def handler(temp_value,a):
    global label_list
    #label1 = tk.Label(window,text = 'python 專題',bg = 'green',font = ('Arial',12),width = 15 , height = 2)
    
    label2 = tk.Label(window , text = a , bg = 'green',font = ('Arial',12),width = 30 , height = 2 )
    label3 = tk.Label(window , text = station[a], bg = 'red',font = ('Arial',12),width = 30 , height = 2 )
    label2.place(x = 250 , y = 30 )
    label3.place(x= 250 , y = 60)
        #會有像觀音這個測站 他的AQI是None的情況 故只做temp_i != 0
    color=put_color(temp_value)
    label2.configure(bg = color)
    label3.configure(bg = color)
    label_list.append(label2)
    label_list.append(label3)
            
# make btns be hidden and delete btn in list
def clear():
    global detail_list, label_list
    for t in detail_list:
        t.place_forget()
        del t
    for l in label_list:
        l.place_forget()
        del l

def new_station(test3):
    global detail_list
    temp_i = station[test3[0]].find(' ')    
    counter = 0
    for i in range(len(test3)):
        # create button for each station
        tmp = Button(window,text=str(test3[i]))
        tmp.place(x=145,y=20*i,width=100,height=20)
    
        temp_i = int(station[test3[i]].find(' '))
        #會有像觀音這個測站 他的AQI是None的情況 故只做temp_i != 0
        if temp_i !=0:
            temp_value = int(station[test3[i]][0:temp_i])
        else:
            temp_value=0
        # push and give it a function and parameters
        tmp.configure(bg=put_color(temp_value),command=lambda val=temp_value,x=test3[i]:handler(val,x))
        detail_list.append(tmp)
        
        counter = counter +1
    
def select_area(which):
    clear()
    global temp_value
    global detail_list
    station_n = {}
    total = []
    # open data
    with open(which + '.txt','r')as f:
        Norths = f.readlines()
        for i in range(len(Norths)):
            Norths[i] = Norths[i].strip('\n')
            if i%2 == 0:
                
                temp_city = Norths[i]
                station_n[temp_city] = ''

            else:
                station_n[temp_city] = Norths[i]
    
    Keys = station_n.keys()
    test3 = list(station_n)

    counter = 0
    new_station(test3)
    
#==============main program================================================



window = tk.Tk()
window.geometry("600x500+350+50")
window.title("Python期末專題-空氣指標小工具")
window.configure(background='white')
#window.attributes('-alpha', 0.9)

btn_frame = Frame(window,relief=GROOVE).pack() # save main btns(blue btns)
var = tk.StringVar()#文字變亮儲存器

btn_img = PhotoImage(file='photo/btn.png')
taiwan = ImageTk.PhotoImage(Image.open('photo/taiwan.png'))

city = []
detail_list = []
label_list = []
area = {'北部':'North', '竹苗':'Chu-Miao', '宜蘭':'Yilan', '花東':'Hua-Tung',
        '雲嘉南':'Yun-Chia-Nan', '中部':'Central', '高屏':'KaoPing', '馬祖':'Matsu', '金門':'Kinmen', '馬公':'Magong'}
# photo taiwan(it uses label)
ptaiwan = Label(window,image=taiwan,bg='white')
ptaiwan.place(x=150,y=50)

# the station for each position
for x in area.keys():
    tmp_button = Button(btn_frame , compound = CENTER, bg='white', fg='white',text = x, image = btn_img, font = ('Arial',"14","bold"),
                        command = lambda val=area[x]: select_area(val), relief=FLAT)
    city.append(tmp_button)

count =0
# set places
for i in city:
    i.place(x=5 , y = 40*(count+1) , width = 134 , height = 40)
    count = count +1

global station
station = {}
temp_city = ''
for area_name in area.values():
    
    with open(area_name + '.txt','r')as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip('\n')
            if i%2 == 0:
                temp_city = lines[i]
                station[temp_city] = ''

            else:
                station[temp_city] = lines[i]
                        
            #data : AQI(空氣品質) 臭氧 細懸浮微粒 懸浮微粒 一氧化碳 二氧化硫 二氧化氮
            



window.mainloop()

