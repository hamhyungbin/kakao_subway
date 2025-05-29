# app.py (카카오 API 버전)
import os
import json
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Render에 설정할 새로운 카카오 REST API 키
KAKAO_REST_API_KEY = os.environ.get('KAKAO_REST_API_KEY')

# 예시 좌표 (경도,위도 순서)
STATION_COORDS = {
    '222': '127.02761,37.49794', # 강남역
    '216': '127.10022,37.51336'  # 잠실역
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_route')
def search_route():
    start_station_id = request.args.get('start_station')
    end_station_id = request.args.get('end_station')

    if not start_station_id or not end_station_id:
        return "출발역과 도착역 ID를 모두 입력해주세요."

    start_coords = STATION_COORDS.get(start_station_id)
    end_coords = STATION_COORDS.get(end_station_id)
    
    if not start_coords or not end_coords:
        return f"좌표를 찾을 수 없는 역 ID가 포함되어 있습니다: {start_station_id}, {end_station_id}"

    # 카카오 모빌리티 길찾기 API URL
    api_url = "https://apis-navi.kakaomobility.com/v1/directions"
    
    # 요청 파라미터 및 헤더 설정
    params = {
        'origin': start_coords,
        'destination': end_coords
    }
    headers = {
        "Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"
    }

    try:
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        # 카카오 API는 'routes' 키가 있는지로 성공 여부 판단 가능
        if 'routes' not in data or not data['routes']:
             return f"API 오류가 발생했습니다: {data.get('error', {}).get('msg', '경로를 찾을 수 없습니다.')}"
        
        # 첫 번째 경로를 결과로 사용
        path_data = data['routes'][0]

        return render_template('result_kakao.html', path_data=path_data)

    except requests.exceptions.RequestException as e:
        return f"API 서버에 연결하는 중 오류가 발생했습니다: {e}"

# 로컬 테스트용
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)