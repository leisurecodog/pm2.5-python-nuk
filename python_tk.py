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

def reset_tabstop(event):
    event.widget.configure(tabs=(event.width-8, "right"))
    
class DetailFrame(tk.Frame):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.label_list = [ Label(self, font=('Arial',12), anchor='center', bg='white', relief=FLAT) for i in range(8)]
        self.titles = ['AQI(空氣品質)', '臭氧', '細懸浮微粒', '懸浮微粒', '一氧化碳', '二氧化硫', '二氧化氮']
    def set_info(self,data):
        self.label_list[0].configure(text=data[0], width=30)
        self.label_list[0].pack(fill=X)
        # cancel button
        self.cancel = Button(self.label_list[0], compound=TOP, text='X', bg=self.label_list[0]['background'], command=destroy_detail, relief=FLAT)
        self.cancel.pack(side=RIGHT)
        count = 1
        for i, j in zip(self.label_list[1:],data[1:]):
            if count == 1:
                i.configure(bg=put_color(int(j)))
            tmp1 = Text(i, height=2, width=30, bg=i['background'], relief=FLAT)
            tmp1.insert(END,self.titles[count-1] + '\t' + data[count])
            tmp1.pack(fill=X)
            tmp1.bind("<Configure>", reset_tabstop)
            i.pack(fill=X)
            count += 1
    

def hit_me():
    var.set('you hit me')
def destroy_detail():
    global d_frame, timer
    d_frame.destroy()
    timer.cancel()

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
    global detail_list, d_frame, timer
    for t in detail_list:
        t.destroy()
        del t
    d_frame.destroy()
    
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
    global d_frame
    
    # destroy it
    d_frame.destroy()
    d_frame = DetailFrame(window, bg='white', width=200, height=30, relief=GROOVE)
    d_frame.set_info([station_name] + station[station_name].split())
    d_frame.place(x=270, y=30)
    
    
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
    
    print('recursion')
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
    tc.join()
#=========================================main program================================================

if __name__ == '__main__':

    tc = threading.Thread(target=main_fun)
    tc.start()
    window = tk.Tk()
    window.geometry("850x600+300+10")
    window.title("Python期末專題-空氣指標小工具")
    window.configure(background='white')
    window.protocol("WM_DELETE_WINDOW",_delete_window)# when you click close(x)button will call this function
    
    # 
    btn_frame = Frame(window, relief=GROOVE, bg='purple',width=130)# save main btns
    btn_frame.pack(side=LEFT,fill=BOTH)
    d_frame = DetailFrame(window)
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
    if c_index == -1:
        city_name = dic['city']
    else:
        city_name = dic['city'][:c_index]
    city_name = city_name.lower()
    
    all_city = [('keelung','new taipei','taipei','taoyuan'),('hsinchu','miaoli'),('taichung','nantou','changhua')
                ,('yunlin','chiayi','tainan'),('kaohsiung','pingtung ') 
                ,('yilan'),('taitung','hualien'),('lienchiang'),('kinmen') ,('penghu')]
    for i in range(len(all_city)):
        if city_name in all_city[i]:
            select_area(all_area[i])
    window.mainloop()
