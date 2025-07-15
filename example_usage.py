#!/usr/bin/env python3
"""
AI-Hub 데이터셋 조회 도구 - 간단한 사용 예시
이 스크립트는 AIHubAPI 클래스의 기본적인 사용법을 보여줍니다.
"""

from aihub_dataset_query import AIHubAPI
import os


def example_basic_usage():
    """기본 사용법 예시"""
    print("=== AI-Hub API 기본 사용법 예시 ===\n")
    
    # 환경변수에서 API 키 가져오기 (또는 직접 입력)
    api_key = os.getenv('AIHUB_API_KEY')
    if not api_key:
        api_key = input("AI-Hub API 키를 입력하세요: ").strip()
        if not api_key:
            print("API 키가 필요합니다. 프로그램을 종료합니다.")
            return
    
    try:
        # AIHubAPI 인스턴스 생성
        aihub = AIHubAPI(api_key)
        
        # 1. 전체 데이터셋 목록 조회
        print("1. 전체 데이터셋 목록 조회 중...")
        print("-" * 50)
        datasets = aihub.list_datasets()
        print(datasets[:500])  # 처음 500자만 출력
        if len(datasets) > 500:
            print("... (출력 결과가 길어서 일부만 표시됨)")
        print()
        
        # 2. 사용자에게 데이터셋 키 입력 받기
        dataset_key = input("조회할 데이터셋 키를 입력하세요 (없으면 엔터): ").strip()
        
        if dataset_key:
            # 3. 특정 데이터셋 상세 정보 조회
            print(f"\n2. 데이터셋 '{dataset_key}' 상세 정보 조회 중...")
            print("-" * 50)
            dataset_info = aihub.get_dataset_info(dataset_key)
            print(dataset_info)
            print()
            
            # 4. 데이터셋 파일 목록 조회
            print(f"3. 데이터셋 '{dataset_key}' 파일 목록 조회 중...")
            print("-" * 50)
            files = aihub.list_files(dataset_key)
            print(files)
            print()
            
            # 5. 다운로드 여부 확인
            download_choice = input("이 데이터셋을 다운로드하시겠습니까? (y/N): ").strip().lower()
            if download_choice in ['y', 'yes']:
                output_path = input("다운로드 경로를 입력하세요 (기본값: ./downloads): ").strip()
                if not output_path:
                    output_path = "./downloads"
                
                print(f"\n4. 데이터셋 '{dataset_key}' 다운로드 시작...")
                print("-" * 50)
                
                # 다운로드 디렉토리 생성
                os.makedirs(output_path, exist_ok=True)
                
                result = aihub.download_dataset(dataset_key, output_path=output_path)
                print("다운로드 완료!")
                print(result)
        else:
            print("데이터셋 키가 입력되지 않아 상세 조회를 건너뜁니다.")
            
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
        print("다음 사항을 확인해주세요:")
        print("1. aihubshell이 설치되어 있는지")
        print("2. API 키가 올바른지")
        print("3. 인터넷 연결이 되어 있는지")


def example_programmatic_usage():
    """프로그래밍 방식 사용법 예시"""
    print("\n\n=== 프로그래밍 방식 사용법 예시 ===\n")
    
    # API 키 설정
    api_key = os.getenv('AIHUB_API_KEY', 'your_api_key_here')
    
    try:
        # AIHubAPI 인스턴스 생성
        aihub = AIHubAPI(api_key)
        
        # 예시 코드 출력
        example_code = '''
# AI-Hub API 사용 예시 코드

from aihub_dataset_query import AIHubAPI
import os

# 1. API 인스턴스 생성
aihub = AIHubAPI(api_key="your_api_key_here")
# 또는 환경변수 사용
aihub = AIHubAPI()  # AIHUB_API_KEY 환경변수에서 자동으로 가져옴

# 2. 전체 데이터셋 목록 조회
datasets = aihub.list_datasets()
print("전체 데이터셋:", datasets)

# 3. 특정 데이터셋 정보 조회
dataset_key = "your_dataset_key"
dataset_info = aihub.get_dataset_info(dataset_key)
print(f"데이터셋 {dataset_key} 정보:", dataset_info)

# 4. 데이터셋 파일 목록 조회
files = aihub.list_files(dataset_key)
print(f"파일 목록:", files)

# 5. 특정 파일 정보 조회
file_key = "your_file_key"
file_info = aihub.list_files(dataset_key, file_key)
print(f"파일 {file_key} 정보:", file_info)

# 6. 데이터셋 다운로드
download_result = aihub.download_dataset(
    dataset_key=dataset_key,
    output_path="./my_datasets"
)
print("다운로드 결과:", download_result)

# 7. 특정 파일만 다운로드
file_download_result = aihub.download_dataset(
    dataset_key=dataset_key,
    file_key=file_key,
    output_path="./my_files"
)
print("파일 다운로드 결과:", file_download_result)
'''
        
        print("다음은 AIHubAPI를 프로그래밍 방식으로 사용하는 예시입니다:")
        print(example_code)
        
    except Exception as e:
        print(f"예시 코드 표시 중 오류 발생: {e}")


if __name__ == "__main__":
    print("AI-Hub 데이터셋 조회 도구 - 사용 예시\n")
    
    try:
        # 기본 대화형 사용법
        example_basic_usage()
        
        # 프로그래밍 방식 예시 코드 보기
        show_code = input("\n프로그래밍 방식 예시 코드를 보시겠습니까? (y/N): ").strip().lower()
        if show_code in ['y', 'yes']:
            example_programmatic_usage()
            
        print("\n사용 예시를 마칩니다. 감사합니다!")
        
    except KeyboardInterrupt:
        print("\n\n프로그램이 중단되었습니다.")
    except Exception as e:
        print(f"\n예상치 못한 오류가 발생했습니다: {e}") 