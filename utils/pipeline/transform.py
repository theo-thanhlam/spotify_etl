import pandas as pd
from .extract import *
from .. import logger

import sqlalchemy

def create_track_df(track_details):
    # track_details = get_track_details_from_tracks(tracks)
    
    track_df = pd.DataFrame(track_details).drop(columns=["artist_ids","album_id"]).drop_duplicates()
    track_df['release_date'] = pd.to_datetime(track_df['release_date'], format='mixed')
    return track_df

def create_album_df(album_details):
    # album_details = get_album_details_from_tracks(tracks)
    album_df = pd.DataFrame(album_details).drop(columns=['artist_ids']).drop_duplicates()
    album_df['release_date']=pd.to_datetime(album_df['release_date'], format='mixed')
    
    return album_df


def create_artist_track_df(artist_track):
    # artist_tracks = get_artist_track_from_tracks(tracks)
    artist_tracks_df = pd.DataFrame({"artist_id": list(artist_track.keys()), "track_id": artist_track.values()}).explode("track_id")
    return artist_tracks_df

def create_artist_album_df(artist_album):
    # artist_albums = get_artist_album_dict_from_tracks(tracks)
    artist_albums_df = pd.DataFrame({"artist_id": list(artist_album.keys()), "album_id": artist_album.values()}).explode("album_id")
    return artist_albums_df


"""Instead of creating from tracks, these functions create from artist details. Because if create from tracks, the artist information is not enough so the better approach is to get artist ids then find the details. 
    The process of finding details takes long time so it is not sufficient to do it everytime the function is called
    ```python
    artist_ids = get_artist_ids_from_tracks(tracks)
    artist_details = get_artist_details_from_ids(artist_ids)
    ```
    """
def create_artist_df(artist_details):
    artist_df = pd.DataFrame(artist_details).drop(columns='genres').drop_duplicates()
    return artist_df

def create_artist_genre_df(artist_genre):
    # artist_genres = get_artist_genre_from_artist_details(artist_details)
    artist_genres_df = pd.DataFrame({"artist_id":artist_genre.keys(),"genre":artist_genre.values()}).explode('genre')
    return artist_genres_df

def create_genre_df(artist_details):
    '''
    DEPRECATED
    '''
    genre_list = get_genre_list_from_artist(artist_details)
    genre_df = pd.DataFrame(genre_list).drop_duplicates()
    return genre_df
    
def create_track_album_df(track_in_album):
    track_album_df = pd.DataFrame(list(track_in_album.items()), columns=['track_id','album_id'])
    return track_album_df

def get_existing_ids(engine:sqlalchemy.engine.base.Engine, table_name:str):
    if table_name not in ["track", "artist", "album"]:
        raise ValueError(f"Table name {table_name} is not supported")
    with engine.begin() as conn:
        try:
            existing_values = pd.read_sql(con=conn, sql=f'SELECT id FROM {table_name}')
            return existing_values['id'].tolist()
        except Exception as e:
            return None

def filter_duplicate(df:pd.DataFrame, ids:List):
    return df[~df['id'].isin(ids)]
    

