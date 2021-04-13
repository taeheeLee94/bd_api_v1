import requests
from urllib.parse import urlparse
import pandas as pd

def kakaomap_search(address):
    url = "https://dapi.kakao.com/v2/local/search/address.json?query=" + address
    result = requests.get(urlparse(url).geturl(), headers={"Authorization": "KakaoAK 3c53094cf92240765e2a2b0acd32bce4"})
    json_obj = result.json()

    list = []
    for document in json_obj['documents']:
        val = [document['road_address']['building_name'], document['address']['b_code'], document['address_name'],
               document['y'], document['x']]
        list.append(val)

    df = pd.DataFrame(list, columns=['building_name', 'b_code', 'address_name', 'lat', 'lon'])
    textInput = df['b_code'][0]

    mt = document['address']['mountain_yn']

    if mt == 'Y':
        mt = 1
    else:
        mt = 0

    bun = document['address']['main_address_no']
    ji = document['address']['sub_address_no']

    for i in range(0, 4):
        if len(bun) == 4:
            break
        else:
            bun = '0' + bun

    for i in range(0, 4):
        if len(ji) == 4:
            break
        else:
            ji = '0' + ji

    result = list + [bun] + [ji] + [str(mt)]
    return result