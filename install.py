#!/usr/bin/env python3
"""
AI-Hub Client 간편 설치 스크립트
npx와 같은 방식으로 GitHub에서 직접 설치하고 실행할 수 있습니다.

사용법:
    python -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/your-username/aihub_mcp_test/main/install.py').read())"
    
또는:
    curl -sSL https://raw.githubusercontent.com/your-username/aihub_mcp_test/main/install.py | python3
"""

import subprocess
import sys
import os
import tempfile
import shutil
from pathlib import Path


def print_banner():
    """설치 배너 출력"""
    banner = """
🚀 AI-Hub Client 설치기 🚀
==========================
GitHub에서 직접 설치합니다...
"""
    print(banner)


def check_python_version():
    """Python 버전 확인"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 이상이 필요합니다.")
        print(f"현재 버전: {sys.version}")
        sys.exit(1)
    print(f"✅ Python 버전 확인: {sys.version.split()[0]}")


def install_pipx():
    """pipx 설치 확인 및 설치"""
    try:
        subprocess.run(["pipx", "--version"], check=True, capture_output=True)
        print("✅ pipx가 이미 설치되어 있습니다.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("📦 pipx를 설치하는 중...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pipx"], check=True)
            print("✅ pipx 설치 완료")
            return True
        except subprocess.CalledProcessError:
            print("⚠️ pipx 설치 실패. pip를 사용합니다.")
            return False


def install_with_pipx(repo_url):
    """pipx를 사용한 설치"""
    try:
        print("📥 pipx로 AI-Hub Client를 설치하는 중...")
        subprocess.run(
            ["pipx", "install", f"git+{repo_url}"],
            check=True
        )
        print("✅ pipx 설치 완료!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ pipx 설치 실패: {e}")
        return False


def install_with_pip(repo_url):
    """pip를 사용한 설치"""
    try:
        print("📥 pip로 AI-Hub Client를 설치하는 중...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", f"git+{repo_url}"],
            check=True
        )
        print("✅ pip 설치 완료!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ pip 설치 실패: {e}")
        return False


def create_env_file():
    """환경 설정 파일 생성"""
    env_path = Path.cwd() / ".env"
    if env_path.exists():
        print("✅ .env 파일이 이미 존재합니다.")
        return
    
    print("\n🔧 환경 설정")
    api_key = input("AI-Hub API 키를 입력하세요 (나중에 설정하려면 엔터): ").strip()
    
    env_content = f"""# AI-Hub API 설정
AIHUB_API_KEY={api_key if api_key else 'your_api_key_here'}

# 선택적 설정
AIHUB_API_BASE_URL=https://api.aihub.or.kr
AIHUB_DOWNLOAD_TIMEOUT=300
AIHUB_DEFAULT_DOWNLOAD_PATH=./downloads
"""
    
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(env_content)
    
    if api_key:
        print("✅ .env 파일이 생성되었습니다.")
    else:
        print("⚠️ .env 파일이 생성되었습니다. API 키를 설정해주세요.")


def run_client():
    """클라이언트 실행"""
    print("\n🎯 설치된 명령어들:")
    print("  • aihub-cli          - 대화형 CLI")
    print("  • aihub-mcp-server   - MCP 서버")
    print("  • aihub-example      - 사용 예시")
    
    choice = input("\n바로 실행하시겠습니까? (cli/mcp/example/n): ").strip().lower()
    
    if choice == "cli":
        try:
            subprocess.run(["aihub-cli"], check=True)
        except subprocess.CalledProcessError:
            print("❌ 실행 실패. 터미널을 다시 시작하고 'aihub-cli'를 실행해보세요.")
    elif choice == "mcp":
        try:
            subprocess.run(["aihub-mcp-server", "--test"], check=True)
        except subprocess.CalledProcessError:
            print("❌ 실행 실패. 터미널을 다시 시작하고 'aihub-mcp-server --test'를 실행해보세요.")
    elif choice == "example":
        try:
            subprocess.run(["aihub-example"], check=True)
        except subprocess.CalledProcessError:
            print("❌ 실행 실패. 터미널을 다시 시작하고 'aihub-example'을 실행해보세요.")
    else:
        print("👋 설치가 완료되었습니다!")


def main():
    """메인 설치 함수"""
    repo_url = "https://github.com/your-username/aihub_mcp_test.git"
    
    try:
        print_banner()
        check_python_version()
        
        # pipx 설치 시도
        pipx_available = install_pipx()
        
        # 패키지 설치
        success = False
        if pipx_available:
            success = install_with_pipx(repo_url)
        
        if not success:
            success = install_with_pip(repo_url)
        
        if not success:
            print("❌ 설치에 실패했습니다.")
            print("\n수동 설치 방법:")
            print(f"  git clone {repo_url}")
            print("  cd aihub_mcp_test")
            print("  pip install -r requirements.txt")
            print("  python aihub_dataset_query.py")
            sys.exit(1)
        
        # 환경 설정
        create_env_file()
        
        # 실행
        run_client()
        
    except KeyboardInterrupt:
        print("\n\n⏹️ 설치가 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 