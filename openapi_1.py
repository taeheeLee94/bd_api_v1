from kakaomap import kakaomap_search

import requests, bs4
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import time
import pandas as pd

def api_1(address):

    kakaodata = kakaomap_search(address)

    decode_key = 'qxYCqkstCZ8XGIddZD07gVxLSNV8Ivpcp4QNatFfp4nS3lmhVB4kg1F4+PoFnHGjlKViFlvHtKGzNpcR4WIHbw=='
    url = 'http://apis.data.go.kr/1613000/BldRgstService_v2/getBrFlrOulnInfo'
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
    rows = xmlobj.findAll('item')

    columns = rows[0].find_all()

    rowList = []
    nameList = []
    columnList = []

    rowsLen = len(rows)

    timestr = time.strftime("%Y-%m-%d %H%M%S")

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

    nameList[0] = "면적"
    nameList[1] = "면적제외여부"
    nameList[2] = "법정동코드"
    nameList[3] = "건물명"
    nameList[4] = "블록"
    nameList[5] = "번(지)"
    nameList[6] = "생성일자"
    nameList[7] = "동명칭"
    nameList[8] = "기타용도"
    nameList[9] = "기타구조"
    nameList[10] = "층구분코드"
    nameList[11] = "층구분코드명"
    nameList[12] = "층번호"
    nameList[13] = "층번호명"
    nameList[14] = "(번)지"
    nameList[15] = "로트"
    nameList[16] = "주부속구분코드"
    nameList[17] = "주부속구분코드명"
    nameList[18] = "주용도코드"
    nameList[19] = "주용도코드명"
    nameList[20] = "관리건축물대장PK"
    nameList[21] = "새주소법정동코드"
    nameList[22] = "새주소본번"
    nameList[23] = "새주소도로코드"
    nameList[24] = "새주소부번"
    nameList[25] = "새주소지상지하코드"
    nameList[26] = "도로명대지위치"
    nameList[27] = "대지구분코드"
    nameList[28] = "대지위치"
    nameList[29] = "순번"
    nameList[30] = "시군구코드"
    nameList[31] = "특수지명"
    nameList[32] = "구조코드"
    nameList[33] = "구조코드명"

    result = pd.DataFrame(rowList, columns=nameList)

    in_name = (
        "면적제외여부", "법정동코드", "블록", "번(지)", "생성일자", "층구분코드", "(번)지", "로트",
        "주부속구분코드", "주용도코드", "관리건축물대장PK", "새주소법정동코드", "새주소본번",
        "새주소도로코드", "새주소부번", "새주소지상지하코드", "대지구분코드", "시군구코드",
        "특수지명", "구조코드"
    )

    for i in range(len(in_name)):
        del result[in_name[i]]

    result.to_excel(excel_writer=timestr + ' sub ' + address + '.xlsx')

    print("api_1 complete")