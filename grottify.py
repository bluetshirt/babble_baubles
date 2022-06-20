import sys
import spotipy
import spotipy.util as util
import os       
                    
class GrottifyException(Exception):
    pass
    
def enqueue(query):
    return act(query, enqueue=True)

def like(query):
    return act(query, like=True)

def act(query, enqueue=False, like=False):

    SPOTIPY_CLIENT_ID = os.environ.get("GROTTIFY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET = os.environ.get("GROTTIFY_CLIENT_SECRET")
    SPOTIPY_REDIRECT_URI = os.environ.get("GROTTIFY_REDIRECT_URI")

    USERNAME = os.environ.get("GROTTIFY_USERNAME")
    
    scope = 'user-library-read user-modify-playback-state user-read-private user-library-modify'

    token = util.prompt_for_user_token(
        USERNAME, scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

    name = "" 
    artists = ""
    id = "" 

    if token:
        sp = spotipy.Spotify(auth=token)
        
        results = sp.search(query)
        
        results_count = len(results['tracks']['items'])
        
        if results_count > 0:
            try:
                track = results['tracks']['items'][0]
                name = track['name']
                artists = ", ".join([artist['name'] for artist in track['artists']])
                id = track['id']
            except Exception as e: 
                raise GrottifyException(e)
        else:
            raise GrottifyException("no results")
        
        track_string = "%s - %s" % (artists, name)
        
        if like: 
            #print("liking %s" % track_string)
            if sp.current_user_saved_tracks_contains([id])[0]:
                #print("you already like this!")
                return (artists, name, False)
            else:
                sp.current_user_saved_tracks_add([id])
                #print("liked!")
                return (artists, name, True)
                
        if enqueue:
            #print("queueing %s" % track_string) 
            try:
                sp.add_to_queue(id)
                return (artists, name, True)
            except spotipy.SpotifyException as se:
                raise GrottifyException("oops - maybe you don't have a queue right now.")


    else:
        raise GrottifyException("Can't get token for % s" % username)
    
   
def getGrotty():
    return "you got grote"
    
    