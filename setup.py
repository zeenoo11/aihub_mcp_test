#!/usr/bin/env python3
"""
AI-Hub API 클라이언트 & MCP 서버 설치 스크립트
"""

from setuptools import setup, find_packages
import os

# README 파일 읽기
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# requirements.txt에서 의존성 읽기
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="aihub-client",
    version="1.0.0",
    author="AI-Hub Client Team",
    author_email="your-email@example.com",
    description="AI-Hub API 클라이언트 및 MCP 서버",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/aihub_mcp_test",
    packages=find_packages(),
    py_modules=[
        "aihub_client",
        "aihub_dataset_query", 
        "aihub_mcp_server",
        "example_usage"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.910",
        ],
    },
    entry_points={
        "console_scripts": [
            "aihub-cli=aihub_dataset_query:main",
            "aihub-mcp-server=aihub_mcp_server:main",
            "aihub-example=example_usage:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.bat"],
    },
    keywords="ai-hub api client mcp server dataset machine-learning",
    project_urls={
        "Bug Reports": "https://github.com/your-username/aihub_mcp_test/issues",
        "Source": "https://github.com/your-username/aihub_mcp_test",
        "Documentation": "https://github.com/your-username/aihub_mcp_test#readme",
    },
) 