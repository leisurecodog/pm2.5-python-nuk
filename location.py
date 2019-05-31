import requests
import json
# get ip
def get_pos():
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    my_ip = ip_request.json()['ip'] 

    # use ip to get latitude and longitude
    url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
    geo_request = requests.get(url)
    print(geo_request.json())
    geo_latitude = geo_request.json()['latitude']
    geo_longitude = geo_request.json()['longitude']
    return geo_latitude,geo_longitude



if __name__ == '__main__':
    a, b = get_pos()
    print(a,b,sep=', ')

