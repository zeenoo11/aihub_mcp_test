#!/bin/bash
# AI-Hub Client 간편 설치 스크립트 (Unix/Linux/macOS)
# 
# 사용법:
#   curl -sSL https://raw.githubusercontent.com/your-username/aihub_mcp_test/main/install.sh | bash
#
# 또는:
#   wget -qO- https://raw.githubusercontent.com/your-username/aihub_mcp_test/main/install.sh | bash

set -e  # 오류 발생시 스크립트 중단

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 로고 출력
print_banner() {
    echo -e "${BLUE}"
    echo "🚀 AI-Hub Client 설치기 🚀"
    echo "=========================="
    echo "GitHub에서 직접 설치합니다..."
    echo -e "${NC}"
}

# 에러 처리
error_exit() {
    echo -e "${RED}❌ $1${NC}" >&2
    exit 1
}

# 성공 메시지
success_msg() {
    echo -e "${GREEN}✅ $1${NC}"
}

# 경고 메시지
warning_msg() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

# Python 설치 확인
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        error_exit "Python이 설치되어 있지 않습니다. Python 3.8+ 를 설치해주세요."
    fi
    
    # Python 버전 확인
    VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    if [[ $(echo "$VERSION >= 3.8" | bc -l) -eq 0 ]]; then
        error_exit "Python 3.8 이상이 필요합니다. 현재 버전: $VERSION"
    fi
    
    success_msg "Python 버전 확인: $VERSION"
}

# Git 설치 확인
check_git() {
    if ! command -v git &> /dev/null; then
        error_exit "Git이 설치되어 있지 않습니다."
    fi
    success_msg "Git 설치 확인"
}

# pipx 설치
install_pipx() {
    if command -v pipx &> /dev/null; then
        success_msg "pipx가 이미 설치되어 있습니다."
        return 0
    fi
    
    echo "📦 pipx를 설치하는 중..."
    if $PYTHON_CMD -m pip install pipx; then
        success_msg "pipx 설치 완료"
        return 0
    else
        warning_msg "pipx 설치 실패. pip를 사용합니다."
        return 1
    fi
}

# 패키지 설치
install_package() {
    local REPO_URL="https://github.com/your-username/aihub_mcp_test.git"
    
    # pipx로 설치 시도
    if command -v pipx &> /dev/null; then
        echo "📥 pipx로 AI-Hub Client를 설치하는 중..."
        if pipx install "git+$REPO_URL"; then
            success_msg "pipx 설치 완료!"
            return 0
        else
            warning_msg "pipx 설치 실패. pip로 재시도합니다."
        fi
    fi
    
    # pip로 설치
    echo "📥 pip로 AI-Hub Client를 설치하는 중..."
    if $PYTHON_CMD -m pip install "git+$REPO_URL"; then
        success_msg "pip 설치 완료!"
        return 0
    else
        error_exit "설치에 실패했습니다."
    fi
}

# 환경 파일 생성
create_env_file() {
    if [ -f ".env" ]; then
        success_msg ".env 파일이 이미 존재합니다."
        return
    fi
    
    echo -e "\n🔧 환경 설정"
    read -p "AI-Hub API 키를 입력하세요 (나중에 설정하려면 엔터): " API_KEY
    
    cat > .env << EOF
# AI-Hub API 설정
AIHUB_API_KEY=${API_KEY:-your_api_key_here}

# 선택적 설정
AIHUB_API_BASE_URL=https://api.aihub.or.kr
AIHUB_DOWNLOAD_TIMEOUT=300
AIHUB_DEFAULT_DOWNLOAD_PATH=./downloads
EOF
    
    if [ -n "$API_KEY" ]; then
        success_msg ".env 파일이 생성되었습니다."
    else
        warning_msg ".env 파일이 생성되었습니다. API 키를 설정해주세요."
    fi
}

# 클라이언트 실행
run_client() {
    echo -e "\n🎯 설치된 명령어들:"
    echo "  • aihub-cli          - 대화형 CLI"
    echo "  • aihub-mcp-server   - MCP 서버"
    echo "  • aihub-example      - 사용 예시"
    
    echo ""
    read -p "바로 실행하시겠습니까? (cli/mcp/example/n): " CHOICE
    
    case $CHOICE in
        cli)
            if command -v aihub-cli &> /dev/null; then
                aihub-cli
            else
                warning_msg "실행 실패. 터미널을 다시 시작하고 'aihub-cli'를 실행해보세요."
            fi
            ;;
        mcp)
            if command -v aihub-mcp-server &> /dev/null; then
                aihub-mcp-server --test
            else
                warning_msg "실행 실패. 터미널을 다시 시작하고 'aihub-mcp-server --test'를 실행해보세요."
            fi
            ;;
        example)
            if command -v aihub-example &> /dev/null; then
                aihub-example
            else
                warning_msg "실행 실패. 터미널을 다시 시작하고 'aihub-example'을 실행해보세요."
            fi
            ;;
        *)
            success_msg "설치가 완료되었습니다!"
            ;;
    esac
}

# 메인 함수
main() {
    print_banner
    
    # 시스템 확인
    check_python
    check_git
    
    # pipx 설치
    install_pipx
    
    # 패키지 설치
    install_package
    
    # 환경 설정
    create_env_file
    
    # 클라이언트 실행
    run_client
}

# 스크립트 실행
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi 