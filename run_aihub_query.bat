@echo off
chcp 65001 >nul
title AI-Hub 데이터셋 조회 도구

echo ====================================
echo    AI-Hub 데이터셋 조회 도구
echo ====================================
echo.

REM Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo [오류] Python이 설치되어 있지 않습니다.
    echo Python을 설치한 후 다시 실행해주세요.
    echo 다운로드: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 현재 디렉토리로 이동
cd /d "%~dp0"

REM 메인 스크립트 파일 존재 확인
if not exist "aihub_dataset_query.py" (
    echo [오류] aihub_dataset_query.py 파일을 찾을 수 없습니다.
    echo 현재 디렉토리: %CD%
    pause
    exit /b 1
)

echo [정보] Python 설치 확인: OK
echo [정보] 스크립트 파일 확인: OK
echo.

REM 메뉴 표시
:MENU
echo ====================================
echo           메뉴 선택
echo ====================================
echo 1. 대화형 모드로 실행
echo 2. 사용 예시 스크립트 실행
echo 3. API 키 환경변수 설정
echo 4. 종료
echo ====================================
set /p choice="선택하세요 (1-4): "

if "%choice%"=="1" goto RUN_MAIN
if "%choice%"=="2" goto RUN_EXAMPLE
if "%choice%"=="3" goto SET_API_KEY
if "%choice%"=="4" goto EXIT
echo 잘못된 선택입니다. 다시 선택해주세요.
echo.
goto MENU

:RUN_MAIN
echo.
echo [실행] 대화형 모드를 시작합니다...
echo.
python aihub_dataset_query.py
echo.
echo 프로그램이 종료되었습니다.
pause
goto MENU

:RUN_EXAMPLE
echo.
if not exist "example_usage.py" (
    echo [오류] example_usage.py 파일을 찾을 수 없습니다.
    pause
    goto MENU
)
echo [실행] 사용 예시 스크립트를 시작합니다...
echo.
python example_usage.py
echo.
echo 예시 스크립트가 종료되었습니다.
pause
goto MENU

:SET_API_KEY
echo.
echo ====================================
echo      API 키 환경변수 설정
echo ====================================
echo 현재 AIHUB_API_KEY 환경변수: %AIHUB_API_KEY%
echo.
set /p api_key="새로운 API 키를 입력하세요 (취소하려면 엔터): "

if "%api_key%"=="" (
    echo 설정이 취소되었습니다.
    echo.
    goto MENU
)

setx AIHUB_API_KEY "%api_key%" >nul
if errorlevel 1 (
    echo [오류] 환경변수 설정에 실패했습니다.
) else (
    echo [성공] API 키가 환경변수로 설정되었습니다.
    echo 새 명령 프롬프트에서 적용됩니다.
)
echo.
pause
goto MENU

:EXIT
echo.
echo 프로그램을 종료합니다.
echo 감사합니다!
pause
exit /b 0 