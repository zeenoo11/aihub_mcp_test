import subprocess
import json
import os
from typing import Optional, Dict, List, Any
import sys


class AIHubAPI:
    """AI-Hub API를 통해 데이터셋을 조회하고 관리하는 클래스"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        AIHubAPI 인스턴스 초기화
        
        Args:
            api_key (str, optional): AI-Hub API 키. 환경변수 AIHUB_API_KEY에서도 가져올 수 있음
        """
        self.api_key = api_key or os.getenv('AIHUB_API_KEY')
        if not self.api_key:
            print("경고: API 키가 설정되지 않았습니다. 환경변수 AIHUB_API_KEY를 설정하거나 생성자에 api_key를 전달하세요.")
    
    def _run_aihubshell(self, *args) -> str:
        """
        aihubshell 명령어를 실행하고 결과를 반환
        
        Args:
            *args: aihubshell에 전달할 인수들
            
        Returns:
            str: 명령어 실행 결과
        """
        try:
            cmd = ['aihubshell'] + list(args)
            if self.api_key:
                cmd.extend(['--aihubapikey', self.api_key])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode != 0:
                raise Exception(f"aihubshell 실행 오류: {result.stderr}")
            
            return result.stdout
        
        except FileNotFoundError:
            raise Exception("aihubshell이 설치되어 있지 않습니다. AI-Hub에서 aihubshell을 다운로드하여 설치하세요.")
        except Exception as e:
            raise Exception(f"명령어 실행 중 오류 발생: {str(e)}")
    
    def list_datasets(self, dataset_key: Optional[str] = None) -> str:
        """
        데이터셋 목록을 조회
        
        Args:
            dataset_key (str, optional): 특정 데이터셋 키. 없으면 전체 목록 조회
            
        Returns:
            str: 데이터셋 목록 정보
        """
        args = ['--mode', 'l']
        if dataset_key:
            args.extend(['--datasetkey', dataset_key])
        
        return self._run_aihubshell(*args)
    
    def get_dataset_info(self, dataset_key: str) -> str:
        """
        특정 데이터셋의 상세 정보 조회
        
        Args:
            dataset_key (str): 조회할 데이터셋 키
            
        Returns:
            str: 데이터셋 상세 정보
        """
        return self.list_datasets(dataset_key)
    
    def list_files(self, dataset_key: str, file_key: Optional[str] = None) -> str:
        """
        데이터셋의 파일 목록 조회
        
        Args:
            dataset_key (str): 데이터셋 키
            file_key (str, optional): 특정 파일 키
            
        Returns:
            str: 파일 목록 정보
        """
        args = ['--mode', 'l', '--datasetkey', dataset_key]
        if file_key:
            args.extend(['--filekey', file_key])
        
        return self._run_aihubshell(*args)
    
    def download_dataset(self, dataset_key: str, file_key: Optional[str] = None, 
                        output_path: Optional[str] = None) -> str:
        """
        데이터셋 다운로드
        
        Args:
            dataset_key (str): 다운로드할 데이터셋 키
            file_key (str, optional): 특정 파일 키
            output_path (str, optional): 다운로드 경로
            
        Returns:
            str: 다운로드 결과
        """
        args = ['--mode', 'd', '--datasetkey', dataset_key]
        if file_key:
            args.extend(['--filekey', file_key])
        if output_path:
            args.extend(['--output', output_path])
        
        return self._run_aihubshell(*args)


def main():
    """메인 함수 - 사용 예시"""
    print("=== AI-Hub 데이터셋 조회 도구 ===\n")
    
    # API 키 확인
    api_key = input("AI-Hub API 키를 입력하세요 (엔터를 누르면 환경변수에서 가져옴): ").strip()
    if not api_key:
        api_key = None
    
    try:
        # AIHubAPI 인스턴스 생성
        aihub = AIHubAPI(api_key)
        
        while True:
            print("\n=== 메뉴 ===")
            print("1. 전체 데이터셋 목록 조회")
            print("2. 특정 데이터셋 상세 정보 조회")
            print("3. 데이터셋 파일 목록 조회")
            print("4. 데이터셋 다운로드")
            print("5. 종료")
            
            choice = input("\n선택하세요 (1-5): ").strip()
            
            if choice == '1':
                print("\n전체 데이터셋 목록을 조회합니다...")
                try:
                    result = aihub.list_datasets()
                    print(result)
                except Exception as e:
                    print(f"오류: {e}")
            
            elif choice == '2':
                dataset_key = input("데이터셋 키를 입력하세요: ").strip()
                if dataset_key:
                    try:
                        result = aihub.get_dataset_info(dataset_key)
                        print(f"\n데이터셋 '{dataset_key}' 정보:")
                        print(result)
                    except Exception as e:
                        print(f"오류: {e}")
                else:
                    print("데이터셋 키를 입력해주세요.")
            
            elif choice == '3':
                dataset_key = input("데이터셋 키를 입력하세요: ").strip()
                if dataset_key:
                    file_key = input("파일 키를 입력하세요 (선택사항, 엔터로 건너뛰기): ").strip()
                    try:
                        result = aihub.list_files(dataset_key, file_key if file_key else None)
                        print(f"\n데이터셋 '{dataset_key}' 파일 목록:")
                        print(result)
                    except Exception as e:
                        print(f"오류: {e}")
                else:
                    print("데이터셋 키를 입력해주세요.")
            
            elif choice == '4':
                dataset_key = input("다운로드할 데이터셋 키를 입력하세요: ").strip()
                if dataset_key:
                    file_key = input("파일 키를 입력하세요 (선택사항, 엔터로 건너뛰기): ").strip()
                    output_path = input("다운로드 경로를 입력하세요 (선택사항, 엔터로 건너뛰기): ").strip()
                    
                    try:
                        print(f"\n데이터셋 '{dataset_key}' 다운로드를 시작합니다...")
                        result = aihub.download_dataset(
                            dataset_key, 
                            file_key if file_key else None,
                            output_path if output_path else None
                        )
                        print("다운로드 완료:")
                        print(result)
                    except Exception as e:
                        print(f"오류: {e}")
                else:
                    print("데이터셋 키를 입력해주세요.")
            
            elif choice == '5':
                print("프로그램을 종료합니다.")
                break
            
            else:
                print("잘못된 선택입니다. 1-5 중에서 선택해주세요.")
    
    except KeyboardInterrupt:
        print("\n\n프로그램이 중단되었습니다.")
    except Exception as e:
        print(f"예상치 못한 오류가 발생했습니다: {e}")


if __name__ == "__main__":
    main() 