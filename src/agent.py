import os
import json
import re
from dotenv import load_dotenv
from groq import Groq
from src.recommender import load_songs, score_song
from src.logger import get_logger

load_dotenv()
log = get_logger("agent")
MODEL = "llama-3.3-70b-versatile"

EXTRACT_PROMPT = """Extract music preferences from the user's request and return ONLY a valid JSON object with these fields:
- mood: one of happy, chill, intense, melancholic, energetic, relaxed, moody, romantic, nostalgic, peaceful, uplifting, dark, dreamy, focused
- genre: one of pop, rock, hip-hop, jazz, classical, electronic, r&b, folk, country, metal, reggae, blues, indie, soul, ambient, lofi, latin, punk, funk (pick closest match)
- energy: float 0.0 to 1.0
- acousticness: float 0.0 to 1.0
- k: integer, always 10

Return ONLY the JSON. No explanation."""

EXPLAIN_PROMPT = """You are a music recommender. The user made a request and the system found matching songs.
Present exactly 5 songs as a numbered playlist. For each song, show the title, artist, and score on the first line (e.g. "1. Song Title - Artist | score: 0.87"), then explain in 1-2 sentences why it fits the request using natural language only — no numbers, percentages, or technical values in the explanation.
If variety was limited, mention it briefly at the end."""


class DJAgent:
    def __init__(self, songs_path: str):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            log.error("GROQ_API_KEY not found. Copy .env.example to .env and add your key.")
            raise SystemExit(1)

        self.songs = load_songs(songs_path)
        self.client = Groq(api_key=api_key)

    def _search_songs(self, mood="", genre="", energy=0.5, acousticness=0.5, k=5):
        prefs = {"mood": mood, "genre": genre, "energy": energy, "acousticness": acousticness}
        log.info(f"search_songs: {prefs}, k={k}")

        scored = []
        for song in self.songs:
            sc, _ = score_song(prefs, song)
            scored.append({
                "id": song["id"],
                "title": song["title"],
                "artist": song["artist"],
                "genre": song["genre"],
                "mood": song["mood"],
                "energy": song["energy"],
                "score": round(sc, 2),
            })

        results = sorted(scored, key=lambda x: x["score"], reverse=True)[:int(k)]
        log.info(f"search_songs result: {[s['title'] for s in results]}")
        return results

    def _check_variety(self, songs):
        genre_counts: dict = {}
        for s in songs:
            genre_counts[s["genre"]] = genre_counts.get(s["genre"], 0) + 1
        total = len(songs)
        variety_ok = total == 0 or max(genre_counts.values()) / total <= 0.6
        log.info(f"check_variety: variety_ok={variety_ok}, genres={genre_counts}")
        return variety_ok, genre_counts

    def _extract_prefs(self, user_request: str) -> dict:
        response = self.client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": EXTRACT_PROMPT},
                {"role": "user", "content": user_request},
            ],
        )
        raw = response.choices[0].message.content or ""
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse preferences from: {raw}")
        prefs = json.loads(match.group())
        log.info(f"Extracted prefs: {prefs}")
        return prefs

    def run(self, user_request: str) -> str:
        log.info(f"Request: {user_request!r}")

        # Step 1: extract preferences
        prefs = self._extract_prefs(user_request)

        # Step 2: search songs
        results = self._search_songs(
            mood=prefs.get("mood", ""),
            genre=prefs.get("genre", ""),
            energy=float(prefs.get("energy", 0.5)),
            acousticness=float(prefs.get("acousticness", 0.5)),
            k=int(prefs.get("k", 10)),
        )

        # Step 3: Python checks variety — retry with relaxed genre if poor
        variety_ok, genre_counts = self._check_variety(results)
        if not variety_ok:
            log.info("Variety poor — retrying with relaxed genre")
            results = self._search_songs(
                mood=prefs.get("mood", ""),
                genre="",
                energy=float(prefs.get("energy", 0.5)),
                acousticness=float(prefs.get("acousticness", 0.5)),
                k=int(prefs.get("k", 10)),
            )
            variety_ok, genre_counts = self._check_variety(results)

        # Step 4: model explains results
        variety_note = "" if variety_ok else f"\nNote: variety was limited ({genre_counts})."
        explain_input = f'User request: "{user_request}"\n{variety_note}\nSearch results:\n{json.dumps(results[:10], indent=2)}'

        final = self.client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": EXPLAIN_PROMPT},
                {"role": "user", "content": explain_input},
            ],
        )
        return final.choices[0].message.content or "No response generated."