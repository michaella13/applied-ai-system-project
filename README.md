# Music Recommender - Applied AI System

## Original Project
This project extends the Module 3 Music Recommender Simulation. The original system represented songs and user taste profiles as data and used a scoring rule to generate recommendations.

## Title and Summary
VibeFinder - An applied AI music recommendation system that scores and recommends songs based on a user's genre, mood, and energy preferences. The system includes full explanation of recommendations and an automated evaluation harness to test reliability.

## Architecture Overview
User Profile (genre, mood, energy, acoustic preference)
-> Recommender.recommend()
-> score_song() scores each song against user prefs
-> Top-K Songs returned with explanation
-> evaluate.py runs 3 predefined profiles and logs pass/fail

## Setup Instructions
1. Clone the repo: git clone https://github.com/michaella13/applied-ai-system-project.git
2. Install dependencies: pip install -r requirements.txt && pip install pytest
3. Run the recommender: python3 -m src.main
4. Run unit tests: python3 -m pytest tests/ -v
5. Run evaluation harness: python3 evaluate.py

## Sample Interactions
Input: User likes pop, happy mood, high energy (0.8)
Output: Sunflower by Post Malone - Recommended because: matches your favorite genre (pop), matches your preferred mood (happy), energy level is close to your preference.

Input: User likes lofi, chill mood, low energy (0.3)
Output: Chill Lofi by Lo Artist - Recommended because: matches your favorite genre (lofi), matches your preferred mood (chill), energy level is close to your preference.

Input: User likes rock, intense mood, high energy (0.9)
Output: Thunder by Imagine Dragons - Recommended because: matches your favorite genre (rock), matches your preferred mood (intense), energy level is close to your preference.

## Design Decisions
- Used a weighted scoring function combining mood (5 pts), genre (3 pts), and continuous features like energy and tempo.
- Mood clusters allow partial credit for similar moods (e.g. chill is similar to relaxed).
- evaluate.py was added as a reliability layer to automatically verify recommendations.

## Testing Summary
- 13/13 unit tests passed covering mood matching, genre scoring, and edge cases.
- 3/3 evaluation profiles passed (Happy Pop Fan, Chill Lofi Listener, Rock Enthusiast).
- The system struggled with songs whose genre is not in the catalog - falls back to numeric feature matching.

## Reflection
Building this system showed how recommenders reduce complex human taste into numbers. Small weight changes dramatically shift results, revealing how easily bias can enter. Human judgment is still needed to define what good taste matching means.
