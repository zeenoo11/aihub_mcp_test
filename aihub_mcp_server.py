#!/usr/bin/env python3
"""
AI-Hub MCP Server
Model Context Protocol 서버로 AI-Hub API 기능을 제공
"""

import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from aihub_client import AIHubClient, AIHubAPIError, AIHubAuthError

# MCP 관련 import (실제 MCP 라이브러리가 있다면 해당 라이브러리 사용)
# from mcp import Server, Tool, Resource
# 여기서는 MCP 서버 구조를 시뮬레이션합니다.


class MCPTool:
    """MCP 도구 클래스"""
    def __init__(self, name: str, description: str, parameters: Dict):
        self.name = name
        self.description = description
        self.parameters = parameters


class AIHubMCPServer:
    """AI-Hub MCP 서버"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        MCP 서버 초기화
        
        Args:
            api_key: AI-Hub API 키
        """
        self.client = AIHubClient(api_key=api_key)
        self.logger = logging.getLogger(__name__)
        
        # 도구 정의
        self.tools = self._define_tools()
    
    def _define_tools(self) -> List[MCPTool]:
        """MCP 도구들 정의"""
        return [
            MCPTool(
                name="list_datasets",
                description="AI-Hub의 전체 데이터셋 목록을 조회합니다.",
                parameters={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            MCPTool(
                name="get_dataset_info",
                description="특정 데이터셋의 상세 정보와 파일 트리를 조회합니다.",
                parameters={
                    "type": "object",
                    "properties": {
                        "dataset_key": {
                            "type": "string",
                            "description": "조회할 데이터셋의 키"
                        }
                    },
                    "required": ["dataset_key"]
                }
            ),
            MCPTool(
                name="get_api_manual",
                description="AI-Hub API 매뉴얼과 사용 가이드를 조회합니다.",
                parameters={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            MCPTool(
                name="download_dataset",
                description="데이터셋을 다운로드합니다. 전체 또는 특정 파일만 다운로드할 수 있습니다.",
                parameters={
                    "type": "object",
                    "properties": {
                        "dataset_key": {
                            "type": "string",
                            "description": "다운로드할 데이터셋의 키"
                        },
                        "file_keys": {
                            "type": ["string", "array"],
                            "description": "다운로드할 파일 키들 (생략시 전체 다운로드)",
                            "items": {"type": "string"}
                        },
                        "output_path": {
                            "type": "string",
                            "description": "다운로드 경로 (생략시 기본 경로 사용)"
                        },
                        "extract": {
                            "type": "boolean",
                            "description": "자동 압축 해제 여부 (기본값: true)",
                            "default": True
                        }
                    },
                    "required": ["dataset_key"]
                }
            ),
            MCPTool(
                name="validate_api_key",
                description="현재 설정된 API 키의 유효성을 검증합니다.",
                parameters={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            )
        ]
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """사용 가능한 도구 목록 반환"""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
            for tool in self.tools
        ]
    
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        도구 실행
        
        Args:
            tool_name: 실행할 도구 이름
            parameters: 도구 실행 파라미터
            
        Returns:
            실행 결과
        """
        try:
            if tool_name == "list_datasets":
                return self._list_datasets()
            elif tool_name == "get_dataset_info":
                return self._get_dataset_info(parameters)
            elif tool_name == "get_api_manual":
                return self._get_api_manual()
            elif tool_name == "download_dataset":
                return self._download_dataset(parameters)
            elif tool_name == "validate_api_key":
                return self._validate_api_key()
            else:
                return {
                    "success": False,
                    "error": f"Unknown tool: {tool_name}",
                    "error_type": "unknown_tool"
                }
                
        except AIHubAuthError as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": "authentication_error"
            }
        except AIHubAPIError as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": "api_error"
            }
        except Exception as e:
            self.logger.exception(f"Tool execution failed: {tool_name}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "unexpected_error"
            }
    
    def _list_datasets(self) -> Dict[str, Any]:
        """데이터셋 목록 조회"""
        datasets = self.client.get_datasets()
        return {
            "success": True,
            "data": datasets,
            "tool": "list_datasets"
        }
    
    def _get_dataset_info(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """데이터셋 정보 조회"""
        dataset_key = parameters.get("dataset_key")
        if not dataset_key:
            return {
                "success": False,
                "error": "dataset_key parameter is required",
                "error_type": "missing_parameter"
            }
        
        dataset_info = self.client.get_dataset_info(dataset_key)
        return {
            "success": True,
            "data": dataset_info,
            "dataset_key": dataset_key,
            "tool": "get_dataset_info"
        }
    
    def _get_api_manual(self) -> Dict[str, Any]:
        """API 매뉴얼 조회"""
        manual = self.client.get_api_manual()
        return {
            "success": True,
            "data": manual,
            "tool": "get_api_manual"
        }
    
    def _download_dataset(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """데이터셋 다운로드"""
        dataset_key = parameters.get("dataset_key")
        if not dataset_key:
            return {
                "success": False,
                "error": "dataset_key parameter is required",
                "error_type": "missing_parameter"
            }
        
        file_keys = parameters.get("file_keys")
        output_path = parameters.get("output_path")
        extract = parameters.get("extract", True)
        
        result = self.client.download_dataset(
            dataset_key=dataset_key,
            file_keys=file_keys,
            output_path=output_path,
            extract=extract,
            show_progress=False  # MCP에서는 진행률 표시 비활성화
        )
        
        return {
            "success": True,
            "data": result,
            "tool": "download_dataset"
        }
    
    def _validate_api_key(self) -> Dict[str, Any]:
        """API 키 유효성 검증"""
        is_valid = self.client.validate_api_key()
        return {
            "success": True,
            "data": {
                "is_valid": is_valid,
                "api_key_masked": f"{self.client.api_key[:8]}..." if self.client.api_key else None
            },
            "tool": "validate_api_key"
        }


class MCPServerProtocol:
    """MCP 서버 프로토콜 시뮬레이션"""
    
    def __init__(self, aihub_server: AIHubMCPServer):
        self.aihub_server = aihub_server
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        MCP 요청 처리
        
        Args:
            request: MCP 요청
            
        Returns:
            MCP 응답
        """
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "tools/list":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": self.aihub_server.get_available_tools()
                    }
                }
            
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                result = self.aihub_server.execute_tool(tool_name, arguments)
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2, ensure_ascii=False)
                            }
                        ]
                    }
                }
            
            elif method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "aihub-mcp-server",
                            "version": "1.0.0"
                        }
                    }
                }
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
                
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }


def create_mcp_server(api_key: Optional[str] = None) -> MCPServerProtocol:
    """
    MCP 서버 생성
    
    Args:
        api_key: AI-Hub API 키
        
    Returns:
        MCP 서버 프로토콜
    """
    aihub_server = AIHubMCPServer(api_key=api_key)
    return MCPServerProtocol(aihub_server)


def main():
    """MCP 서버 실행"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI-Hub MCP Server")
    parser.add_argument("--api-key", help="AI-Hub API key")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()
    
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        # MCP 서버 생성
        mcp_server = create_mcp_server(api_key=args.api_key)
        
        if args.test:
            # 테스트 모드
            print("🧪 AI-Hub MCP Server - Test Mode")
            
            # 도구 목록 테스트
            test_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": {}
            }
            
            response = mcp_server.handle_request(test_request)
            print("\n📋 Available Tools:")
            for tool in response["result"]["tools"]:
                print(f"  • {tool['name']}: {tool['description']}")
            
            # API 키 검증 테스트
            validate_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "validate_api_key",
                    "arguments": {}
                }
            }
            
            response = mcp_server.handle_request(validate_request)
            print(f"\n🔑 API Key Validation:")
            print(response["result"]["content"][0]["text"])
            
        else:
            # 실제 MCP 서버 모드 (stdin/stdout을 통한 JSON-RPC)
            print("🚀 AI-Hub MCP Server starting...", file=sys.stderr)
            
            for line in sys.stdin:
                try:
                    request = json.loads(line.strip())
                    response = mcp_server.handle_request(request)
                    print(json.dumps(response, ensure_ascii=False))
                    sys.stdout.flush()
                except json.JSONDecodeError:
                    continue
                except KeyboardInterrupt:
                    break
                    
    except Exception as e:
        print(f"❌ MCP Server error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 