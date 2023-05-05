from musicbrainzngs import search_artists, set_useragent



# Set up MusicBrainz API
set_useragent(os.environ.get("MUSICBRAINZ_APP"), "1.0")

def get_musicbrainz_artist(mbid):
    return search_artists(mbid=mbid, limit=1)