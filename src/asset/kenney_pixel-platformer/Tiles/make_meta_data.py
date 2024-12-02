import os
import json
from PIL import Image, PngImagePlugin


def add_metadata_to_png_from_json(json_path, folder_path):
    # JSON 파일 로드
    with open(json_path, "r") as json_file:
        metadata_dict = json.load(json_file)

    for file_name, metadata in metadata_dict.items():
        try:
            # 이미지 파일 경로
            input_path = os.path.join(folder_path, file_name)

            if not os.path.isfile(input_path):
                print(f"Skipping {file_name}, file not found.")
                continue

            # 이미지 열기
            image = Image.open(input_path)
            metadata_plugin = PngImagePlugin.PngInfo()

            # 메타데이터 추가
            for key, value in metadata.items():
                metadata_plugin.add_text(key, value)

            # 덮어쓰기 저장
            image.save(input_path, "PNG", pnginfo=metadata_plugin)
            print(f"Metadata added to {file_name}")
        except Exception as e:
            print(f"Error processing {file_name}: {e}")


# JSON 파일 경로와 이미지 폴더 경로 설정
json_path = "metadata.json"  # JSON 파일 경로
folder_path = "./"  # 이미지가 저장된 폴더 경로

# 실행
add_metadata_to_png_from_json(json_path, folder_path)
