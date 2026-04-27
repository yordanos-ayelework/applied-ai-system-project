import argparse
from src.recommender import load_songs, recommend_songs

user_profiles = [
    {"genre": "pop",        "mood": "happy",       "energy": 0.90, "acousticness": 0.10},  # high-energy pop
    {"genre": "lofi",       "mood": "chill",        "energy": 0.35, "acousticness": 0.85},  # chill lofi
    {"genre": "rock",       "mood": "intense",      "energy": 0.92, "acousticness": 0.08},  # deep intense rock
    {"genre": "rock",       "mood": "melancholic",  "energy": 0.90, "acousticness": 0.10},  # edge case: conflicting mood vs energy
    {"genre": "bossa nova", "mood": "relaxed",      "energy": 0.40, "acousticness": 0.80},  # edge case: genre not in dataset
    {"genre": "folk",       "mood": "intense",      "energy": 0.92, "acousticness": 0.90},  # edge case: high energy + high acoustic
]


def run_sim() -> None:
    print("Next Song Please 1.0.\n")
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


def run_agent() -> None:
    from src.agent import DJAgent
    agent = DJAgent("data/songs.csv")
    print("Next Song Please 2.0: Type your request or 'quit' to exit.\n")

    while True:
        request = input("What are you in the mood for? ").strip()
        if request.lower() in ("quit", "exit", "q"):
            break
        if not request:
            continue
        print("\nThinking...\n")
        try:
            response = agent.run(request)
            print(response)
        except Exception:
            print("Something went wrong — try rephrasing your request.")
        print("\n" + "-" * 60 + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Next Song Please 2.0")
    parser.add_argument(
        "--mode",
        choices=["sim", "agent"],
        default="sim",
        help="sim: run hardcoded profile simulation | agent: interactive AI recommender",
    )
    args = parser.parse_args()

    if args.mode == "agent":
        run_agent()
    else:
        run_sim()


if __name__ == "__main__":
    main()
