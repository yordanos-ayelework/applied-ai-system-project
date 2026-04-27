# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**Next Song Please 2.0**

---

## 2. Intended Use  

This system recommends songs from a dataset based on descriptions of what a user is in the mood for. 

---

## 3. How the Model Works  

The AI reads the user's request and extracts structured preferences like mood, genre, and energy level. Then, every song in the catalog is scored using a weighted formula. Mood match accounts for 35%, energy similarity for 30%, genre match for 20%, and acousticness similarity for 15%. Python checks variety and retries if needed. Finally, the AI receives the scored results and writes an explanation of why each song fits the request.
---

## 4. Data  

The dataset contains about 1,000 songs sourced from the Spotify Tracks Dataset on Kaggle, filtered for popularity and distributed across 19 genres. Audio features (energy, acousticness, valence, danceability, tempo) come from Spotify's own measurements. Mood labels were derived from valence and energy using a threshold-based formula since the original dataset had no mood field.

---

## 5. Strengths  

The system seems to work best when requests are grounded in mood and energy (e.g. "gym hype" and "sad rainy music"). Additionally, because of the scoring formula, every recommendation comes with a score that explains why it ranked where it did.

---

## 6. Limitations and Bias 

The mood matching uses exact string comparisons, so songs that have the same feeling described in different labels are treated as unrelated. The dataset has no attributes for artist style, demographics, or cultural context, so requests rooted in those attributes (e.g. "girly pop", "African party music") produce weak results. The 1,000 song catalog is also small compared to real music services, which limits diversity. Genres with historically mainstream representation have more high-popularity options than niche genres, which may bias results toward popular western music.

---

## 7. Evaluation  

5/5 automated tests passed. Verified that the recommender sorts songs correctly, returns the right number of results, scores between 0 and 1, and always ranks a perfect match above a no-match.

Manual testing across a range of requests confirmed that the system consistently retrieves real songs before generating a response.

---

## 8. Ethics and Misuse 

The system itself poses minimal misuse risk as it only recommends songs. However, the architecture (using an LLM to understand intent and retrieve results) is a pattern that could be applied to many domains. In those contexts, the exact match bias and limited dataset diversity could cause harm by systematically excluding certain demographics.

---

## 9. Future Work

Grouping similar moods semantically would significantly improve results. Adding artist or style tags to the dataset would also help with vague requests. A larger catalog and collaborative filtering (recommendations based on what similar users liked) would bring it closer to a real music service.

---

## 10. Personal Reflection  

I was surprised by how often the model generated wrong tool calls for simple requests. Reliability required more tinkering and engineering than I expected.

I used Claude Code throughout this project. A helpful suggestion was moving the variety check from an LLM tool call into Python code, which made the system significantly more reliable. It previously kept saying that something was wrong and to try rephrasing the request. A flawed suggestion was recommending Gemini as a free LLM to use for API calls when it wasn't, which wasted some time.