from typing import List, Dict
import requests
from .. import spotify, logger
import sqlalchemy

SPOTIFY_API_URL_PREFIX = "https://api.spotify.com/v1"


def get_tracks_by_genre(genre:str, token:Dict[str,any],offset:int=0,limit:int=20):
    """
    Fetch tracks by genre from Spotify
    
    Params:
        genre (str): The genre to search for
        token (Dict[str,any]): Spotify authentication token
        offset (int, optiional): Pagination offset, Default to 0
        limit (int, optional): Number of tracks to fetch per request. Defaults to 20
    
    Returns:
        tracks (Dict[str,any]): A response detail from Spotify API
    
    """
    if offset+limit >= 1000:
        logger.error("Exceed maximum offset")
        raise ValueError("Exceed maximum offset")
    ENDPOINT = f"{SPOTIFY_API_URL_PREFIX}/search?q=genre:{genre}&type=track&offset={offset}&limit={limit}"
    headers = spotify.get_auth_header(token=token)
    response = requests.get(url=ENDPOINT, headers=headers)
    tracks = response.json()['tracks']
    logger.info(f"Get {genre} tracks from Spotify API")
    return tracks

def get_track_details_from_tracks(tracks:Dict[str,any]):
    """
    Retrieves a list of track details 
    
    Params:
        tracks (Dict[str,any]): tracks from get_tracks_by_genre
    
    Returns:
        track_details (List[Dict[str,any]]): A list of dictionaries of new tracks details, containing:
            - id (str): Spotify ID for the track
            - name (str): Name of this track
            - url (str): Spotify URL for the object
            - duration_ms (int): The track length in milliseconds
            - artist_ids (List[str]): List of Spotify ID for the artists
            - album_id (str): Spotify ID for the album
            - release_date (str): The date the album was first released
            - is_single (Boolean):Check if this is a single or part of the album
            - explicit (Boolean): Whether or not the track has explicit lyrics
    """
    track_details = []
    for item in tracks['items']:
        track_artist_ids =[artist['id'] for artist in item['artists']]
        track_detail = {
            "id":item["id"],
            "name":item['name'],
            "url":item['external_urls']['spotify'],
            "duration_ms":item['duration_ms'],
            'artist_ids':track_artist_ids,
            "album_id":item['album']['id'],
            'release_date':item['album']['release_date'],
            "is_single":True if item['album']['album_type']=='single' else False,
            'explicit': item['explicit']
        }
        track_details.append(track_detail)
        
    return track_details
    
def get_album_details_from_tracks(tracks:Dict[str,any]):
    """
    Retrieves a list of album details from tracks
    
    Params:
        tracks (Dict[str,any]): tracks from get_tracks_by_genre
    
    Returns:
        album_details (List[Dict[str,any]]): A list of dictionaries of new album details, containing:
            - id (str): Spotify ID for the album
            - album_name (str): The name of the album. In case of an album takedown, the value may be an empty string
            - release_date (str): The date the album was first released
            - artist_ids (List[str]): List of Spotify ID for the artists
            - total_tracks (int): number of tracks in the album
            - image_640_url (str): URL for the album cover size 640x640
            _ image_300_url (str): URL for the album cover size 300x300
            _ image_64_url (str): URL for the album cover size 64x64
    """
    album_details = []
    for item in tracks['items']:
        album = item['album']
        album_artist_ids = [artist['id'] for artist in album['artists']]
        album_detail= {
            "id":album['id'],
            "name":album['name'],
            "release_date":album['release_date'],
            'artist_ids':album_artist_ids,
            'album_url':album['external_urls']['spotify'],
            'total_tracks':album['total_tracks'],
            "type":album['type'],
            "image_640_url":album['images'][0]["url"] if album['images'] else "",
            "image_300_url":album['images'][1]["url"] if album['images'] else "",
            'image_64_url':album['images'][2]['url'] if album['images'] else ""
        }
        album_details.append(album_detail)
        
    return album_details

def get_artist_track_from_tracks(tracks:Dict[str,any]):
    """
    Retrieves artist who procduces the track
    
    Params:
        tracks (Dict[str,any]): tracks from get_tracks_by_genre
    
    Returns:
        artist_track_dict (Dict[str,List[str]]): A dictionary containing artist_id own a list of track
    """
    artist_track_dict:Dict[str,List[str]] = {}
    for item in tracks['items']:
        track_id = item['id']
        for artist in item['artists']:
            artist_id = artist['id']
            if artist_track_dict.get(artist_id) is None:
                artist_track_dict[artist_id] = []
            artist_track_dict[artist_id].append(track_id)
    return artist_track_dict
        
def get_artist_album_dict_from_tracks(tracks:Dict[str,any]):
    """
    Retrieves artist who procduces the album
    
    Params:
        tracks (Dict[str,any]): tracks from get_tracks_by_genre
    
    Returns:
        artist_album_dict (Dict[str,List[str]]): A dictionary containing artist_id own a list of album
    """
    
    artist_album_dict:Dict[str,List[str]] = {}
    for item in tracks['items']:
        album = item['album']
        album_id = album['id']
        for artist in item['artists']:
            artist_id = artist['id']
            if artist_album_dict.get(artist_id) is None:
                artist_album_dict[artist_id] = []
            artist_album_dict[artist_id].append(album_id)
    return artist_album_dict
        
def get_artist_detail(artist_id:str, token:Dict[str,any]):
    '''
    Retrieve artist information from Spotify
    
    Params:
        artist_id (str): Spotify Id of the artist
    
    Returns:
        artist_detail (Dict[str,str]): A dictionary of artist detail, containing:
            - artist_id (str): Spotify ID for the artist
            - name (str): The name of the artist
            - url (str): Spotify URL for the object
            - genres (List[str]): A list of the genres thr artist is associated with. If not yet classified, the array is empty
            - image_640_url (str): URL for the artist cover size 640x640
            - image_320_url (str): URL for the artist cover size 320x320
            - image_160_url (str): URL for the artist cover size 160x160
        
    '''
    ENDPOINT = f"{SPOTIFY_API_URL_PREFIX}/artists/{artist_id}"
    headers = spotify.get_auth_header(token=token)
    response = requests.get(url=ENDPOINT, headers=headers)
    if response.status_code == 429:
        logger.error("Exceed rate limit")
        raise "Exceed rate limit"
    artist_doc = response.json()
    artist_detail = {
        "id": artist_doc['id'],
        "name": artist_doc['name'],
        "url":artist_doc['external_urls']['spotify'],
        'genres':artist_doc['genres'],
        'image_640_url':artist_doc['images'][0]['url'] if artist_doc['images'] else "",
        'image_320_url':artist_doc['images'][1]['url'] if artist_doc['images'] else "",
        'image_160_url':artist_doc['images'][2]['url'] if artist_doc['images'] else ""
    }
    return artist_detail
    
def get_genre_list_from_artist(artist_details:List[Dict[str,any]]):
    '''
    Retrieve list of genres of artists
    
    Params:
        artist_details (List[Dict[str,any]]): details of artist 
    
    Returns:
        genre_list (List): list of unique genres
    '''
    genre_list = []
    for artist_detail in artist_details:
        genre_list.extend(artist_detail['genres'])
    return list(set(genre_list))

def get_artist_ids_from_tracks(tracks):
    artists_from_album = []
    artists_from_artists = []
    for item in tracks['items']:
        for artist in item['album']['artists']:
           artists_from_album.append(artist['id'])
        for artist in item['artists']:
            artists_from_artists.append(artist['id'])
    artist_ids = list(set(artists_from_album + artists_from_artists))
    return artist_ids
def get_artist_details_from_ids(artist_ids:List[str], token=None):
    if token is None:
        token = spotify.get_token()
    artist_details = [get_artist_detail(artist_id, token=token) for artist_id in artist_ids]
    return artist_details
def get_artist_genre_from_artist_details(artist_details):
    artist_genres_dict = {artist_detail['id']:artist_detail['genres'] for artist_detail in artist_details}
    return artist_genres_dict

def get_track_album_from_tracks(tracks):
    track_album = {}
    for item in tracks['items']:
        track_id = item['id']
        album_id = item['album']['id']
        if track_album.get(track_id) is None:
            track_album[track_id] = album_id
    return track_album


def count_records(engine:sqlalchemy.engine.base.Engine, table_name:str):
    if table_name not in ['track','artist','album']:
        raise ValueError(f"Table name {table_name} is not supported")
    with engine.begin() as conn:
        try:
            stmt = sqlalchemy.text(f"SELECT count(*) from {table_name}")
            total_track = conn.execute(stmt)
            return total_track.scalar()
        except Exception as e:
            logger.error(f"Error in get_existing_ids_list: {e}")