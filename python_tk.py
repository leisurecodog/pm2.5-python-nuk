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
import datetime
import time
from location import *


'''
HoverButton class:
    # inherence tk.button class
    # add more function(eg.bind) for HoverButton
'''
class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.leavebg = 'purple'
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self,e):
        self['background'] = self['activebackground']

    def on_leave(self,e):
        self['background'] = self.leavebg


def hit_me():
    var.set('you hit me')


'''
clear function:
    # hide and delete these lists
    # detail_list: stations which is created by previous area button
    # label_list: detail information for which station you clicked
'''
def clear():
    #detail_list used to store station_name
    #label_list used to store label in ui
    #btn_close is 代表關閉的 'x'符號
    global detail_list, h_frame, btn_close, timer
    for t in detail_list:
        t.destroy()
        del t
    h_frame.destroy()
    
    if timer.is_alive():
        timer.cancel()
    
'''
put_color function:
    # it will return color of string
    # depend on its parameter temp_value
    # according rule below(see function implementation)
'''
def put_color(temp_value):
    if temp_value == -1:
        return "gray70"
    
    if temp_value <= 50:
        return "green2"
    
    if temp_value <= 100:
        return "yellow"
    
    if temp_value <= 150:
        return "dark orange"
    
    if temp_value <= 200:
        return "red3"
    
    if temp_value <= 300:
        return "purple3"
    
    return  "saddle brown"

def cancel_play(self):
    timer.cancel()

'''
handler function:
    # handler function will create label for detail information
    # which you clicked
    # will call put_color function(above) to get color when it needs
'''
def handler(aqi_value, station_name, station):
    global h_frame, timer
    label_x = 260
    lb3_data = ''
    def destroy_labels():
        h_frame.destroy()
        timer.cancel()
        
        
    # destroy above global widgets when station button was clicked
    h_frame.destroy()
    
    h_frame = Frame(window, width=200, height=30,bg='white')
    h_frame.place(x=label_x, y=30)
    
    if aqi_value == -1:
        lb3_data = '設備維護中'
    else:
        lb3_data = ['ND' if data == '-1' or data == '-' else data for data in station[station_name].split()]
    # initialize the label2 and label3
    label2 = tk.Label(h_frame, text=station_name, font=('Arial',12), width = 30, height=2)
    label3 = tk.Label(h_frame, text=lb3_data, font=('Arial',12), width = 30, height=2)
    label2.pack(fill=X)
    label3.pack(fill=X)
    
    color = put_color(aqi_value) # get color
    
    # btn_close:close label2 and label3
    btn_close = Button(label2, text='X', bg=color, compound=TOP, relief=FLAT, command=destroy_labels)
    btn_close.pack(side=RIGHT)
    label2.configure(bg=color)
    label3.configure(bg=color)
            
'''
recursion function:
    #when the area button is onclick
    #every 10 seconds 輪播測站data
    #when the 測站button is onclick ,stop recursion(or start resursion from that測站?)
    #using datatime to check if 10 sec 
    
'''
def recursion(station):    
    global timer, count_station
    timer = threading.Timer(3,lambda s=station : recursion(s))
    timer.start()
    
    
    station_name = list(station)
    length = len(station_name)
    if count_station < length:
        info = station[station_name[count_station]].split()#information of station
        aqi = int(info[0])
        handler(aqi, station_name[count_station], station)
        count_station += 1
    else:
        count_station = 0
'''
new_station function:
    # create station buttons for this area
    # save to golbal list(detail_list)
    # clear function(above) to hidden and delete these stations when click another area
'''
def new_station(station, area_y):
    
    
    global count_station
    global detail_list
    counter = 0
    test3 = list(station)
    for i in range(len(test3)):
        
        info = station[test3[i]].split()# information of each station
        
        tmp = Button(window, text=str(test3[i]), font = ('Arial',12))
        tmp.place(x=130, y=area_y+22*i, width=120, height=22)

        temp_value = int(info[0])
        # info[0] is AQI(if station is x then info[0] is -1)
        
        # push and give it a function and parameters
        tmp.configure(bg=put_color(temp_value), command=lambda val=temp_value, x=test3[i], s=station:handler(val, x, s))
        tmp.bind("<Button-1>",cancel_play)
        detail_list.append(tmp)
        
        counter = counter + 1
    count_station = 0
    recursion(station)
'''
change_area_image:
    # chanage its image when area button was clicked
'''
def change_area_image(img):
    global ptaiwan
    try:
        area_img = ImageTk.PhotoImage(Image.open('photo/taiwan-' + img + '.png'))
    except FileNotFoundError:
        area_img = ImageTk.PhotoImage(Image.open('photo/taiwan-total.png'))
    ptaiwan.configure(image=area_img)
    ptaiwan.image = area_img

'''
select_area:
    # which paremeter is the area you sent in
    # it will open this txt file to get all station in this area
'''
def select_area(where):
    clear()
    global city, area, temp_value, detail_list
    chinese_name = ''
    # find this button's name
    for x, y in area.items():
        if y == where:
            chinese_name = x
            break
    ypos = 0
    for i ,c in zip(city,range(len(city))):
        if i['text'] == chinese_name:
            ypos = c * 60
    change_area_image(where)
    station_n = {}
    total = []
    # open data
    with open(where + '.txt','r')as f:
        lst = f.readlines()
        for i in range(len(lst)):
            lst[i] = lst[i].strip('\n')
            if i % 2 == 0:
                
                temp_city = lst[i]
                station_n[temp_city] = ''

            else:
                station_n[temp_city] = lst[i]
                
    new_station(station_n, ypos)

def _delete_window():
    window.destroy()
    timer.cancel()
#=========================================main program================================================

if __name__ == '__main__':

    main_fun()
    window = tk.Tk()
    window.geometry("700x600+300+10")
    window.title("Python期末專題-空氣指標小工具")
    window.configure(background='white')
    window.protocol("WM_DELETE_WINDOW",_delete_window)# when you click close(x)button will call this function
    
    # 
    btn_frame = Frame(window, relief=GROOVE, bg='purple',width=130)# save main btns
    btn_frame.pack(side=LEFT,fill=BOTH)
    h_frame = Frame(window)
    var = tk.StringVar()#文字變亮儲存器
    taiwan = ImageTk.PhotoImage(Image.open('photo/taiwan-total.png'))
    
    city = []
    detail_list = []
    label_list = []
    area = {'北部':'North', '竹苗':'Chu-Miao', '中部':'Central', '雲嘉南':'Yun-Chia-Nan',
            '高屏':'KaoPing', '宜蘭':'Yilan', '花東':'Hua-Tung', '馬祖':'Matsu', '金門':'Kinmen', '馬公':'Magong'}

    # photo of taiwan
    ptaiwan = Label(window, image=taiwan, bg='white')
    ptaiwan.pack(side=RIGHT)
    all_area = []
    # initialize the timer
    timer = threading.Timer(.5,0,'','')
    
    # the area button
    for x in area.keys():
        tmp_button = HoverButton(btn_frame, compound = CENTER, bg='purple', fg='white', activebackground='orchid3', text = x, font = ('Arial',"14","bold"),
                            command=lambda val=area[x]: select_area(val), relief=FLAT)
        tmp_button.pack()
        city.append(tmp_button)
        all_area.append(area[x])

    count =0
    # set places
    for i in city:
        i.place(x=0, y = 60*(count), width = 130, height = 60)
        count = count + 1
                            
    #data : AQI(空氣品質) 臭氧 細懸浮微粒 懸浮微粒 一氧化碳 二氧化硫 二氧化氮
    
    #location of user ip , and 優先顯示那地區的測站
    dic = get_pos()
    c_index = dic['city'].find(' ')
    city_name = dic['city'][:c_index]
    city_name = city_name.lower()
    all_city = [('keelung','new taipei','taipei','taoyuan'),('hsinchu','miaoli'),('taichung','nantou','changhua')
                ,('yunlin','chiayi','tainan'),('kaohsiung','pingtung ') 
                ,('yilan'),('taitung','hualien'),('lienchiang'),('kinmen') ,('penghu')]
    city_name='tainan'
    for i in range(len(all_city)):
        if city_name in all_city[i]:
            select_area(all_area[i])
    window.mainloop()
