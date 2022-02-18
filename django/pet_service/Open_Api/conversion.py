import requests
import json
# rest api
api_key = 'b8b58dd6490543a58e8ab1ea5352a75f'
# 주소로 좌표변환
def addr_to_lat_lon(addr):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query={address}'.format(address=addr)
    api = {"Authorization": "KakaoAK " + api_key}
    result = json.loads(str(requests.get(url, headers=api).text))
    found = result['documents'][0]['address']
    # return float(found['x']), float(found['y'])
    return float(found['y']), float(found['x'])


# print(addr_to_lat_lon('서울특별시 강남구 도곡로 174, 1,2층 (도곡동)'))
# (37.4979313896033, 126.871013564548)
# (37.4985987300398, 126.871229657654)
# 좌표로 주소 변환
def lat_lon_to_addr(lon,lat):
    url = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={longitude}&y={latitude}'.format(longitude=lon,latitude=lat)
    api = {"Authorization": "KakaoAK " + api_key}
    result = json.loads(str(requests.get(url, headers=api).text))
    found = result['documents'][0]['address_name']
    return str(found)

# print(lat_lon_to_addr('126.974907969051', '37.5696996246023'))