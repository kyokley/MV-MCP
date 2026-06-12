import os
import httpx
from fastmcp import FastMCP


API_KEY = os.environ["MV_MCP_API_KEY"].strip()
MV_HOST = os.environ["MV_HOST"].strip()
HEADERS = {'API-KEY': API_KEY}

mcp = FastMCP("MediaViewer MCP")


@mcp.tool
def tv_shows(name: str = '',
            imdb: str = '',
            tmdb: str = '',
             genre: str = '',
             ):
    resp = httpx.get(f'{MV_HOST}/mediaviewer/api/mcp-tv/',
                    params={'name': name,
                            'imdb': imdb,
                            'tmdb': tmdb,
                            'genre': genre,
                             },
                     headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

@mcp.tool
def media_files_for_tv(tv_id: str):
    """Get all episodes for a given tv show"""
    resp = httpx.get(f'{MV_HOST}/mediaviewer/api/mcp-mediafile/',
                     params={'tv_id': tv_id},
                     headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


@mcp.tool
def posters(tv_id: str = '',
            movie_id: str = '',
            mf_id: str = '',
            episode_name: str = '',
            ):
    """
    Get poster information.

    Posters contain extended information about tv shows, movies, and media files. This information includes

    Args:
        tv_id: The ID of the TV show.
        movie_id: The ID of the movie.
        mf_id: The ID of the media file.
        episode_name: The name of the episode.

    """
    resp = httpx.get(f'{MV_HOST}/mediaviewer/api/mcp-poster/',
                     params={'tv_id': tv_id,
                            'movie_id': movie_id,
                            'mf_id': mf_id,
                             'episode_name': episode_name,
                             },
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
def play_link(mf_id: str):
    """
    Get a play link for a given media file ID.

    Args:
        mf_id: The ID of the media file.
    """
    resp = httpx.get(f'{MV_HOST}/mediaviewer/api/mcp-autoplay/{mf_id}/',
                     headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


@mcp.tool
def movie_play_link(movie_id: str):
    """
    Get a play link for a given media file ID.

    Args:
        mf_id: The ID of the media file.
    """
    resp = httpx.get(f'{MV_HOST}/mediaviewer/api/mcp-movie-autoplay/{movie_id}/',
                     headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


@mcp.tool
def movies(name: str = '',
        imdb: str = '',
        tmdb: str = '',
           genre: str = '',
        ):
    resp = httpx.get(f'{MV_HOST}/mediaviewer/api/mcp-movie/',
                    params={'name': name,
                            'imdb': imdb,
                            'tmdb': tmdb,
                            'genre': genre,
                             },
                     headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    # mcp.run()
    mcp.run(transport="http", port=8089)
