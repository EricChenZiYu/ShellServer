# MCP Shell Server

A simple Model Context Protocol (MCP) server that provides terminal command execution capabilities.

## Features

- **Terminal Command Tool**: Execute shell commands and get their output
- **Safe Execution**: Commands have a 30-second timeout to prevent hanging
- **Complete Output**: Returns both stdout and stderr along with return codes
- **Error Handling**: Graceful error handling for failed commands

## Installation

1. Make sure you have Python 3.10+ installed
2. Install dependencies:
   ```bash
   uv add "mcp[cli]"
   ```

## Usage

### Running the Server

To start the MCP server:

```bash
uv run python main.py
```

### Connecting to Claude Desktop

To use this server with Claude Desktop, you need to add it to Claude's configuration file:

#### For macOS:
Edit `~/Library/Application Support/Claude/claude_desktop_config.json`

#### For Windows:
Edit `%APPDATA%/Claude/claude_desktop_config.json`

Add the following configuration:

```json
{
  "mcpServers": {
    "shell-server": {
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "/path/to/your/ShellServer",
      "env": {}
    }
  }
}
```

**Important**: Replace `/path/to/your/ShellServer` with the actual path to your server directory.

#### Alternative Configurations

The repository includes several configuration templates:

1. **`claude-desktop-config.json`** - Generic template for Claude Desktop
2. **`server-configs.json`** - Multiple configuration options:
   - `shell-server-uv`: Uses uv to run the server (recommended)
   - `shell-server-python`: Uses system Python directly
   - `shell-server-venv`: Uses virtual environment Python directly

Choose the configuration that matches your setup and copy it to Claude Desktop's config file.

### Testing with MCP Inspector

You can test the server using the MCP Inspector:

```bash
uv run mcp dev main.py
```

### Available Tools

#### `run_terminal_command`

Execute a terminal command and return its output.

**Parameters:**
- `command` (string): The terminal command to execute

**Returns:**
- String containing the command output, including stdout, stderr, and return code

**Example:**
```python
# This would be called by an MCP client
result = run_terminal_command("ls -la")
```

## Security Considerations

⚠️ **Warning**: This server executes arbitrary shell commands. Only use it in trusted environments and with trusted clients. Consider implementing additional security measures for production use:

- Command whitelisting
- User permission checks
- Sandboxing
- Input validation

## Configuration

The server includes the following safety features:
- 30-second timeout for command execution
- Capture of both stdout and stderr
- Proper error handling for failed commands

## Example Output

When executing a command like `echo "Hello World"`, you'll get output like:

```
STDOUT:
Hello World

Return code: 0
```

## Development

To test the server functionality:

```bash
uv run python test_server.py
```

## Configuration Files

The repository includes several MCP configuration files:

- `mcp-server-config.json` - Specific configuration for this installation
- `claude-desktop-config.json` - Generic Claude Desktop template
- `server-configs.json` - Multiple configuration options

## Troubleshooting

### Claude Desktop Not Finding Server
1. Ensure the `cwd` path in the config is correct
2. Verify Python 3.10+ is available
3. Check that dependencies are installed: `uv add "mcp[cli]"`
4. Restart Claude Desktop after updating the config

### Permission Errors
Make sure the server has appropriate permissions to execute commands in your environment.

## License

This project is open source and available under the MIT License.


docker build -t shellserver-app .
docker run -it --rm shellserver-app
