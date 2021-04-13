from kakaomap import kakaomap_search

import requests, bs4
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import time
import pandas as pd

def api_2(address):

    kakaodata = kakaomap_search(address)

    decode_key = 'qxYCqkstCZ8XGIddZD07gVxLSNV8Ivpcp4QNatFfp4nS3lmhVB4kg1F4+PoFnHGjlKViFlvHtKGzNpcR4WIHbw=='
    url = 'http://apis.data.go.kr/1613000/BldRgstService_v2/getBrTitleInfo'
    queryParams = ('?' +
                   urlencode({quote_plus('ServiceKey'): decode_key,
                              quote_plus('sigunguCd'): (kakaodata[0][1][:5]),
                              quote_plus('bjdongCd'): (kakaodata[0][1][5:]),
                              quote_plus('platGbCd'): kakaodata[3],
                              quote_plus('bun'): kakaodata[1],
                              quote_plus('ji'): kakaodata[2],
                              #                           quote_plus('startDate') : '',
                              #                           quote_plus('endDate') : '',
                              quote_plus('numOfRows'): '1000',
                              #                           quote_plus('pageNo') : '10'
                              }))

    request = Request(url + queryParams)
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()
    response_body = response_body.decode('utf-8')

    xmlobj = bs4.BeautifulSoup(response_body, 'lxml-xml')

    xmlobj = bs4.BeautifulSoup(response_body, 'lxml-xml')
    rows = xmlobj.findAll('item')
    columns = rows[0].find_all()

    rowList = []
    nameList = []
    columnList = []

    rowsLen = len(rows)
    for i in range(0, rowsLen):
        columns = rows[i].find_all()

        columnsLen = len(columns)
        for j in range(0, columnsLen):
            if i == 0:
                nameList.append(columns[j].name)

            eachColumn = columns[j].text
            columnList.append(eachColumn)

        rowList.append(columnList)
        columnList = []

    nameList[0] = "건축면적(㎡)"
    nameList[1] = "부속건축물면적(㎡)"
    nameList[2] = "부속건축물수"
    nameList[3] = "건폐율(%)"
    nameList[4] = "법정동코드"
    nameList[5] = "건물명"
    nameList[6] = "블록"
    nameList[7] = "번"
    nameList[8] = "외필지수"
    nameList[9] = "생성일자"
    nameList[10] = "동명칭"
    nameList[11] = "비상용승강기수"
    nameList[12] = "EPI점수"
    nameList[13] = "에너지효율등급"
    nameList[14] = "에너지절감율"
    nameList[15] = "기타용도"
    nameList[16] = "기타지붕"
    nameList[17] = "기타구조"
    nameList[18] = "가구수(가구)"
    nameList[19] = "친환경건축물인증점수"
    nameList[20] = "친환경건축물등급"
    nameList[21] = "지상층수"
    nameList[22] = "높이(m)"
    nameList[23] = "세대수(세대)"
    nameList[24] = "호수(호)"
    nameList[25] = "옥내자주식면적(㎡)"
    nameList[26] = "옥내자주식대수(대)"
    nameList[27] = "옥내기계식면적(㎡)"
    nameList[28] = "옥내기계식대수(대)"
    nameList[29] = "지능형건축물인증점수"
    nameList[30] = "지능형건축물등급"
    nameList[31] = "지"
    nameList[32] = "로트"
    nameList[33] = "주부속구분코드"
    nameList[34] = "주부속구분코드명"
    nameList[35] = "주용도코드"
    nameList[36] = "주용도코드명"
    nameList[37] = "관리건축물대장PK"
    nameList[38] = "새주소법정동코드"
    nameList[39] = "새주소본번"
    nameList[40] = "새주소도로코드"
    nameList[41] = "새주소부번"
    nameList[42] = "새주소지상지하코드"
    nameList[43] = "도로명주소"
    nameList[44] = "옥외자주식면적(㎡)"
    nameList[45] = "옥외자주식대수(대)"
    nameList[46] = "옥외기계식면적(㎡)"
    nameList[47] = "옥외기계식대수(대)"
    nameList[48] = "대지면적(㎡)"
    nameList[49] = "대지구분코드"
    nameList[50] = "구 주소"


    result = pd.DataFrame(rowList, columns=nameList)

    in_name = (
        "법정동코드", "생성일자", "번", "지", "주부속구분코드", "주용도코드", "관리건축물대장PK", "새주소법정동코드",
        "새주소본번", "새주소도로코드", "새주소부번", "새주소지상지하코드", "대지구분코드"
    )

    for i in range(len(in_name)):
        del result[in_name[i]]

    timestr = time.strftime("%Y-%m-%d %H%M%S")

    result.to_excel(excel_writer=timestr + ' main ' + address + '.xlsx')

    print("api_2 complete")