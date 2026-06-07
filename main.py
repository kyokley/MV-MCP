from fastmcp import FastMCP


mcp = FastMCP("MediaViewer MCP")


@mcp.tool
def main():
    return "Hello from mv-mcp!"


if __name__ == "__main__":
    mcp.run()
    # mcp.run(transport="http", port=8089)
