# Model Card - VibeFinder Music Recommender

## 1. Model Name
VibeFinder 1.0

## 2. Intended Use
This system suggests songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

## 3. How It Works
The system scores each song against a user profile using a weighted formula. Mood match earns up to 5 points, genre match earns 3 points, and continuous features like energy, valence, tempo, danceability, and acousticness contribute smaller weighted scores. The top-scoring songs are returned as recommendations.

## 4. Data
The catalog contains 5 sample songs covering pop, lofi, rock, and hiphop genres. Songs were manually created for testing purposes. The data mostly reflects mainstream Western music tastes.

## 5. Strengths
- Transparent scoring — every recommendation can be explained
- Works well when user genre and mood match songs in the catalog
- Fast and reproducible results

## 6. Limitations and Bias
- Only works on a tiny catalog of 5 songs
- Does not understand lyrics or audio features directly
- May over-favor mood matching since it carries the highest weight (5 pts)
- Users with niche tastes like jazz or classical will get poor results
- Assumes all users have the same taste structure

## 7. Evaluation
- 13/13 unit tests passed covering mood matching, genre scoring, edge cases, and missing keys
- 3/3 evaluation profiles passed: Happy Pop Fan, Chill Lofi Listener, Rock Enthusiast
- System struggled when user genre was not present in the catalog

## 8. Future Work
- Add support for a larger, real-world song catalog
- Balance diversity so recommendations are not always the closest match
- Add collaborative filtering to learn from multiple users

## 9. Personal Reflection
Building this system showed how easily bias enters a recommender through weight choices. Weighting mood at 5 points versus genre at 3 points means the system prioritizes emotional feel over musical style, which may not match everyone. I also learned that a simple scoring function can be surprisingly effective when features are well chosen. Human judgment is still needed to decide what good taste matching actually means.
