from src.recommender import Song, UserProfile, Recommender, score_song


def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_perfect_match_scores_higher_than_no_match():
    perfect = Song(id=1, title="Perfect", artist="A", genre="pop", mood="happy",
                   energy=0.9, tempo_bpm=120, valence=0.9, danceability=0.8, acousticness=0.1)
    no_match = Song(id=2, title="No Match", artist="B", genre="metal", mood="dark",
                    energy=0.1, tempo_bpm=60, valence=0.1, danceability=0.2, acousticness=0.9)
    user = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.9, likes_acoustic=False)
    rec = Recommender([perfect, no_match])
    results = rec.recommend(user, k=2)

    assert results[0].title == "Perfect"


def test_score_is_between_0_and_1():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "acousticness": 0.2}
    song = {"genre": "rock", "mood": "chill", "energy": 0.5, "acousticness": 0.7}
    score, _ = score_song(prefs, song)

    assert 0.0 <= score <= 1.0


def test_recommend_returns_k_songs():
    rec = make_small_recommender()
    user = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.8, likes_acoustic=False)

    assert len(rec.recommend(user, k=1)) == 1
    assert len(rec.recommend(user, k=2)) == 2