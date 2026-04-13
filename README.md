# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

I built a rule-based music recommender that scores every song in a 20-song catalog against my user preference profile across seven features — mood, genre, energy, valence, tempo, danceability, and acousticness — and returns the top k results. I used a mood-first weighting strategy where mood carries the most points (up to 5), followed by genre (3 pts), with continuous features filling in the rest up to a maximum of 15.5 points total.

---

## How The System Works

Explain your design in plain language.

Each song is described by seven features: two categorical labels (genre and mood) and five decimal values between 0 and 1 — energy, valence, danceability, acousticness — plus tempo in BPM. The user profile stores a reference song or a set of target preferences across all seven features.

Scoring follows a mood-first weighting strategy. Mood is the highest-weighted attribute (5 pts for an exact match, 2.5 pts for a semantically similar mood cluster such as chill/relaxed/peaceful) because getting the emotional feel wrong is the most noticeable kind of bad recommendation. Genre is the next strongest signal (3 pts for an exact match). The five continuous features each contribute a partial score based on proximity: `weight × (1 - |reference_value - candidate_value|)`, with energy weighted at 3 pts, valence at 2 pts, tempo at 1 pt, danceability at 1 pt, and acousticness at 0.5 pts. A perfect match on every attribute would total 15.5 pts. Every song in the catalogue is scored this way and the top k by total score are returned as recommendations.

This design has a few potential biases worth knowing about. Because mood and genre together account for 8 out of 15.5 possible points, songs that share both labels with the reference will almost always outrank songs that are a closer numerical match but belong to a different genre or mood. The mood cluster groupings are also hand-coded, so moods left out of a cluster (such as "gritty" or "nostalgic") are treated as total mismatches even when they may feel adjacent to a listener. Finally, the catalogue of 20 songs skews toward certain genres and moods, so some combinations will rarely or never appear in the top results regardless of the weights used.

img: results.png

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

I tested several user profiles — a pop/happy/high-energy listener, a jazz fan whose genre matched nothing in the catalog, and an all-zero preference user — to see how the scoring held up in each case. I also tested edge cases like an extreme tempo gap (60 vs 400 BPM), which revealed that the formula produces a negative tempo contribution when the difference exceeds 200 BPM, and out-of-cluster moods like "gritty" and "nostalgic," which receive zero partial credit because they are not included in any mood cluster.

---

## Limitations and Risks

My recommender only works on a hand-picked catalog of 20 songs, so entire genres and moods a real user might love can simply be absent from the results. Because mood and genre together account for 8 out of 15.5 possible points, the system will almost always favor a song that shares labels with the user over one that is a numerically closer match but belongs to a different genre or mood — which could feel unfair or repetitive in practice.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this made it clear that a recommender is really just a set of rules about what "closeness" means — every weight I chose reflects a judgment call about which features matter most to a listener, and those calls are easy to get wrong. The mood-first design felt intuitive, but I realized it quietly buries songs that might actually sound great to the user just because they carry a different label.

I also learned that bias in a recommender does not have to be intentional to be real. My hand-coded mood clusters leave moods like "gritty" and "nostalgic" completely unconnected to anything, so users who prefer those feelings are silently penalized every time — not because I chose to exclude them, but because I never thought to include them in the first place.


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

