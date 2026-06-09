import os
import httpx
from fastmcp import FastMCP


API_KEY = os.environ["MV_MCP_API_KEY"].strip()
MV_HOST = os.environ["MV_HOST"].strip()
HEADERS = {'API-KEY': API_KEY}

mcp = FastMCP("MediaViewer MCP")


@mcp.tool
def main():
    return "Hello from mv-mcp!"


@mcp.tool
def tv_shows():
    resp = httpx.get(f'{MV_HOST}/mediaviewer/api/tv/',
                     headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


@mcp.tool
def tv_shows_by_imdb(imdb_id: str):
    resp = httpx.get(f'{MV_HOST}/mediaviewer/api/tv-imdb/',
                     params={'imdb_id': imdb_id},
                     headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


@mcp.tool
def tv_shows_by_genre(genre: str):
    resp = httpx.get(f'{MV_HOST}/mediaviewer/api/tv-genre/',
                     params={'genre': genre},
                     headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


@mcp.tool
def genres():
    """Get all genres from MediaViewer"""
    resp = httpx.get(f'{MV_HOST}/mediaviewer/api/genre/',
                     headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


@mcp.tool
def movies():
    resp = httpx.get(f'{MV_HOST}/mediaviewer/api/movies/',
                     headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    # mcp.run()
    mcp.run(transport="http", port=8089)
