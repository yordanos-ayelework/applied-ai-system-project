from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """
        Return the top-k songs ranked by match to the given user's preferences.
        """
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Return a human-readable explanation of why a song was recommended to the user.
        """
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv

    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in int_fields:
                if field in row:
                    row[field] = int(row[field])
            for field in float_fields:
                if field in row:
                    row[field] = float(row[field])
            songs.append(dict(row))
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by src/main.py
    """
    score = 0.0
    reasons = []

    if song.get("mood") == user_prefs.get("mood"):
        score += 0.35
        reasons.append("mood match (+0.35)")

    energy_sim = 1 - abs(user_prefs.get("energy", 0.5) - song.get("energy", 0.5))
    score += 0.30 * energy_sim
    reasons.append(f"{energy_sim:.0%} energy similarity (+{0.30 * energy_sim:.2f})")

    if song.get("genre") == user_prefs.get("genre"):
        score += 0.20
        reasons.append("genre match (+0.20)")

    acoustic_sim = 1 - abs(user_prefs.get("acousticness", 0.5) - song.get("acousticness", 0.5))
    score += 0.15 * acoustic_sim
    reasons.append(f"{acoustic_sim:.0%} acousticness similarity (+{0.15 * acoustic_sim:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [
        (song, score, ", ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
