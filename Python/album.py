class Album():
    def __init__(self, artist: str, name: str, rating: int, sunday: bool,  count: int, uri: str, length: float, last_played: str) -> None:
        self.artist = artist
        self.name = name
        self.sunday = sunday
        self.rating = rating
        self.count = count
        self.uri = uri
        self.length = length
        self.last_played = last_played

    def __repr__(self) -> str:
        title = f"{self.artist} - {self.name}"
        if(self.last_played == None):
            last_played = f"{self.name} hasn't been played yet"
        else:
            last_played = f"Last played: {self.last_played}"
        if(self.rating == ""):
            rating_text = "There is no rating info"
        else:
            ratings = [int(x) for x in self.rating.split(",") if x != ""]
            rating_text = sum(ratings) / len(ratings)
        sep = "#" * len(title)
        return f"\n{title}\n{sep}\nSunday?: {self.sunday}\nRating: {rating_text}\nCount: {self.count}\nLength: {self.length} minutes\n{last_played}\n{sep}"
