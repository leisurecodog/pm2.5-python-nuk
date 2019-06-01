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
    global detail_list, label_list, btn_close
    for t in detail_list:
        t.destroy()
        del t
    for l in label_list:
        l.destroy()
        del l
    btn_close.destroy()
    
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

'''
handler function:
    # handler function will create label for detail information
    # which you clicked
    # will call put_color function(above) to get color when it needs
'''
def handler(temp_value, a, station):
    global label_list, btn_close, label2, label3
    label_x = 260
    lb3_data = ''
    def destroy_labels():
        label2.destroy()
        label3.destroy()
        btn_close.destroy()
        
    # destroy three above global widgets when station button was clicked
    destroy_labels()
    
    if temp_value == -1:
        lb3_data = '設備維護中'
    else:
        lb3_data = ['ND' if data == '-1' or data == '-' else data for data in station[a].split()]
    # initialize the label2 and label3
    label2 = tk.Label(window, text=a, font=('Arial',12), width = 30, height=2)
    label3 = tk.Label(window, text=lb3_data, font=('Arial',12), width = 30, height=2)
    label2.place(x=label_x, y=30)
    label3.place(x=label_x, y=60)
    
    color = put_color(temp_value) # get color
    
    # btn_close:close label2 and label3
    btn_close = Button(window, text='X', bg=color, compound=TOP, relief=FLAT, command=destroy_labels)
    btn_close.place(x=2 * label_x, y=30, width=15)
    label2.configure(bg=color)
    label3.configure(bg=color)
    label_list.append(label2)
    label_list.append(label3)
            
'''
new_station function:
    # create station buttons for this area
    # save to golbal list(detail_list)
    # clear function(above) to hidden and delete these stations when click another area
'''
def new_station(station, area_y):
    global detail_list
    counter = 0
    test3 = list(station)
    for i in range(len(test3)):
        
        info = station[test3[i]].split()# information of each station
        
        tmp = Button(window, text=str(test3[i]), font = ('Arial',12))
        tmp.place(x=135, y=area_y+22*i, width=120, height=22)

        temp_value = int(info[0])
        # info[0] is AQI(if station is x then info[0] is -1)
        
        # push and give it a function and parameters
        tmp.configure(bg=put_color(temp_value), command=lambda val=temp_value, x=test3[i], s=station:handler(val, x, s))
        detail_list.append(tmp)
        
        counter = counter + 1
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
    for i in city:
        if i['text'] == chinese_name:
            ypos = i.winfo_rooty() - i.winfo_height()
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
 
def update_data():
    t1 = threading.Thread(target=main_fun)
    t1.start()
#=========================================main program================================================

if __name__ == '__main__':

    window = tk.Tk()
    window.geometry("700x600+300+10")
    window.title("Python期末專題-空氣指標小工具")
    window.configure(background='white')
    # menu
    menu = Menu(window)
    window.config(menu=menu)
    menu.add_cascade(label='update', command=update_data)
    #window.attributes('-alpha', 0.9)

    btn_frame = Frame(window, relief=GROOVE, bg='purple').pack() # save main btns
    var = tk.StringVar()#文字變亮儲存器
    taiwan = ImageTk.PhotoImage(Image.open('photo/taiwan-total.png'))
    btn_close = Button(window)
    label2 = Label(window)
    label3 = Label(window)
    city = []
    detail_list = []
    label_list = []
    area = {'北部':'North', '竹苗':'Chu-Miao', '中部':'Central', '雲嘉南':'Yun-Chia-Nan',
            '高屏':'KaoPing', '宜蘭':'Yilan', '花東':'Hua-Tung', '馬祖':'Matsu', '金門':'Kinmen', '馬公':'Magong'}

    # photo of taiwan
    ptaiwan = Label(window, image=taiwan, bg='white')
    ptaiwan.pack(side=RIGHT)
    
    # the area button
    for x in area.keys():
        tmp_button = HoverButton(btn_frame, compound = CENTER, bg='purple', fg='white', activebackground='orchid3', text = x, font = ('Arial',"14","bold"),
                            command=lambda val=area[x]: select_area(val), relief=FLAT)
        city.append(tmp_button)

    count =0
    # set places
    for i in city:
        i.place(x=0, y = 60*(count), width = 134, height = 60)
        count = count + 1
    
                        
    #data : AQI(空氣品質) 臭氧 細懸浮微粒 懸浮微粒 一氧化碳 二氧化硫 二氧化氮
            

    window.mainloop()

