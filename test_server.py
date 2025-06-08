#!/usr/bin/env python3

import asyncio
from main import mcp

async def test_server():
    """Test the MCP server functionality"""
    print("Testing MCP ShellServer...")
    
    # Test the tool registration
    tools = mcp._tools
    print(f"Registered tools: {list(tools.keys())}")
    
    # Test the terminal command tool
    if "run_terminal_command" in tools:
        print("✓ run_terminal_command tool is registered")
        
        # Test a simple command
        try:
            result = tools["run_terminal_command"]("echo 'Hello from MCP Shell Server!'")
            print(f"Test command result:\n{result}")
            print("✓ Terminal command execution works!")
        except Exception as e:
            print(f"✗ Error testing terminal command: {e}")
    else:
        print("✗ run_terminal_command tool not found")

if __name__ == "__main__":
    asyncio.run(test_server()) 