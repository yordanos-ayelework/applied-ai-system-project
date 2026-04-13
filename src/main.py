"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

user_profiles = [
    {"genre": "pop",        "mood": "happy",       "energy": 0.90, "acousticness": 0.10},  # high-energy pop
    {"genre": "lofi",       "mood": "chill",        "energy": 0.35, "acousticness": 0.85},  # chill lofi
    {"genre": "rock",       "mood": "intense",      "energy": 0.92, "acousticness": 0.08},  # deep intense rock
    {"genre": "rock",       "mood": "melancholic",  "energy": 0.90, "acousticness": 0.10},  # edge case: conflicting mood vs energy
    {"genre": "bossa nova", "mood": "relaxed",      "energy": 0.40, "acousticness": 0.80},  # edge case: genre not in dataset
    {"genre": "folk",       "mood": "intense",      "energy": 0.92, "acousticness": 0.90},  # edge case: high energy + high acoustic
]


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for user_prefs in user_profiles:
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\n" + "=" * 85)
        print(f"Prefs: {user_prefs}")
        print("=" * 85)
        for i, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n#{i}  {song['title']} by {song['artist']}")
            print(f"    Score: {score:.2f}")
            print("    Reasons:")
            for reason in explanation.split(", "):
                print(f"      - {reason}")
    print("\n" + "=" * 45)


if __name__ == "__main__":
    main()
