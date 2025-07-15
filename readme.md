# AI-Hub 데이터셋 조회 도구

AI-Hub API를 통해 데이터셋을 조회하고 다운로드할 수 있는 Python 도구입니다.

## 📋 기능

- ✅ AI-Hub 데이터셋 목록 조회
- ✅ 특정 데이터셋 상세 정보 조회  
- ✅ 데이터셋 파일 목록 조회
- ✅ 데이터셋 다운로드
- ✅ 대화형 메뉴 인터페이스
- ✅ 클래스 기반 API로 프로그래밍 방식 사용 가능

## 🚀 시작하기

### 1. 사전 준비

#### AI-Hub aihubshell 설치
1. [AI-Hub 개발자 지원](https://www.aihub.or.kr/devsport/apishell/list.do?currMenu=403&topMenu=100) 페이지에서 `aihubshell` 프로그램을 다운로드합니다.
2. 다운로드한 파일을 시스템 PATH에 추가하여 어디서든 실행할 수 있도록 설정합니다.

#### API 키 발급
1. AI-Hub 웹사이트에서 회원가입 및 로그인
2. 마이페이지에서 API 키 발급
3. 발급받은 API 키를 안전한 곳에 보관

### 2. 설치

```bash
# 저장소 클론 (또는 파일 다운로드)
git clone <repository-url>
cd aihub_mcp_test

# 의존성 설치 (선택사항)
pip install -r requirements.txt
```

### 3. 환경 설정

API 키를 환경변수로 설정하는 것을 권장합니다:

**Windows:**
```cmd
set AIHUB_API_KEY=your_api_key_here
```

**Linux/Mac:**
```bash
export AIHUB_API_KEY=your_api_key_here
```

## 💻 사용법

### 대화형 모드

```bash
python aihub_dataset_query.py
```

프로그램을 실행하면 대화형 메뉴가 나타납니다:

```
=== AI-Hub 데이터셋 조회 도구 ===

AI-Hub API 키를 입력하세요 (엔터를 누르면 환경변수에서 가져옴): 

=== 메뉴 ===
1. 전체 데이터셋 목록 조회
2. 특정 데이터셋 상세 정보 조회
3. 데이터셋 파일 목록 조회
4. 데이터셋 다운로드
5. 종료

선택하세요 (1-5): 
```

### 프로그래밍 방식 사용

```python
from aihub_dataset_query import AIHubAPI

# API 인스턴스 생성
aihub = AIHubAPI(api_key="your_api_key_here")

# 또는 환경변수 사용
aihub = AIHubAPI()

# 전체 데이터셋 목록 조회
datasets = aihub.list_datasets()
print(datasets)

# 특정 데이터셋 정보 조회
dataset_info = aihub.get_dataset_info("dataset_key_here")
print(dataset_info)

# 데이터셋 파일 목록 조회
files = aihub.list_files("dataset_key_here")
print(files)

# 데이터셋 다운로드
result = aihub.download_dataset(
    dataset_key="dataset_key_here",
    file_key="file_key_here",  # 선택사항
    output_path="./downloads"   # 선택사항
)
print(result)
```

## 📚 API 참조

### AIHubAPI 클래스

#### `__init__(api_key: Optional[str] = None)`
- API 키로 인스턴스를 초기화합니다.
- `api_key`가 None이면 환경변수 `AIHUB_API_KEY`에서 가져옵니다.

#### `list_datasets(dataset_key: Optional[str] = None) -> str`
- 데이터셋 목록을 조회합니다.
- `dataset_key`가 제공되면 해당 데이터셋만 조회합니다.

#### `get_dataset_info(dataset_key: str) -> str`
- 특정 데이터셋의 상세 정보를 조회합니다.

#### `list_files(dataset_key: str, file_key: Optional[str] = None) -> str`
- 데이터셋의 파일 목록을 조회합니다.
- `file_key`가 제공되면 특정 파일 정보만 조회합니다.

#### `download_dataset(dataset_key: str, file_key: Optional[str] = None, output_path: Optional[str] = None) -> str`
- 데이터셋을 다운로드합니다.
- `file_key`: 특정 파일만 다운로드 (선택사항)
- `output_path`: 다운로드 경로 (선택사항)

## 🛠️ aihubshell 명령어 참조

이 도구는 내부적으로 다음과 같은 aihubshell 명령어를 사용합니다:

```bash
# 데이터셋 목록 조회
aihubshell --mode l --aihubapikey YOUR_API_KEY

# 특정 데이터셋 조회
aihubshell --mode l --datasetkey DATASET_KEY --aihubapikey YOUR_API_KEY

# 파일 목록 조회
aihubshell --mode l --datasetkey DATASET_KEY --filekey FILE_KEY --aihubapikey YOUR_API_KEY

# 데이터셋 다운로드
aihubshell --mode d --datasetkey DATASET_KEY --aihubapikey YOUR_API_KEY

# 특정 파일 다운로드
aihubshell --mode d --datasetkey DATASET_KEY --filekey FILE_KEY --output OUTPUT_PATH --aihubapikey YOUR_API_KEY
```

## ❗ 주의사항

1. **API 키 보안**: API 키를 코드에 직접 하드코딩하지 마세요. 환경변수를 사용하는 것을 권장합니다.

2. **aihubshell 설치**: 이 도구를 사용하기 위해서는 AI-Hub에서 제공하는 `aihubshell` 프로그램이 먼저 설치되어 있어야 합니다.

3. **네트워크 연결**: 데이터셋 조회 및 다운로드를 위해 인터넷 연결이 필요합니다.

4. **용량 주의**: 일부 데이터셋은 매우 클 수 있으므로 다운로드 전에 용량을 확인하세요.

## 🔧 문제 해결

### "aihubshell이 설치되어 있지 않습니다" 오류
- AI-Hub 개발자 지원 페이지에서 aihubshell을 다운로드하여 설치하세요.
- aihubshell이 시스템 PATH에 추가되어 있는지 확인하세요.

### API 키 관련 오류
- API 키가 정확한지 확인하세요.
- 환경변수 `AIHUB_API_KEY`가 올바르게 설정되어 있는지 확인하세요.

### 권한 오류
- 해당 데이터셋에 대한 접근 권한이 있는지 AI-Hub 웹사이트에서 확인하세요.

## 📞 지원

문제가 발생하거나 기능 요청이 있으시면 이슈를 등록해 주세요.

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 제공됩니다.
