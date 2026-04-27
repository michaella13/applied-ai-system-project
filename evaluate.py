"""
Evaluation harness for the Music Recommender System.
Runs predefined user profiles and logs results.
"""
import sys
import logging
from src.recommender import Recommender, Song, UserProfile

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

def make_sample_songs():
    return [
        Song(1, "Sunflower", "Post Malone", "pop", "happy", 0.8, 120, 0.9, 0.8, 0.2),
        Song(2, "Chill Lofi", "Lo Artist", "lofi", "chill", 0.3, 75, 0.5, 0.4, 0.9),
        Song(3, "Thunder", "Imagine Dragons", "rock", "intense", 0.9, 160, 0.4, 0.6, 0.1),
        Song(4, "Blinding Lights", "The Weeknd", "pop", "energetic", 0.85, 171, 0.8, 0.75, 0.05),
        Song(5, "River", "Eminem", "hiphop", "moody", 0.7, 95, 0.3, 0.6, 0.1),
    ]

TEST_PROFILES = [
    {
        "name": "Happy Pop Fan",
        "user": UserProfile("pop", "happy", 0.8, False),
        "expect_genre": "pop",
        "expect_mood": "happy",
    },
    {
        "name": "Chill Lofi Listener",
        "user": UserProfile("lofi", "chill", 0.3, True),
        "expect_genre": "lofi",
        "expect_mood": "chill",
    },
    {
        "name": "Rock Enthusiast",
        "user": UserProfile("rock", "intense", 0.9, False),
        "expect_genre": "rock",
        "expect_mood": "intense",
    },
]

def run_evaluation():
    songs = make_sample_songs()
    rec = Recommender(songs)
    passed = 0

    log.info("=" * 50)
    log.info("MUSIC RECOMMENDER EVALUATION REPORT")
    log.info("=" * 50)

    for test in TEST_PROFILES:
        user = test["user"]
        results = rec.recommend(user, k=1)
        top = results[0]
        explanation = rec.explain_recommendation(user, top)

        genre_ok = top.genre == test["expect_genre"]
        mood_ok = top.mood == test["expect_mood"]
        success = genre_ok and mood_ok

        if success:
            passed += 1
            status = "PASS"
        else:
            status = "FAIL"

        log.info(f"\n[{status}] {test['name']}")
        log.info(f"  Top pick: {top.title} by {top.artist}")
        log.info(f"  Genre: {top.genre} (expected {test['expect_genre']}) — {'✓' if genre_ok else '✗'}")
        log.info(f"  Mood:  {top.mood} (expected {test['expect_mood']}) — {'✓' if mood_ok else '✗'}")
        log.info(f"  {explanation}")

    log.info("\n" + "=" * 50)
    log.info(f"RESULT: {passed}/{len(TEST_PROFILES)} tests passed")
    log.info("=" * 50)

if __name__ == "__main__":
    run_evaluation()
