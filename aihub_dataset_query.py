#!/usr/bin/env python3
"""
AI-Hub 데이터셋 조회 도구 - 대화형 인터페이스
새로운 AIHubClient를 사용하여 실제 AI-Hub API와 통신
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional

from aihub_client import AIHubClient, AIHubAPIError, AIHubAuthError


class AIHubCLI:
    """AI-Hub 명령줄 인터페이스"""
    
    def __init__(self):
        self.client: Optional[AIHubClient] = None
        self.api_key: Optional[str] = None
    
    def initialize_client(self, api_key: Optional[str] = None) -> bool:
        """
        AI-Hub 클라이언트 초기화
        
        Args:
            api_key: API 키
            
        Returns:
            초기화 성공 여부
        """
        try:
            self.client = AIHubClient(api_key=api_key)
            self.api_key = self.client.api_key
            
            # API 키 유효성 검증
            if not self.client.validate_api_key():
                print("❌ API 키가 유효하지 않습니다.")
                return False
            
            print("✅ API 키 검증 완료")
            return True
            
        except AIHubAuthError as e:
            print(f"❌ 인증 오류: {e}")
            return False
        except AIHubAPIError as e:
            print(f"❌ API 오류: {e}")
            return False
        except Exception as e:
            print(f"❌ 예상치 못한 오류: {e}")
            return False
    
    def display_menu(self):
        """메인 메뉴 표시"""
        print("\n" + "="*50)
        print("         AI-Hub 데이터셋 조회 도구")
        print("="*50)
        print("1. 전체 데이터셋 목록 조회")
        print("2. 특정 데이터셋 상세 정보 조회")
        print("3. API 매뉴얼 조회")
        print("4. 데이터셋 다운로드")
        print("5. API 키 재설정")
        print("6. 종료")
        print("="*50)
    
    def list_datasets(self):
        """전체 데이터셋 목록 조회"""
        try:
            print("\n📋 전체 데이터셋 목록을 조회하고 있습니다...")
            datasets = self.client.get_datasets()
            
            # JSON 응답 파싱 및 표시
            if isinstance(datasets, dict) and 'raw_response' in datasets:
                # Raw 텍스트 응답인 경우
                print("\n응답:")
                print(datasets['raw_response'][:1000])  # 처음 1000자만 표시
                if len(datasets['raw_response']) > 1000:
                    print("... (응답이 길어서 일부만 표시됨)")
            else:
                # JSON 응답인 경우
                print(f"\n📊 조회 결과:")
                print(json.dumps(datasets, indent=2, ensure_ascii=False)[:1500])
                if len(str(datasets)) > 1500:
                    print("... (결과가 길어서 일부만 표시됨)")
                    
        except AIHubAPIError as e:
            print(f"❌ 데이터셋 목록 조회 실패: {e}")
        except Exception as e:
            print(f"❌ 예상치 못한 오류: {e}")
    
    def get_dataset_info(self):
        """특정 데이터셋 상세 정보 조회"""
        dataset_key = input("\n🔍 조회할 데이터셋 키를 입력하세요: ").strip()
        
        if not dataset_key:
            print("❌ 데이터셋 키를 입력해주세요.")
            return
        
        try:
            print(f"\n📄 데이터셋 '{dataset_key}' 정보를 조회하고 있습니다...")
            dataset_info = self.client.get_dataset_info(dataset_key)
            
            # 결과 표시
            if isinstance(dataset_info, dict) and 'raw_response' in dataset_info:
                print("\n응답:")
                print(dataset_info['raw_response'][:1000])
                if len(dataset_info['raw_response']) > 1000:
                    print("... (응답이 길어서 일부만 표시됨)")
            else:
                print(f"\n📊 데이터셋 '{dataset_key}' 정보:")
                print(json.dumps(dataset_info, indent=2, ensure_ascii=False)[:1500])
                if len(str(dataset_info)) > 1500:
                    print("... (결과가 길어서 일부만 표시됨)")
                    
        except AIHubAPIError as e:
            print(f"❌ 데이터셋 정보 조회 실패: {e}")
        except Exception as e:
            print(f"❌ 예상치 못한 오류: {e}")
    
    def get_api_manual(self):
        """API 매뉴얼 조회"""
        try:
            print("\n📚 API 매뉴얼을 조회하고 있습니다...")
            manual = self.client.get_api_manual()
            
            # 결과 표시
            if isinstance(manual, dict) and 'raw_response' in manual:
                print("\n📖 API 매뉴얼:")
                print(manual['raw_response'][:1000])
                if len(manual['raw_response']) > 1000:
                    print("... (매뉴얼이 길어서 일부만 표시됨)")
            else:
                print("\n📖 API 매뉴얼:")
                print(json.dumps(manual, indent=2, ensure_ascii=False)[:1500])
                if len(str(manual)) > 1500:
                    print("... (결과가 길어서 일부만 표시됨)")
                    
        except AIHubAPIError as e:
            print(f"❌ API 매뉴얼 조회 실패: {e}")
        except Exception as e:
            print(f"❌ 예상치 못한 오류: {e}")
    
    def download_dataset(self):
        """데이터셋 다운로드"""
        print("\n⬇️ 데이터셋 다운로드")
        
        # 데이터셋 키 입력
        dataset_key = input("데이터셋 키를 입력하세요: ").strip()
        if not dataset_key:
            print("❌ 데이터셋 키를 입력해주세요.")
            return
        
        # 파일 키 입력 (선택사항)
        file_keys_input = input("파일 키를 입력하세요 (전체 다운로드는 엔터, 여러 개는 쉼표로 구분): ").strip()
        file_keys = None
        if file_keys_input:
            if ',' in file_keys_input:
                file_keys = [key.strip() for key in file_keys_input.split(',')]
            else:
                file_keys = file_keys_input
        
        # 출력 경로 입력
        output_path = input(f"다운로드 경로를 입력하세요 (기본값: {self.client.default_download_path}): ").strip()
        if not output_path:
            output_path = None
        
        # 압축 해제 여부
        extract_choice = input("다운로드 후 자동으로 압축을 해제하시겠습니까? (Y/n): ").strip().lower()
        extract = extract_choice not in ['n', 'no']
        
        try:
            print(f"\n📥 데이터셋 '{dataset_key}' 다운로드를 시작합니다...")
            
            result = self.client.download_dataset(
                dataset_key=dataset_key,
                file_keys=file_keys,
                output_path=output_path,
                extract=extract,
                show_progress=True
            )
            
            # 결과 표시
            print(f"\n✅ {result['message']}")
            print(f"📊 다운로드 크기: {result['downloaded_size']:,} bytes")
            print(f"📁 저장 경로: {result['output_path']}")
            
            if result['extracted_files']:
                print(f"📄 추출된 파일 수: {len(result['extracted_files'])}")
                if len(result['extracted_files']) <= 10:
                    print("📋 추출된 파일 목록:")
                    for file_path in result['extracted_files'][:10]:
                        print(f"  • {Path(file_path).name}")
                else:
                    print("📋 추출된 파일 (일부):")
                    for file_path in result['extracted_files'][:10]:
                        print(f"  • {Path(file_path).name}")
                    print(f"  ... 및 {len(result['extracted_files']) - 10}개 파일 더")
                    
        except AIHubAPIError as e:
            print(f"❌ 다운로드 실패: {e}")
        except Exception as e:
            print(f"❌ 예상치 못한 오류: {e}")
    
    def reset_api_key(self):
        """API 키 재설정"""
        print("\n🔑 API 키 재설정")
        new_api_key = input("새로운 API 키를 입력하세요: ").strip()
        
        if not new_api_key:
            print("❌ API 키를 입력해주세요.")
            return
        
        # 기존 클라이언트 정리
        if self.client:
            self.client.session.close()
        
        # 새로운 클라이언트로 초기화
        if self.initialize_client(new_api_key):
            print("✅ API 키가 성공적으로 변경되었습니다.")
        else:
            print("❌ API 키 변경에 실패했습니다.")
    
    def run(self):
        """메인 실행 루프"""
        print("🚀 AI-Hub 데이터셋 조회 도구를 시작합니다.")
        
        # API 키 초기화
        api_key = os.getenv('AIHUB_API_KEY')
        if not api_key:
            api_key = input("\n🔑 AI-Hub API 키를 입력하세요 (환경변수 AIHUB_API_KEY에서도 설정 가능): ").strip()
        
        if not self.initialize_client(api_key):
            print("\n❌ 클라이언트 초기화에 실패했습니다.")
            print("다음 사항을 확인해주세요:")
            print("• API 키가 올바른지 확인")
            print("• 인터넷 연결 상태 확인")
            print("• .env 파일의 AIHUB_API_KEY 설정 확인")
            return
        
        # 메인 루프
        while True:
            try:
                self.display_menu()
                choice = input("\n선택하세요 (1-6): ").strip()
                
                if choice == '1':
                    self.list_datasets()
                elif choice == '2':
                    self.get_dataset_info()
                elif choice == '3':
                    self.get_api_manual()
                elif choice == '4':
                    self.download_dataset()
                elif choice == '5':
                    self.reset_api_key()
                elif choice == '6':
                    print("\n👋 프로그램을 종료합니다. 감사합니다!")
                    break
                else:
                    print("❌ 잘못된 선택입니다. 1-6 중에서 선택해주세요.")
                
                # 계속하기 확인
                if choice in ['1', '2', '3', '4']:
                    input("\n⏸️ 계속하려면 엔터를 누르세요...")
                    
            except KeyboardInterrupt:
                print("\n\n⏹️ 사용자에 의해 프로그램이 중단되었습니다.")
                break
            except Exception as e:
                print(f"\n❌ 예상치 못한 오류가 발생했습니다: {e}")
                input("⏸️ 계속하려면 엔터를 누르세요...")
        
        # 정리
        if self.client:
            self.client.session.close()


def main():
    """메인 함수"""
    try:
        cli = AIHubCLI()
        cli.run()
    except Exception as e:
        print(f"❌ 프로그램 실행 중 오류가 발생했습니다: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 