# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

**Next Song Please 1.0**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

It recommends songs from the dataset based on a user's mood, genre, energy level, and acoustic level. Made for classroom exploration.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Songs are scored on a scale of 0 to 1. Mood matching is exact and makes up 35% of a song's score. Genre match accounts for 20%. Energy similarity makes up 30%, and acousticness similarity makes up 15%. Once the songs are scored, the top 5 songs are recommended.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The dataset has 20 songs with columns genre, mood, energy, tempo, valence, danceability, and acousticness. Genres include pop, rock, r&b, etc. Some genres only appear once, and there are genres missing.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system seems to work best when a user's preferences are common genres and moods (in the dataset). For example, chill lofi and intense rock got good recommendations with pretty high scores.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The mood matching uses exact string comparisons, so songs that have the same feeling described in different labels are treated as different. Since mood carries the highest weight in the formula, a mood mismatch can lower the score of an otherwise very fitting song.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I tested 6 user profiles: 
1. High energy pop - preferred loud "happy" songs.
2. Chill lofi - preferred more soft acoustic songs.
3. Deep intense rock - preferred high energy & low acoustic songs. Its recommendations had high score results.
4. High energy melancholic rock - got recommended a slow song because mood outweighs genre.
5. Bossa nova - genre doesn't exist in the dataset, so it was ignored. The system relied on the other 3 factors.
6. High energy & high acoustic folk - combo is less common, so results weren't the best.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

Since scoring by mood is limiting the system, grouping similar moods together for a mood match would improve it. Dataset could also definitely use some more songs.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

With this project, I saw the math behind how recommenders actually work (and how they don't work sometimes). It was interesting to see how even the simple scoring logic I was working with can affect results.