'''
1. json -> keypoint 추출 -> filtered_keypoints.csv -> 데이터프레임 생성 -> 시각화
2. json -> one_json -> yolo prediction moddel train 
'''
import os
import json
import pandas as pd

# 1. JSON 파일이 있는 폴더 경로 설정
folder_path = '/Users/kimseohee/Desktop/Autonomous-Pedestrian-Prediction-with-Talchum-Motion-Data/Data/Data_TL'

# 2. 사용할 주요 keypoint 목록 설정
keypoints = ['head', 'neck', 'left_shoulder', 'right_shoulder', 
             'left_ankle', 'right_ankle', 'left_wrist', 'right_wrist']

# 3. 데이터를 저장할 리스트 초기화
data_all_json = []  # 모든 JSON 데이터를 저장
keypoint_data = []  # 특정 keypoint 데이터를 저장

# 4. 폴더 내 모든 JSON 파일 읽고 처리
for file_name in os.listdir(folder_path):
    if file_name.endswith('.json'):  # JSON 파일만 처리
        file_path = os.path.join(folder_path, file_name)
        
        with open(file_path, 'r') as file:
            data = json.load(file)  # JSON 파일 불러오기
            data_all_json.append(data)  # 원본 데이터 저장
            
            # annotation에서 keypoint 추출
            for annotation in data['annotation_info']['annotation']:
                dancer_height = data['Dancer_info']['dancer_hight']  # 키 정보 추출
                for point in annotation['keypoint']:
                    if point['keypoint_name'] in keypoints:  # 주요 keypoint만 필터링
                        keypoint_data.append({
                            'file_name': file_name,        # 파일 이름
                            'dancer_height': dancer_height, # 키 정보
                            'keypoint_name': point['keypoint_name'],
                            'x': point['x'],               # keypoint x 좌표
                            'y': point['y']                # keypoint y 좌표
                        })

# 5. DataFrame 생성
df = pd.DataFrame(keypoint_data)

# 결과 확인
print(f"Loaded {len(data_all_json)} JSON files")  # 전체 JSON 파일 개수
print("Extracted Keypoints DataFrame:")
print(df.head())  # 추출된 데이터프레임 확인

# 6. 데이터프레임 저장 (CSV 파일)
output_path = 'filtered_keypoints.csv'
df.to_csv(output_path, index=False)
print(f"Filtered keypoints saved to '{output_path}'")
