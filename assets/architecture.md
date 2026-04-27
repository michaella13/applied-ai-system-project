# System Architecture

## VibeFinder - Music Recommender System

[User Input]
  - favorite_genre
  - favorite_mood
  - target_energy
  - likes_acoustic
        |
        v
[Recommender.recommend()]
  - converts UserProfile to scoring dict
        |
        v
[score_song()]
  - mood match: up to 5 pts
  - genre match: 3 pts
  - energy, valence, tempo, danceability, acousticness: weighted pts
        |
        v
[Top-K Songs Ranked by Score]
        |
        v
[explain_recommendation()]
  - generates human-readable explanation
        |
        v
[Output: Song title, artist, explanation]
        |
        v
[evaluate.py - Reliability Testing]
  - runs 3 predefined user profiles
  - checks top recommendation matches expected genre and mood
  - logs PASS/FAIL for each profile
  - prints summary: X/3 tests passed
