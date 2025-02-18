from utils import *
from utils.pipeline import *
from time import time


def main():
     #Spotify handler
    token = spotify.get_token()
    #Database Session
    engine = database.get_engine()
    
    #task starts
    extract_start_time = time()
    offset = int(Extract.count_records(engine=engine,table_name="track"))
    dupstep_tracks = Extract.get_tracks_by_genre(genre="dubstep", offset=offset, limit=20, token=token)
    
    #Extrack Tasks
    extract_start_time = time()

    artist_ids = Extract.get_artist_ids_from_tracks(dupstep_tracks)
    artists = Extract.get_artist_details_from_ids(artist_ids, token=token)
    
    aritst_genre = Extract.get_artist_genre_from_artist_details(artist_details=artists) 
    artist_track = Extract.get_artist_track_from_tracks(tracks=dupstep_tracks)
    artist_album = Extract.get_artist_album_dict_from_tracks(tracks=dupstep_tracks)
    
    albums = Extract.get_album_details_from_tracks(tracks=dupstep_tracks)
    tracks = Extract.get_track_details_from_tracks(tracks=dupstep_tracks)
    
    track_album = Extract.get_track_album_from_tracks(tracks=dupstep_tracks)
    extract_end_time = time()
    #Tranform Tasks
    transform_start_time = time()
    artist_df = Transform.create_artist_df(artist_details=artists)
    artist_genre_df = Transform.create_artist_genre_df(artist_genre=aritst_genre)
    artist_track_df = Transform.create_artist_track_df(artist_track=artist_track)
    artist_album_df = Transform.create_artist_album_df(artist_album=artist_album)
    album_df = Transform.create_album_df(album_details=albums)
    track_df = Transform.create_track_df(track_details=tracks)
    track_album_df = Transform.create_track_album_df(track_in_album=track_album)
    
    #filter duplicate
    artist_df = Transform.filter_duplicate(df=artist_df,ids= Transform.get_existing_ids(engine=engine,table_name="artist"))
    album_df = Transform.filter_duplicate(df=album_df,ids= Transform.get_existing_ids(engine=engine,table_name="album"))
    track_df = Transform.filter_duplicate(df=track_df,ids= Transform.get_existing_ids(engine=engine,table_name="track"))
    transform_end_time = time()
    
    #Load tasks
    load_start_time = time()
    dfs = [artist_df, album_df, track_df, artist_genre_df, artist_track_df, artist_album_df,track_album_df]
    tables = ["artist",'album','track','artist_genre','artist_track','artist_album','track_album']
    for df,table in zip(dfs,tables):
        try:
            Load.load_to_db(df=df,table_name=table,engine=engine)
            load_end_time = time()
        except Exception as err:
            print(f"Error when loading to table {table}")
            print(err)
            return
        
    extract_duration = extract_end_time - extract_start_time
    transform_duration = transform_end_time - transform_start_time
    load_duration = load_end_time - load_start_time   
    logger.info(f"Pipeline duration:{extract_duration + transform_duration + load_duration}")
    logger.info(f"Extract duration:{extract_duration}")
    logger.info(f"Transform duration:{transform_duration}")
    logger.info(f"Load duration:{load_duration}")

    
    

if __name__ == '__main__':
    main()
    