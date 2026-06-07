from fastmcp import FastMCP


mcp = FastMCP("MediaViewer MCP")


def main():
    print("Hello from mv-mcp!")


if __name__ == "__main__":
    mcp.run(transport="http", port=8089)
