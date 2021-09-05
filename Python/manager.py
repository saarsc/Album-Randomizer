#!"C:\Users\scsaa\Documents\Random-Scripts\Album Randomizer\Python\venv\Scripts\python.exe"
from genericpath import exists
from InquirerPy import prompt
from util import getAlbums, getAllGenres, initCheckboxes, playAlbum, selectRandomAlbum, groupArtists, getAllAlbums, removeData, updateSunday, reset

from db import addAlbums, closeDB, getInfo, increaseCount, remove, updateRating

from os.path import isfile
from os.path import dirname, abspath
import os
import datetime

LAST_PLAY_PATH = f"{dirname(abspath(__file__))}/last_played"


def generateQuestion(type: str = "list", name: str = "", message: str = "",  types: list[str] = None, names: list[str] = None, messages: list[str] = None, choices: list[str] = None, default: bool = None):
    """
        Generate a list elements for the prompt command

        @Parms:
            -type: the type of the question
            -name: the name of the question
            -message: Message to be displayed with the question
            -types: A list of types for multiple questions
            -names: A list of names for multiple questions
            -messages: A list of messages for multiple questions
            -choices: A list for questions which supports chochies i.e checkboxes
            -defualt: Wheater the option is defulat or not, can be both bool or a list of bools in the case of multiple questions

        @return
            a list with question objects
    """
    question = []
    if types is not None:
        for i, type in enumerate(types):
            question.append({
                "type": type,
                "name": names[i],
                "message": messages[i],
                'choices': choices[i],
                "default": default[i],
                'qmark': '📻'
            })
    else:
        question.append({
            "type": type,
            "name": name,
            "message": message,
            'choices': choices,
            "default": default,
            'qmark': '📻'
        })
    return question


def mainScreen():
    """
        Disaplys the main menu.
    """
    pickAction = generateQuestion(name='actions', message="Choose an action", choices=[
                                  'add artist', "Pick album", 'get info', "Manage DB"])
    answers = prompt(pickAction).get("actions")
    if answers == "add artist":
        handleArtistPick()
    if answers == "get info":
        handleGetInfo()
    if answers == "Pick album":
        pickAlbum()
    if answers == "Manage DB":
        manageDB()


def handleArtistPick():
    """
        Handles the add artist option from the main screen
    """
    def selectAlbums(artist):
        """
            Disaplys a checkbox prompt for the user to pich which albums they would like to enable

            @Parms:
                - artist: the name of the artist to add
        """
        question = generateQuestion(types=["checkbox", "confirm"], messages=[
                                    f"Select albums for {artist}", "Is this a sunday artist?"], names=["albums", "sunday"], default=[" ", False], choices=[initCheckboxes(list(getAlbums(artist))).sort(), None])
        albums = prompt(question)
        print(albums)
        addAlbums(albums["sunday"],
                  albums["albums"], artist)

    addAritst = generateQuestion(
        type="input", name="artistName", message="enter artist name/ file path:", default="")

    artistPick = prompt(addAritst)
    artist = artistPick["artistName"]
    if isfile(artist):
        with open(artist) as f:
            artists = f.readlines()
        for artist in artists:
            selectAlbums(artist.strip())
    else:
        selectAlbums(artist)


def handleGetInfo():
    """
        Handles the get option from the main screen. Disaplys stats of the user selected album
    """
    albumsList = getAllAlbums()

    q = generateQuestion(
        type="fuzzy", message="Select actions:", choices=albumsList, name="name")
    print(albumsList)

    print(getInfo(prompt(q)["name"]))


def pickAlbum():
    """
        Handles the pick album option from the main screen. Based on the user category selects a random album.

        Categories: Aritst, Genre or random
    """
    def checkForSunday() -> bool:
        """
            In the case the current day is sunday ask if the user would like to hear a sunday album or not

            @return
                bool
        """
        sunday = False
        if (datetime.datetime.today().weekday() + 1) % 7 == 0:
            question = generateQuestion(
                type="confirm", message="Loos like this is a sunday. Would you like a sunday artist?", name="sunday", default=True)
            sunday = prompt(question)["sunday"]
        return sunday

    happyWithSelectionPromt = generateQuestion(
        "confirm", "ok", "Is this OK?", default=True)
    sunday = checkForSunday()
    selectBy = generateQuestion(name="select_by", message="Select By:", choices=[
                                "Random", "Genre", "Artist", "Length"])
    selectBy = prompt(selectBy)["select_by"]
    selected = False
    while not selected:
        if selectBy == "Random":
            album = selectRandomAlbum(sunday)
        elif selectBy == "Artist":
            selectArtist = generateQuestion(type="fuzzy",
                                            name="artist", message="Select By:", choices=groupArtists(sunday))
            artist = prompt(selectArtist)["artist"]
            album = selectRandomAlbum(sunday, artist=artist)
        elif selectBy == "Genre":
            selectGenre = generateQuestion(
                type="fuzzy", message="Select Genre:", choices=getAllGenres(), name="genre")
            genre = prompt(selectGenre)["genre"].split("-")[0].strip()
            print(genre)
            album = selectRandomAlbum(sunday=sunday, genre=genre)
        elif selectBy == "Length":
            slecetLength = generateQuestion(
                type="list", message="Select Length:", choices=["Short", "Normal", "Long"], name="length")
            length = prompt(slecetLength)["length"].split("-")[0].strip()
            print(length)
            album = selectRandomAlbum(sunday=sunday, length=length)
        print(album)

        selected = prompt(happyWithSelectionPromt)["ok"]
    with open(LAST_PLAY_PATH, "w") as f:
        f.write(f"{album.uri}-{album.name}")
    playNow = prompt(generateQuestion("confirm", "playNow",
                     f"Do you wish to play {album.name} now?", default=True))["playNow"]
    if playNow:
        playAlbum(album.uri)
    increaseCount(album.name)


def manageDB():
    q = prompt(generateQuestion(name="action", choices=[
               "Remove artist", "Remove album", "Change sunday", "Reset DB", "Back"], message="Select action:"))["action"]
    if q == "Remove artist":
        pickArtist = prompt(generateQuestion(
            "fuzzy", "artist", "Select artist:", choices=groupArtists(False)))["artist"]
        confirm = prompt(generateQuestion("confirm", "confirm",
                         f"Are you sure you want to remove {pickArtist}", default=False))
        if confirm:
            removeData(pickArtist, isArtist=True)
        else:
            manageDB()
    if q == "Remove album":
        pickAlbum = prompt(generateQuestion(
            "fuzzy", "album", "Select album:", choices=getAllAlbums()))["album"]
        confirm = prompt(generateQuestion("confirm", "confirm",
                                          f"Are you sure you want to remove {pickAlbum}", default=False))
        if confirm:
            removeData(pickAlbum, isAlbum=True)
        else:
            manageDB()
    if q == "Change sunday":
        pickArtist = prompt(generateQuestion(
            "fuzzy", "artist", "Select artist:", choices=groupArtists(False)))["artist"]
        confirm = prompt(generateQuestion("confirm", "confirm",
                         f"Are you sure you want to update the sunday value of {pickArtist}", default=False))
        if confirm:
            updateSunday(pickArtist)
        else:
            manageDB()
    if q == "Reset DB":
        reset()
    if q == "Back":
        mainScreen()


def handleRateArtist():
    if(exists(LAST_PLAY_PATH)):
        with open(LAST_PLAY_PATH,"r") as f:
            album_uri, album_name = f.readline().split("-")
        rating = prompt(generateQuestion("input", "rating",
                        f"How would you rate {album_name}?",default=''))["rating"]
        updateRating(album_uri, rating)
        os.remove(LAST_PLAY_PATH)


def main():
    quit = False
    handleRateArtist()
    while not quit:
        try:
            mainScreen()
        except KeyboardInterrupt:
            quit = True
    closeDB()


if __name__ == "__main__":
    main()
