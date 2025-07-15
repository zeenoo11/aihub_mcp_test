#!/usr/bin/env python3
"""
AI-Hub API Client
실제 AI-Hub API를 사용하여 데이터셋을 조회하고 다운로드하는 클라이언트
MCP(Model Context Protocol) 지원을 고려한 구조
"""

import json
import os
import tarfile
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import logging
import time

import requests
from dotenv import load_dotenv
from tqdm import tqdm


class AIHubAPIError(Exception):
    """AI-Hub API 관련 예외"""
    pass


class AIHubAuthError(AIHubAPIError):
    """AI-Hub API 인증 관련 예외"""
    pass


class AIHubClient:
    """
    AI-Hub API 클라이언트
    실제 AI-Hub REST API를 사용하여 데이터셋 조회 및 다운로드 기능 제공
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 300,
        default_download_path: Optional[str] = None
    ):
        """
        AI-Hub API 클라이언트 초기화
        
        Args:
            api_key: AI-Hub API 키 (None이면 환경변수에서 가져옴)
            base_url: API 기본 URL (기본값: https://api.aihub.or.kr)
            timeout: 요청 타임아웃 (초)
            default_download_path: 기본 다운로드 경로
        """
        # 환경변수 로드
        load_dotenv()
        
        # API 설정
        self.api_key = api_key or os.getenv('AIHUB_API_KEY')
        self.base_url = base_url or os.getenv('AIHUB_API_BASE_URL', 'https://api.aihub.or.kr')
        self.timeout = timeout or int(os.getenv('AIHUB_DOWNLOAD_TIMEOUT', '300'))
        self.default_download_path = default_download_path or os.getenv('AIHUB_DEFAULT_DOWNLOAD_PATH', './downloads')
        
        if not self.api_key:
            raise AIHubAuthError("API 키가 설정되지 않았습니다. 환경변수 AIHUB_API_KEY를 설정하거나 api_key 파라미터를 전달하세요.")
        
        # HTTP 세션 설정
        self.session = requests.Session()
        self.session.headers.update({
            'apikey': self.api_key,
            'User-Agent': 'AIHub-Python-Client/1.0'
        })
        
        # 로깅 설정
        self.logger = logging.getLogger(__name__)
        
        # API 엔드포인트
        self.endpoints = {
            'validate': f'{self.base_url}/api/keyValidate.do',
            'datasets': f'{self.base_url}/info/dataset.do',
            'manual': f'{self.base_url}/info/api.do',
            'filetree': f'{self.base_url}/info',
            'download': f'{self.base_url}/down/0.5'
        }
    
    def __enter__(self):
        """컨텍스트 매니저 진입"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 매니저 종료"""
        self.session.close()
    
    def _make_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict] = None,
        **kwargs
    ) -> requests.Response:
        """
        HTTP 요청 실행
        
        Args:
            method: HTTP 메서드 (GET, POST 등)
            url: 요청 URL
            params: URL 파라미터
            **kwargs: requests 추가 파라미터
            
        Returns:
            HTTP 응답 객체
            
        Raises:
            AIHubAPIError: API 요청 실패시
        """
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                timeout=self.timeout,
                **kwargs
            )
            
            if response.status_code == 401:
                raise AIHubAuthError("API 키가 유효하지 않습니다.")
            elif response.status_code == 403:
                raise AIHubAuthError("해당 데이터셋에 대한 접근 권한이 없습니다.")
            elif response.status_code != 200:
                raise AIHubAPIError(f"API 요청 실패: HTTP {response.status_code}")
            
            return response
            
        except requests.exceptions.Timeout:
            raise AIHubAPIError(f"요청 시간 초과 ({self.timeout}초)")
        except requests.exceptions.ConnectionError:
            raise AIHubAPIError("네트워크 연결 오류")
        except requests.exceptions.RequestException as e:
            raise AIHubAPIError(f"요청 오류: {str(e)}")
    
    def validate_api_key(self) -> bool:
        """
        API 키 유효성 검증
        
        Returns:
            API 키가 유효한지 여부
        """
        try:
            response = self._make_request('GET', self.endpoints['validate'])
            return response.status_code == 200
        except AIHubAPIError:
            return False
    
    def get_datasets(self) -> Dict[str, Any]:
        """
        전체 데이터셋 목록 조회
        
        Returns:
            데이터셋 목록 정보
        """
        response = self._make_request('GET', self.endpoints['datasets'])
        try:
            return response.json()
        except json.JSONDecodeError:
            # JSON이 아닌 경우 텍스트로 반환
            return {'raw_response': response.text}
    
    def get_dataset_info(self, dataset_key: str) -> Dict[str, Any]:
        """
        특정 데이터셋의 파일 트리 정보 조회
        
        Args:
            dataset_key: 데이터셋 키
            
        Returns:
            데이터셋 파일 트리 정보
        """
        url = f"{self.endpoints['filetree']}/{dataset_key}.do"
        response = self._make_request('GET', url)
        try:
            return response.json()
        except json.JSONDecodeError:
            return {'raw_response': response.text}
    
    def get_api_manual(self) -> Dict[str, Any]:
        """
        API 매뉴얼 정보 조회
        
        Returns:
            API 매뉴얼 정보
        """
        response = self._make_request('GET', self.endpoints['manual'])
        try:
            return response.json()
        except json.JSONDecodeError:
            return {'raw_response': response.text}
    
    def download_dataset(
        self,
        dataset_key: str,
        file_keys: Optional[Union[str, List[str]]] = None,
        output_path: Optional[str] = None,
        extract: bool = True,
        show_progress: bool = True
    ) -> Dict[str, Any]:
        """
        데이터셋 다운로드
        
        Args:
            dataset_key: 데이터셋 키
            file_keys: 다운로드할 파일 키들 (None이면 전체 다운로드)
            output_path: 다운로드 경로
            extract: tar 파일 자동 압축 해제 여부
            show_progress: 진행 상황 표시 여부
            
        Returns:
            다운로드 결과 정보
        """
        # 출력 경로 설정
        if output_path is None:
            output_path = self.default_download_path
        
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 파일 키 처리
        if file_keys is None:
            file_sn = "all"
        elif isinstance(file_keys, list):
            file_sn = ",".join(map(str, file_keys))
        else:
            file_sn = str(file_keys)
        
        # 다운로드 URL 및 파라미터 설정
        download_url = f"{self.endpoints['download']}/{dataset_key}.do"
        params = {'fileSn': file_sn}
        
        # 임시 파일로 다운로드
        with tempfile.NamedTemporaryFile(delete=False, suffix='.tar') as temp_file:
            temp_path = temp_file.name
        
        try:
            # 스트리밍 다운로드
            response = self._make_request('GET', download_url, params=params, stream=True)
            
            # 파일 크기 확인
            total_size = int(response.headers.get('content-length', 0))
            
            # 진행 상황 표시기 설정
            progress_bar = None
            if show_progress and total_size > 0:
                progress_bar = tqdm(
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    desc=f"Downloading {dataset_key}"
                )
            
            # 파일 다운로드
            downloaded_size = 0
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        if progress_bar:
                            progress_bar.update(len(chunk))
            
            if progress_bar:
                progress_bar.close()
            
            # 압축 해제
            extracted_files = []
            if extract:
                self.logger.info("압축 파일을 해제하는 중...")
                extracted_files = self._extract_and_merge(temp_path, output_dir)
            else:
                # tar 파일을 출력 디렉토리로 이동
                final_path = output_dir / f"{dataset_key}.tar"
                Path(temp_path).rename(final_path)
                extracted_files = [str(final_path)]
            
            return {
                'success': True,
                'dataset_key': dataset_key,
                'file_keys': file_sn,
                'downloaded_size': downloaded_size,
                'output_path': str(output_dir),
                'extracted_files': extracted_files,
                'message': f"데이터셋 '{dataset_key}' 다운로드 완료"
            }
            
        except Exception as e:
            # 임시 파일 정리
            if Path(temp_path).exists():
                Path(temp_path).unlink()
            raise AIHubAPIError(f"다운로드 실패: {str(e)}")
        finally:
            # 임시 파일 정리
            if Path(temp_path).exists():
                Path(temp_path).unlink()
    
    def _extract_and_merge(self, tar_path: str, output_dir: Path) -> List[str]:
        """
        tar 파일 압축 해제 및 분할 파일 병합
        
        Args:
            tar_path: tar 파일 경로
            output_dir: 출력 디렉토리
            
        Returns:
            추출된 파일 목록
        """
        extracted_files = []
        
        # tar 파일 압축 해제
        with tarfile.open(tar_path, 'r') as tar:
            tar.extractall(output_dir)
            extracted_files = [str(output_dir / member.name) for member in tar.getmembers()]
        
        # 분할 파일 병합
        self._merge_part_files(output_dir)
        
        return extracted_files
    
    def _merge_part_files(self, directory: Path):
        """
        분할된 .part 파일들을 병합
        
        Args:
            directory: 대상 디렉토리
        """
        # 모든 하위 디렉토리 탐색
        for root in directory.rglob('*'):
            if not root.is_dir():
                continue
            
            # .part 파일들 찾기
            part_files = list(root.glob('*.part*'))
            if not part_files:
                continue
            
            # 파일명별로 그룹화
            file_groups = {}
            for part_file in part_files:
                # 파일명에서 .part 이전 부분 추출
                base_name = part_file.name.split('.part')[0]
                if base_name not in file_groups:
                    file_groups[base_name] = []
                file_groups[base_name].append(part_file)
            
            # 각 그룹별로 병합
            for base_name, parts in file_groups.items():
                if len(parts) <= 1:
                    continue
                
                # 파트 번호 순으로 정렬
                parts.sort(key=lambda x: self._extract_part_number(x.name))
                
                # 병합
                output_file = root / base_name
                self.logger.info(f"Merging {base_name} in {root}")
                
                with open(output_file, 'wb') as outf:
                    for part in parts:
                        with open(part, 'rb') as inf:
                            outf.write(inf.read())
                
                # 분할 파일들 삭제
                for part in parts:
                    part.unlink()
    
    def _extract_part_number(self, filename: str) -> int:
        """
        파일명에서 파트 번호 추출
        
        Args:
            filename: 파일명
            
        Returns:
            파트 번호 (없으면 0)
        """
        try:
            if '.part' in filename:
                part_str = filename.split('.part')[1]
                return int(part_str) if part_str.isdigit() else 0
            return 0
        except (ValueError, IndexError):
            return 0


# MCP용 함수들
def create_aihub_client(api_key: Optional[str] = None) -> AIHubClient:
    """
    AIHubClient 인스턴스 생성 (MCP 호환용)
    
    Args:
        api_key: API 키
        
    Returns:
        AIHubClient 인스턴스
    """
    return AIHubClient(api_key=api_key)


def list_datasets_mcp(client: Optional[AIHubClient] = None) -> Dict[str, Any]:
    """
    데이터셋 목록 조회 (MCP 호환용)
    
    Args:
        client: AIHubClient 인스턴스
        
    Returns:
        데이터셋 목록
    """
    if client is None:
        client = create_aihub_client()
    
    return client.get_datasets()


def get_dataset_info_mcp(
    dataset_key: str,
    client: Optional[AIHubClient] = None
) -> Dict[str, Any]:
    """
    데이터셋 정보 조회 (MCP 호환용)
    
    Args:
        dataset_key: 데이터셋 키
        client: AIHubClient 인스턴스
        
    Returns:
        데이터셋 정보
    """
    if client is None:
        client = create_aihub_client()
    
    return client.get_dataset_info(dataset_key)


def download_dataset_mcp(
    dataset_key: str,
    file_keys: Optional[Union[str, List[str]]] = None,
    output_path: Optional[str] = None,
    client: Optional[AIHubClient] = None
) -> Dict[str, Any]:
    """
    데이터셋 다운로드 (MCP 호환용)
    
    Args:
        dataset_key: 데이터셋 키
        file_keys: 파일 키들
        output_path: 출력 경로
        client: AIHubClient 인스턴스
        
    Returns:
        다운로드 결과
    """
    if client is None:
        client = create_aihub_client()
    
    return client.download_dataset(
        dataset_key=dataset_key,
        file_keys=file_keys,
        output_path=output_path
    )


if __name__ == "__main__":
    # 간단한 테스트
    import sys
    
    try:
        with create_aihub_client() as client:
            print("API 키 검증 중...")
            if client.validate_api_key():
                print("✓ API 키가 유효합니다.")
                
                print("\n데이터셋 목록 조회 중...")
                datasets = client.get_datasets()
                print(f"데이터셋 조회 완료: {type(datasets)}")
                
            else:
                print("✗ API 키가 유효하지 않습니다.")
                sys.exit(1)
                
    except AIHubAPIError as e:
        print(f"오류: {e}")
        sys.exit(1) 