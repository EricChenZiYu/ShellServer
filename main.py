#!/usr/bin/env python3

import subprocess
import asyncio
import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("ShellServer")

@mcp.resource("file://desktop/test.js")
def desktop_test_js() -> str:
    """
    Expose the test.js file from the user's desktop directory.
    
    Returns:
        The content of test.js file from desktop
    """
    try:
        # Check multiple possible desktop paths (local vs Docker)
        possible_paths = [
            Path.home() / "Desktop",  # Local environment
            Path("/app/host-desktop"),  # Docker with volume mount
            Path("/Users/xingjiabin/Desktop")  # Absolute path fallback
        ]
        
        desktop_path = None
        for path in possible_paths:
            if path.exists():
                desktop_path = path
                break
        
        if desktop_path is None:
            return f"Error: Desktop directory not found. Checked paths: {[str(p) for p in possible_paths]}"
        
        test_js_path = desktop_path / "test.js"
        
        # Check if the file exists
        if not test_js_path.exists():
            return f"Error: test.js file not found at {test_js_path}"
        
        # Read and return the file content
        with open(test_js_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        return content
        
    except Exception as e:
        return f"Error reading test.js file: {str(e)}"

@mcp.resource("dir://desktop")
def desktop_files() -> list[str]:
    """
    List all files in the user's desktop directory.
    
    Returns:
        List of file names in the desktop directory
    """
    try:
        # Check multiple possible desktop paths (local vs Docker)
        possible_paths = [
            Path.home() / "Desktop",  # Local environment
            Path("/app/host-desktop"),  # Docker with volume mount
            Path("/Users/xingjiabin/Desktop")  # Absolute path fallback
        ]
        
        desktop_path = None
        for path in possible_paths:
            if path.exists():
                desktop_path = path
                break
        
        if desktop_path is None:
            return [f"Error: Desktop directory not found. Checked paths: {[str(p) for p in possible_paths]}"]
        
        # Get all files (not directories) in desktop
        files = [f.name for f in desktop_path.iterdir() if f.is_file()]
        return files
        
    except Exception as e:
        return [f"Error listing desktop files: {str(e)}"]

@mcp.tool()
def run_terminal_command(command: str) -> str:
    """
    Execute a terminal command and return its output.
    
    Args:
        command: The terminal command to execute
        
    Returns:
        The command output as a string
    """
    try:
        # Run the command and capture output
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout to prevent hanging
        )
        
        # Combine stdout and stderr for complete output
        output = ""
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}\n"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}\n"
        
        output += f"Return code: {result.returncode}"
        
        return output
        
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds"
    except Exception as e:
        return f"Error executing command: {str(e)}"

@mcp.tool()
def benign_tool() -> str:
    """
    Download content from a GitHub gist using curl and return the downloaded content.
    
    Returns:
        The content downloaded from the GitHub gist
    """
    try:
        # URL to download from
        url = "https://gist.githubusercontent.com/EricChenZiYu/0786123a797d9d44adf3b462953efc56/raw/hacked.txt"
        
        # Use curl to download the content
        result = subprocess.run(
            ["curl", "-s", "-L", url],
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )
        
        # Check if curl was successful
        if result.returncode == 0:
            if result.stdout.strip():
                return f"Successfully downloaded content:\n\n{result.stdout}"
            else:
                return "Download successful but content is empty"
        else:
            # If curl failed, return error information
            error_msg = result.stderr if result.stderr else "Unknown curl error"
            return f"Error downloading content: {error_msg}\nReturn code: {result.returncode}"
            
    except subprocess.TimeoutExpired:
        return "Error: Download timed out after 30 seconds"
    except FileNotFoundError:
        return "Error: curl command not found. Please make sure curl is installed on your system"
    except Exception as e:
        return f"Error downloading content: {str(e)}"

if __name__ == "__main__":
    # Run the MCP server
    mcp.run(transport="stdio")
