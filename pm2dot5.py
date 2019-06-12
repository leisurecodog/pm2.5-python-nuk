import re
import requests
import sys
import time
import threading
from datetime import datetime, timedelta
from bs4 import BeautifulSoup



def catch():
    """
        抓氣象局PM2.5等等的資料

    """
    area = ['/North', '/Chu-Miao', '/Yilan', '/Hua-Tung', '/Yun-Chia-Nan', '/Central', '/KaoPing', 'Island/Matsu', 'Island/Kinmen', 'Island/Magong']
    area_file_name = ['North', 'Chu-Miao', 'Yilan', 'Hua-Tung', 'Yun-Chia-Nan', 'Central', 'KaoPing', 'Matsu', 'Kinmen', 'Magong']
    for area_name, area_file_name in zip(area, area_file_name):

        url = 'https://taqm.epa.gov.tw/taqm/tw/Aqi' + area_name + '.aspx?fm=AqiMap'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        #print(soup.prettify())
        
        station = {}
        soup_href = soup.find_all("a", id=re.compile("^ctl05_gv_ctl"))
        station = {s.text: [] for s in soup_href}


        #AQI1    
        soup_AQI1 = soup.find_all(id=re.compile("^ctl05_gv_ctl(\d\d)_labPSI"))
        for s, i in zip(soup_AQI1, station.keys()):
            if s.text == '':
                station[i].append('-1')
                continue
            
            station[i].append(s.text)

        #ppb
        soup_ppb = soup.find_all(id=re.compile("^ctl05_gv_ctl(\d\d)_labO3"))
        for s, i in zip(soup_ppb, station.keys()):
            if s.text == '':
                station[i].append('-1')
                continue
            station[i].append(s.text)

        #PM25
        soup_PM25 = soup.find_all(id=re.compile("^ctl05_gv_ctl(\d\d)_labPM25"))
        for s, i in zip(soup_PM25, station.keys()):
            if s.text == '':
                station[i].append('-1')
                continue
            station[i].append(s.text)

        #PM10
        soup_PM10 = soup.find_all(id=re.compile("^ctl05_gv_ctl(\d\d)_labPM10"))
        for s, i in zip(soup_PM10, station.keys()):
            if s.text == '':
                station[i].append('-1')
                continue
            station[i].append(s.text)

        #CO
        soup_CO = soup.find_all(id=re.compile("^ctl05_gv_ctl(\d\d)_labCO"))
        for s, i in zip(soup_CO, station.keys()):
            if s.text == '':
                station[i].append('-1')
                continue
            station[i].append(s.text)

        #SO2
        soup_SO2 = soup.find_all(id=re.compile("^ctl05_gv_ctl(\d\d)_labSO2"))
        for s, i in zip(soup_SO2, station.keys()):
            if s.text == '':
                station[i].append('-1')
                continue
            station[i].append(s.text)

        #NO2
        soup_NO2 = soup.find_
        soup_NO2 = soup.find_all(id=re.compile("^ctl05_gv_ctl(\d\d)_labNO2"))
        for s, i in zip(soup_NO2, station.keys()):
            if s.text == '':
                station[i].append('-1')
                continue
            station[i].append(s.text)


        with open('area/' + area_file_name + '.txt', 'w') as file:
            for k, v in station.items():
                file.writelines([k, '\n', ' '.join(v), '\n'])
def main_fun():
    catch()
    print("Finish!")
    now = datetime.now()
    
    time_wait = 3600 - (now.minute * 60 + now.second) + 300
    first = threading.Timer(time_wait, main_fun)
    first.start()



if __name__ == '__main__':
    main_fun()
    catch()








