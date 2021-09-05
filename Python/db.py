from sqlite3 import connect, Cursor
from album import Album
from datetime import date
from os.path import dirname, abspath
con = connect(f"{dirname(abspath(__file__))}/albums.db")
cur = con.cursor()

TB_NAME = "albums"
KEY_ID = "id"
KEY_ARTIST = "artist"
KEY_NAME = "name"
KEY_RATING = "rating"
KEY_PLAY_COUNT = "count"
KEY_SUNDAY = "sunday"
KEY_LENGTH = "LENGTH"
KEY_STATUS = "status"
KEY_GENRES = "genres"
KEY_LAST_PLAYED = "last_played"
KEY_URI = "album_uri"
# Creating the DB


def initDB() -> None:
    """
        Initalize the DB, create tables and such.
    """
    cur.execute(
        f"CREATE TABLE IF NOT EXISTS '{TB_NAME}' ({KEY_ID} INTEGER PRIMARY KEY, {KEY_ARTIST} TEXT, {KEY_NAME} TEXT, {KEY_RATING} TEXT DEFAULT '', {KEY_PLAY_COUNT} INTEGER DEFAULT 0, {KEY_SUNDAY} BOOLEAN, {KEY_LENGTH} FLOAT, {KEY_STATUS} BOOLEAN DEFAULT FALSE, {KEY_GENRES} TEXT,{KEY_LAST_PLAYED} TEXT DEFAULT null, {KEY_URI} TEXT)")
    con.commit()


def addAlbum(name: str, artist: str, sunday: bool, length: float, genres: str, uri: str) -> None:
    """
        Adds an album in to the db. the album is added when adding a new artist, and defaults to not aviable.

        @name: The name of the album
        @artitst: Artist name
        @sunday: Whether the artist is a sunday artist(AKA artist I'm testing ATM)
        @length: The length of the album in minutes
        @genres: comma sperated string to reprsent to artist / album genres
        @uri - Album URI. used to be played later
    """
    if not len(cur.execute(
            f"SELECT * FROM {TB_NAME} WHERE {KEY_ARTIST} = ? AND {KEY_NAME} = ?", (artist, name)).fetchall()):
        cur.execute(
            f"INSERT INTO {TB_NAME} ({KEY_ARTIST} , {KEY_NAME}, {KEY_SUNDAY}, {KEY_LENGTH}, {KEY_GENRES}, {KEY_URI}) VALUES(?, ?,?,?,?,?)", (artist, name, sunday, length, genres, uri))
        con.commit()


def addAlbums(sunday: bool, albums: set[str], artist: str) -> None:
    """
        Enables a list of albums

        @sunday: Whether the artist is a sunday artist(AKA artist I'm testing ATM)
        @albums: A set of strings with the albums names.
        @artist: artist name. To make sure no 2 albums with the same name but different artists are affected
    """
    for album in albums:
        cur.execute(
            f"UPDATE {TB_NAME} SET {KEY_STATUS} = true, {KEY_SUNDAY} = ? WHERE {KEY_NAME} = ? AND {KEY_ARTIST} = ?", (sunday, album, artist))
    con.commit()


def getAllAlbumsNames() -> Cursor:
    """
        Get all the album names

        @return Cursor object with a all of the albums
    """
    return cur.execute(f"SELECT {KEY_NAME} FROM {TB_NAME}")


def getAllArtist(sunday: bool) -> Cursor:
    """
        Get all the artist names

        @sunday: Whether the artist is a sunday artist(AKA artist I'm testing ATM)

        @return Cursor object with a all of the albums
    """
    return cur.execute(f"SELECT {KEY_ARTIST} FROM {TB_NAME} WHERE ({KEY_SUNDAY} = ? OR {KEY_SUNDAY} = TRUE) GROUP BY {KEY_ARTIST}", (sunday,)).fetchall()


def getGenres(sunday: bool = False) -> Cursor:
    """
        Pull all of the genres coulmn

    """
    return cur.execute(f"SELECT {KEY_GENRES}, {KEY_ARTIST} FROM {TB_NAME} WHERE ({KEY_SUNDAY} = ? OR {KEY_SUNDAY} = TRUE) GROUP BY {KEY_ARTIST}", (sunday,)).fetchall()


def getInfo(name: str) -> Album:
    """
        Get all the stats about an album

        @name: Album name

        @return Album object with all the stats
    """
    album = None
    for data in cur.execute(
            f"SELECT {KEY_ARTIST},{KEY_NAME},{KEY_RATING},{KEY_SUNDAY},{KEY_PLAY_COUNT},{KEY_URI},{KEY_LENGTH},{KEY_LAST_PLAYED} FROM {TB_NAME} WHERE {KEY_NAME}= ?", (name,)):
        album = Album(data[0], data[1], data[2],
                      data[3], data[4], data[5], data[6], data[7])
    return album


def selectRandomAlbum(sunday: bool, **kw) -> Album:
    """
        Picks a random albums based on the catagory

        @sunday: Whether the artist is a sunday artist(AKA artist I'm testing ATM)
        @artist: Artist name if selection is baesd on artist
        @genre: Genre if selection is based on genre

        @return one album name
    """

    if "artist" in kw:
        data = cur.execute(
            f"SELECT {KEY_ARTIST},{KEY_NAME}, {KEY_RATING}, {KEY_SUNDAY},{KEY_PLAY_COUNT}, {KEY_URI},{KEY_LENGTH},{KEY_LAST_PLAYED} FROM {TB_NAME} WHERE ({KEY_SUNDAY} = ? OR {KEY_SUNDAY} = TRUE) AND {KEY_ARTIST} = ? ORDER BY RANDOM() LIMIT 1", (sunday, kw["artist"])).fetchall()[0]
    if "genre" in kw:
        data = cur.execute(f"SELECT {KEY_ARTIST},{KEY_NAME}, {KEY_RATING}, {KEY_SUNDAY},{KEY_PLAY_COUNT}, {KEY_URI},{KEY_LENGTH},{KEY_LAST_PLAYED} FROM {TB_NAME} WHERE ({KEY_SUNDAY} = ? OR {KEY_SUNDAY} = TRUE) AND {KEY_GENRES} LIKE ? ORDER BY RANDOM() LIMIT 1", (
            sunday, f"%{kw['genre']}%")).fetchall()[0]
    if "length" in kw:
        data = cur.execute(
            f"SELECT {KEY_ARTIST},{KEY_NAME}, {KEY_RATING}, {KEY_SUNDAY},{KEY_PLAY_COUNT}, {KEY_URI},{KEY_LENGTH},{KEY_LAST_PLAYED}, (CASE WHEN  {KEY_LENGTH} < 40 THEN 'Short' WHEN  {KEY_LENGTH} < 50 THEN 'Normal' ELSE 'Long' END ) l FROM albums WHERE l = ? AND ({KEY_SUNDAY} = ? OR {KEY_SUNDAY} = TRUE) ORDER BY RANDOM() LIMIT 1", (kw["length"], sunday)).fetchall()[0]
    else:
        data = cur.execute(
            f"SELECT {KEY_ARTIST},{KEY_NAME}, {KEY_RATING}, {KEY_SUNDAY},{KEY_PLAY_COUNT}, {KEY_URI},{KEY_LENGTH}, {KEY_LAST_PLAYED} FROM {TB_NAME} WHERE ({KEY_SUNDAY} = ? OR {KEY_SUNDAY} = TRUE) ORDER BY RANDOM() LIMIT 1", (sunday,)).fetchall()[0]

    return Album(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])


def increaseCount(album: str) -> None:
    """
        Increses the listend count by 1 for the selected album

        @album: name of the album
    """
    today = date.today().strftime('%d/%m/%Y')
    print({today})
    cur.execute(
        f"UPDATE {TB_NAME} SET {KEY_PLAY_COUNT} = {KEY_PLAY_COUNT} +1, {KEY_LAST_PLAYED} = ? WHERE {KEY_NAME} = ?", (today, album,))
    con.commit()


def remove(who: str, by: str) -> None:
    cur.execute(f"DELETE FROM {TB_NAME} WHERE ? = ?", (by, who))
    con.commit()


def changeSunday(artist: str) -> None:
    cur.execute(
        f"UPDATE {TB_NAME} SET {KEY_SUNDAY} = NOT {KEY_SUNDAY} WHERE {KEY_ARTIST} = ?", (artist,))
    con.commit()


def updateRating(uri: str, rating: str) -> None:
    con.execute(
        f"UPDATE {TB_NAME} SET {KEY_RATING} = {KEY_RATING} || ? WHERE {KEY_URI} = ?", (f"{rating},", uri))
    con.commit()


def closeDB() -> None:
    """
        Gracefuly close the DB connection upon exiting
    """
    con.close()


def resetDB() -> None:
    """
        Resets the DB.
    """
    cur.execute(f"DROP TABLE IF EXISTS {TB_NAME}")
    con.commit()
    initDB()


initDB()
