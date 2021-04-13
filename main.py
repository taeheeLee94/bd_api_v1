from kakaomap import kakaomap_search
from openapi_1 import api_1
from openapi_2 import api_2

print("주소를 입력하세요: ", end="")
address = input()

kakaomap_search(address)
api_1(address)
api_2(address)