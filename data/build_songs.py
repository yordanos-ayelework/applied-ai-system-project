"""
One-time script to convert the Kaggle Spotify Tracks Dataset
into the songs.csv format used by Next Song Please 2.0.

Run from project root: python data/build_songs.py
"""
import csv
import random

random.seed(42)

GENRE_MAP = {
    "acoustic":         "folk",
    "alt-rock":         "rock",
    "alternative":      "rock",
    "ambient":          "ambient",
    "blues":            "blues",
    "bluegrass":        "folk",
    "chill":            "lofi",
    "classical":        "classical",
    "club":             "electronic",
    "country":          "country",
    "dance":            "electronic",
    "dancehall":        "reggae",
    "death-metal":      "metal",
    "deep-house":       "electronic",
    "disco":            "funk",
    "drum-and-bass":    "electronic",
    "dub":              "reggae",
    "dubstep":          "electronic",
    "edm":              "electronic",
    "electro":          "electronic",
    "electronic":       "electronic",
    "folk":             "folk",
    "funk":             "funk",
    "gospel":           "soul",
    "grunge":           "rock",
    "guitar":           "folk",
    "hard-rock":        "rock",
    "hardcore":         "metal",
    "heavy-metal":      "metal",
    "hip-hop":          "hip-hop",
    "house":            "electronic",
    "indie":            "indie",
    "indie-pop":        "indie",
    "j-pop":            "pop",
    "jazz":             "jazz",
    "k-pop":            "pop",
    "latin":            "latin",
    "metal":            "metal",
    "metal-misc":       "metal",
    "metalcore":        "metal",
    "new-age":          "ambient",
    "opera":            "classical",
    "piano":            "classical",
    "pop":              "pop",
    "pop-film":         "pop",
    "power-pop":        "pop",
    "progressive-house":"electronic",
    "psych-rock":       "rock",
    "punk":             "punk",
    "punk-rock":        "punk",
    "r-n-b":            "r&b",
    "rainy-day":        "lofi",
    "reggae":           "reggae",
    "reggaeton":        "latin",
    "rock":             "rock",
    "rock-n-roll":      "rock",
    "romance":          "r&b",
    "sad":              "lofi",
    "salsa":            "latin",
    "singer-songwriter":"folk",
    "sleep":            "ambient",
    "soul":             "soul",
    "study":            "lofi",
    "synth-pop":        "pop",
    "techno":           "electronic",
    "trance":           "electronic",
    "trip-hop":         "lofi",
    "work-out":         "hip-hop",
}

KEEP_GENRES = {
    "pop", "rock", "hip-hop", "jazz", "classical", "electronic",
    "r&b", "folk", "country", "metal", "reggae", "blues", "indie",
    "soul", "ambient", "lofi", "latin", "punk", "funk",
}

PER_GENRE = 53  # ~1000 total across 19 genres


def derive_mood(valence: float, energy: float) -> str:
    if valence >= 0.6 and energy >= 0.6:
        return "happy"
    elif valence >= 0.6 and energy < 0.4:
        return "relaxed"
    elif valence >= 0.5:
        return "chill"
    elif energy >= 0.7:
        return "intense"
    elif valence < 0.35 and energy < 0.35:
        return "melancholic"
    elif valence < 0.35:
        return "moody"
    elif energy >= 0.55:
        return "energetic"
    else:
        return "chill"


def main():
    by_genre: dict = {g: [] for g in KEEP_GENRES}
    seen: set = set()

    with open("data/dataset.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_genre = row["track_genre"].strip()
            genre = GENRE_MAP.get(raw_genre)
            if genre not in KEEP_GENRES:
                continue

            title = row["track_name"].strip()
            artist = row["artists"].strip().split(";")[0]
            key = (title.lower(), artist.lower())
            if key in seen:
                continue

            try:
                popularity = int(row["popularity"])
                energy = float(row["energy"])
                acousticness = float(row["acousticness"])
                valence = float(row["valence"])
                danceability = float(row["danceability"])
                tempo = float(row["tempo"])
            except (ValueError, KeyError):
                continue

            if popularity < 50:
                continue

            if not all(ord(c) < 128 for c in title):
                continue

            seen.add(key)
            by_genre[genre].append({
                "title": title,
                "artist": artist,
                "genre": genre,
                "mood": derive_mood(valence, energy),
                "energy": round(energy, 2),
                "tempo_bpm": round(tempo),
                "valence": round(valence, 2),
                "danceability": round(danceability, 2),
                "acousticness": round(acousticness, 2),
            })

    songs = []
    for genre, tracks in by_genre.items():
        sample = sorted(tracks, key=lambda x: random.random())[:PER_GENRE]
        songs.extend(sample)

    random.shuffle(songs)

    with open("data/songs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "title", "artist", "genre", "mood",
            "energy", "tempo_bpm", "valence", "danceability", "acousticness"
        ])
        writer.writeheader()
        for i, song in enumerate(songs, start=1):
            writer.writerow({"id": i, **song})

    print(f"Wrote {len(songs)} songs to data/songs.csv")
    genre_counts = {}
    for s in songs:
        genre_counts[s["genre"]] = genre_counts.get(s["genre"], 0) + 1
    for g, count in sorted(genre_counts.items()):
        print(f"  {g}: {count}")


if __name__ == "__main__":
    main()