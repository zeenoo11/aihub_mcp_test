# AI-Hub API 클라이언트 & MCP 서버

실제 AI-Hub REST API를 사용하여 데이터셋을 조회하고 다운로드할 수 있는 Python 클라이언트와 MCP(Model Context Protocol) 서버입니다.

## 🎯 주요 특징

- ✅ **실제 AI-Hub REST API 연동** - aihubshell 대신 직접 HTTP API 호출
- ✅ **MCP 서버 지원** - 다른 AI 시스템에서 도구로 사용 가능
- ✅ **환경변수 지원** - .env 파일을 통한 설정 관리
- ✅ **타입 힌트 완전 지원** - 개발자 친화적인 코드
- ✅ **진행률 표시** - 다운로드 진행 상황 실시간 확인
- ✅ **자동 압축 해제** - tar 파일 및 분할 파일 자동 처리
- ✅ **대화형 CLI** - 사용자 친화적인 명령줄 인터페이스

## 📋 기능

### Core Features
- 🔍 **데이터셋 목록 조회** - 전체 데이터셋 목록 및 검색
- 📄 **상세 정보 조회** - 특정 데이터셋의 파일 트리 및 메타데이터
- 📚 **API 매뉴얼** - AI-Hub API 사용 가이드 조회
- ⬇️ **스마트 다운로드** - 전체/부분 다운로드, 자동 압축 해제
- 🔐 **API 키 관리** - 유효성 검증 및 안전한 저장

### Interfaces
- 🖥️ **대화형 CLI** - 직관적인 메뉴 기반 인터페이스
- 🐍 **Python API** - 프로그래밍 방식 사용
- 🔌 **MCP 서버** - AI 시스템 통합용 서버
- 🖱️ **Windows GUI** - 배치 스크립트를 통한 쉬운 실행

## 🚀 시작하기

### ⚡ 간편 설치 (npx 스타일)

**한 줄로 설치하고 바로 실행:**

```bash
# Python으로 (Windows/Mac/Linux 모두 지원)
python -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/your-username/aihub_mcp_test/main/install.py').read())"

# 또는 Unix/Linux/macOS에서
curl -sSL https://raw.githubusercontent.com/your-username/aihub_mcp_test/main/install.sh | bash
```

**pipx로 설치 (권장):**
```bash
# pipx 한 번만 설치
pip install pipx

# GitHub에서 직접 설치
pipx install git+https://github.com/your-username/aihub_mcp_test.git

# 실행
aihub-cli
```

**pip로 설치:**
```bash
pip install git+https://github.com/your-username/aihub_mcp_test.git
aihub-cli
```

### 📋 수동 설치

```bash
# 저장소 클론
git clone https://github.com/your-username/aihub_mcp_test.git
cd aihub_mcp_test

# 의존성 설치
pip install -r requirements.txt

# 또는 패키지로 설치
pip install -e .
```

### 🔑 API 키 발급
1. [AI-Hub](https://www.aihub.or.kr)에서 회원가입 및 로그인
2. 개발자 지원 페이지에서 API 키 발급
3. 발급받은 API 키를 안전한 곳에 보관

### 3. 환경 설정

`.env` 파일을 생성하여 API 키를 설정하세요:

```bash
# .env 파일 생성 (env_example.txt 참조)
cp env_example.txt .env

# .env 파일 편집
# AIHUB_API_KEY=your_api_key_here
```

또는 환경변수로 직접 설정:

**Windows:**
```cmd
set AIHUB_API_KEY=your_api_key_here
```

**Linux/Mac:**
```bash
export AIHUB_API_KEY=your_api_key_here
```

## 💻 사용법

### 🖥️ 대화형 CLI

```bash
python aihub_dataset_query.py
```

새로운 대화형 인터페이스:

```
🚀 AI-Hub 데이터셋 조회 도구를 시작합니다.
✅ API 키 검증 완료

==================================================
         AI-Hub 데이터셋 조회 도구
==================================================
1. 전체 데이터셋 목록 조회
2. 특정 데이터셋 상세 정보 조회
3. API 매뉴얼 조회
4. 데이터셋 다운로드
5. API 키 재설정
6. 종료
==================================================

선택하세요 (1-6): 
```

### 🐍 Python API 사용

```python
from aihub_client import AIHubClient

# 클라이언트 생성 (컨텍스트 매니저 사용 권장)
with AIHubClient(api_key="your_api_key") as client:
    # 또는 환경변수/.env 파일 사용
    # with AIHubClient() as client:
    
    # API 키 검증
    if client.validate_api_key():
        print("✅ API 키 유효")
    
    # 데이터셋 목록 조회
    datasets = client.get_datasets()
    print(datasets)
    
    # 특정 데이터셋 정보 조회
    dataset_info = client.get_dataset_info("dataset_key")
    print(dataset_info)
    
    # 데이터셋 다운로드
    result = client.download_dataset(
        dataset_key="dataset_key",
        file_keys=["file1", "file2"],  # 선택사항
        output_path="./downloads",     # 선택사항
        extract=True,                  # 자동 압축 해제
        show_progress=True             # 진행률 표시
    )
    print(f"다운로드 완료: {result['message']}")

# MCP 호환 함수들
from aihub_client import list_datasets_mcp, get_dataset_info_mcp, download_dataset_mcp

# MCP 호환 사용법
datasets = list_datasets_mcp()
dataset_info = get_dataset_info_mcp("dataset_key")
result = download_dataset_mcp("dataset_key", output_path="./data")
```

### 🔌 MCP 서버 사용

#### 테스트 모드
```bash
python aihub_mcp_server.py --test
```

#### 실제 MCP 서버 실행
```bash
python aihub_mcp_server.py
```

#### MCP 서버 JSON-RPC 예시
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "list_datasets",
    "arguments": {}
  }
}
```

## 📚 API 참조

### AIHubClient 클래스

#### `__init__(api_key, base_url, timeout, default_download_path)`
```python
client = AIHubClient(
    api_key="your_api_key",          # API 키 (환경변수에서 자동 로드)
    base_url="https://api.aihub.or.kr",  # API 기본 URL
    timeout=300,                     # 요청 타임아웃 (초)
    default_download_path="./downloads"  # 기본 다운로드 경로
)
```

#### 주요 메서드

| 메서드 | 설명 | 반환값 |
|--------|------|--------|
| `validate_api_key()` | API 키 유효성 검증 | `bool` |
| `get_datasets()` | 전체 데이터셋 목록 조회 | `Dict[str, Any]` |
| `get_dataset_info(dataset_key)` | 특정 데이터셋 정보 조회 | `Dict[str, Any]` |
| `get_api_manual()` | API 매뉴얼 조회 | `Dict[str, Any]` |
| `download_dataset(...)` | 데이터셋 다운로드 | `Dict[str, Any]` |

#### 다운로드 메서드 상세

```python
result = client.download_dataset(
    dataset_key="593",               # 필수: 데이터셋 키
    file_keys=["file1", "file2"],    # 선택: 특정 파일들만
    output_path="./my_data",         # 선택: 출력 경로
    extract=True,                    # 선택: 자동 압축 해제
    show_progress=True               # 선택: 진행률 표시
)

# 반환값 예시
{
    "success": True,
    "dataset_key": "593",
    "downloaded_size": 1073741824,
    "output_path": "./my_data",
    "extracted_files": ["file1.txt", "file2.json"],
    "message": "데이터셋 '593' 다운로드 완료"
}
```

### MCP 도구 목록

| 도구명 | 설명 | 파라미터 |
|--------|------|----------|
| `list_datasets` | 데이터셋 목록 조회 | 없음 |
| `get_dataset_info` | 데이터셋 정보 조회 | `dataset_key` |
| `get_api_manual` | API 매뉴얼 조회 | 없음 |
| `download_dataset` | 데이터셋 다운로드 | `dataset_key`, `file_keys?`, `output_path?`, `extract?` |
| `validate_api_key` | API 키 검증 | 없음 |

## 🛠️ AI-Hub REST API 엔드포인트

이 클라이언트는 다음 AI-Hub REST API를 사용합니다:

```http
# 기본 URL
https://api.aihub.or.kr

# 엔드포인트
GET /api/keyValidate.do          # API 키 검증
GET /info/dataset.do             # 데이터셋 목록
GET /info/{dataset_key}.do       # 데이터셋 정보
GET /info/api.do                 # API 매뉴얼
GET /down/0.5/{dataset_key}.do   # 데이터셋 다운로드

# 헤더
apikey: YOUR_API_KEY
```

## ❗ 주의사항

1. **🔐 API 키 보안**: 
   - API 키를 코드에 직접 하드코딩하지 마세요
   - `.env` 파일을 사용하고 `.gitignore`에 추가하세요
   - 환경변수 사용을 권장합니다

2. **📊 데이터셋 용량**: 
   - 일부 데이터셋은 수십 GB에 이를 수 있습니다
   - 다운로드 전에 용량과 무료 공간을 확인하세요
   - 분할 다운로드(`file_keys` 파라미터) 활용을 고려하세요

3. **🌐 네트워크 연결**: 
   - 안정적인 인터넷 연결이 필요합니다
   - 대용량 파일 다운로드 시 연결 중단에 주의하세요

4. **📝 데이터셋 승인**: 
   - 다운로드 전에 AI-Hub 웹사이트에서 데이터셋 사용 승인을 받아야 합니다
   - 승인되지 않은 데이터셋은 다운로드할 수 없습니다

## 🔧 문제 해결

### 🔑 API 키 관련 오류
```
❌ API 키가 유효하지 않습니다.
```
**해결 방법:**
1. AI-Hub 웹사이트에서 API 키를 다시 확인
2. `.env` 파일의 `AIHUB_API_KEY` 설정 확인
3. 환경변수가 올바르게 로드되는지 확인
4. API 키에 특수문자가 있다면 따옴표로 감싸기

### 🚫 권한 관련 오류
```
❌ 해당 데이터셋에 대한 접근 권한이 없습니다.
```
**해결 방법:**
1. AI-Hub 웹사이트에서 해당 데이터셋 승인 신청
2. 승인 완료까지 대기 (수분~수시간 소요)
3. 데이터셋 키가 올바른지 확인

### 📦 패키지 설치 오류
```
❌ ModuleNotFoundError: No module named 'requests'
```
**해결 방법:**
```bash
pip install -r requirements.txt
```

### 💾 다운로드 실패
```
❌ 다운로드 실패: 네트워크 연결 오류
```
**해결 방법:**
1. 인터넷 연결 상태 확인
2. 방화벽/프록시 설정 확인
3. 다운로드 경로의 쓰기 권한 확인
4. 디스크 공간 부족 여부 확인

### 🏗️ MCP 서버 오류
```
❌ MCP Server error: [Errno 2] No such file or directory
```
**해결 방법:**
1. `aihub_client.py` 파일이 같은 디렉토리에 있는지 확인
2. Python 경로 설정 확인
3. 의존성 패키지 설치 확인

## 📁 파일 구조

```
aihub_mcp_test/
├── aihub_client.py          # 🎯 메인 AI-Hub API 클라이언트
├── aihub_dataset_query.py   # 🖥️ 대화형 CLI 인터페이스
├── aihub_mcp_server.py      # 🔌 MCP 서버
├── example_usage.py         # 📝 사용 예시 스크립트
├── run_aihub_query.bat      # 🖱️ Windows 실행 스크립트
├── requirements.txt         # 📦 Python 의존성
├── env_example.txt          # 🔧 환경변수 예시
├── README.md               # 📚 이 문서
└── aihubshell              # 📋 원본 shell 스크립트 (참조용)
```

## 🔄 버전 히스토리

### v1.0.0 (현재)
- ✅ 실제 AI-Hub REST API 연동
- ✅ MCP 서버 지원
- ✅ 타입 힌트 및 에러 처리 개선
- ✅ 진행률 표시 및 자동 압축 해제
- ✅ 환경변수 및 .env 파일 지원

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 지원

- 🐛 **버그 리포트**: GitHub Issues에 등록
- 💡 **기능 요청**: GitHub Issues에 등록
- 📧 **문의사항**: 이메일 또는 GitHub Discussions

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 제공됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 🙏 감사의 말

- AI-Hub 팀의 API 제공에 감사드립니다
- 오픈소스 커뮤니티의 지속적인 지원에 감사드립니다

---

**⚡ 빠른 시작**
```bash
# npx 스타일 - 한 줄로 설치하고 실행
python -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/your-username/aihub_mcp_test/main/install.py').read())"

# 또는 pipx로
pipx install git+https://github.com/your-username/aihub_mcp_test.git && aihub-cli

# 또는 수동으로
git clone https://github.com/your-username/aihub_mcp_test.git
cd aihub_mcp_test
pip install -e .
echo "AIHUB_API_KEY=your_api_key_here" > .env
aihub-cli
```
