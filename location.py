import requests
import json
# get ip
def get_pos():
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    my_ip = ip_request.json()['ip'] 

    # use ip to get latitude and longitude
    url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
    geo_request = requests.get(url)
    dic = geo_request.json()
    return dic



if __name__ == '__main__':
    dic = get_pos()
    print(dic['city'])

