from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

from config import *
from pprint import PrettyPrinter, pprint
from db import KEY_NAME, addAlbum, changeSunday, getGenres, resetDB, getAllArtist, getAllAlbumsNames, remove, updateRating
from db import selectRandomAlbum as randomAlbum
from db import KEY_ARTIST
# spotify = Spotify(auth_manager=SpotifyClientCredentials(
#     CLIENT_ID, CLIENT_SECRET))
spotify = Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                  redirect_uri=REDIRECT_URL, scope="user-modify-playback-state,streaming,user-read-playback-state"))


def getAlbums(artist: str) -> set[str]:
    """
        Lists all the artist albums from spotify

        @artist: artist name

        @return a set of all the artist albums names
    """

    def calculateLength(id: str):
        """
            Calculate the length of the album in minutes

            @id: album's Spotify id

            @retrun the length of the album
        """
        albums = spotify.album_tracks(id, market="IL")["items"]
        length = 0
        for album in albums:
            length += album["duration_ms"]

        return round((length/(1000*60)) % 60)

    artistAlbums = set()
    genres, id = getId(artist)
    genres = ",".join(genres)
    results = spotify.artist_albums(
        id, album_type="album", country="IL")

    albums = results['items']
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])

    for album in albums:
        addAlbum(album["name"].title(), artist.title(), False,
                 calculateLength(album["id"]), genres.replace("-", " "),album["uri"])
        artistAlbums.add(album['name'])

    return artistAlbums


def getId(artist: str) -> tuple[str]:
    """
        Gets the generes and the artist id from Spotify

        @artist: artist name

        @return artist genres , artist spotify ID
    """
    info = spotify.search(artist, type='artist', market="IL")[
        "artists"]["items"][0]
    return (info["genres"], info["id"])


def initCheckboxes(options: set[str]) -> list[str]:
    """
        Creates a checkbox prompt based of a list of strings

        @options: data to convert into a checkbox prompt object

        @return a list of checkbox format data
    """
    choices = []
    for el in options:
        choices.append({
            'name': el,
            'value': el,
            "enabled": True
        })
    return choices


def groupArtists(sunday: bool) -> set[str]:
    """
        Returns a list of artist

        @sunday: Whether the artist is a sunday artist(AKA artist I'm testing ATM)

        @return a set of artists names

    """
    artists = set()
    for artist in getAllArtist(sunday):
        artists.add(artist[0])
    return artists


def selectRandomAlbum(sunday: bool, **kw) -> str:
    """
        picks a random album

        @sunday: Whether the artist is a sunday artist(AKA artist I'm testing ATM)
        @artist[optional]: which artist to use
        @genre[optional]: which genre to use
        @Length[optional]: Select by album length [Short, Noraml, Long]
    """
    print(kw)
    return randomAlbum(sunday, **kw)


def getAllAlbums() -> list[str]:
    """
        Get all of the albums names

        @return a set of all the albums names 
    """
    albums = []
    for option in getAllAlbumsNames():
        albums.append(option[0])
    return albums


def getAllGenres():
    artistList = {}

    for genre in getGenres():
        for g in genre[0].split(","):
            if g not in artistList:
                artistList[g] = f"{g} - {genre[1]}"
            else:
                artistList[g] += f", {genre[1]}"
    return artistList.values()


def playAlbum(uri: str) -> None:
    def getDeviceId():
        devices = spotify.devices()["devices"]
        for device in devices:
            if device["name"] == "Bedroom":
                return device["id"]
    id = getDeviceId()
    spotify.start_playback(id, context_uri=uri)


def removeData(what: str, isArtist: bool = False, isAlbum: bool = False) -> None:
    if isArtist:
        remove(what, KEY_ARTIST)
    elif isAlbum:
        remove(what, KEY_NAME)


def updateSunday(artist: str) -> None:
    changeSunday(artist)

def addRating(uri: str,rating: str) -> None:
    updateRating(uri,rating)

def reset():
    resetDB()


# print(spotify.start_playback(device_id="28e875bd94e696fbc4ba8efef112756beb2ca6b3",uris=["spotify:track:7eEEgizmmwDNvdUI7yOiAF"]))
