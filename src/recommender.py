import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

MOOD_CLUSTERS = [
    {"chill", "relaxed", "peaceful", "laid-back"},
    {"happy", "euphoric", "energetic"},
    {"intense", "aggressive"},
    {"moody", "melancholic"},
    {"focused", "confident"},
]

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    score = 0.0
    reasons = []
    user_mood = user_prefs["mood"]
    song_mood = song["mood"]
    if user_mood == song_mood:
        score += 5.0
        reasons.append("mood match (+5.0)")
    else:
        for cluster in MOOD_CLUSTERS:
            if user_mood in cluster and song_mood in cluster:
                score += 2.5
                reasons.append(f"similar mood — {song_mood} ≈ {user_mood} (+2.5)")
                break
    if user_prefs["genre"] == song["genre"]:
        score += 3.0
        reasons.append("genre match (+3.0)")
    continuous = [
        ("energy",       3.0, user_prefs["energy"],       song["energy"],       1.0),
        ("valence",      2.0, user_prefs["valence"],       song["valence"],      1.0),
        ("tempo_bpm",    1.0, user_prefs["tempo_bpm"],     song["tempo_bpm"],    200.0),
        ("danceability", 1.0, user_prefs["danceability"],  song["danceability"], 1.0),
        ("acousticness", 0.5, user_prefs["acousticness"],  song["acousticness"], 1.0),
    ]
    for feature, weight, ref, candidate, scale in continuous:
        pts = weight * (1 - abs(ref - candidate) / scale)
        score += pts
        reasons.append(f"{feature} (+{pts:.2f})")
    return round(score, 4), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    scored = [
        (song, score, reasons)
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]

def load_songs(csv_path: str) -> List[Dict]:
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs

class Recommender:
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "valence": 0.5,
            "tempo_bpm": 120.0,
            "danceability": 0.5,
            "acousticness": 1.0 if user.likes_acoustic else 0.0,
        }
        scored = []
        for song in self.songs:
            song_dict = {
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "valence": song.valence,
                "tempo_bpm": song.tempo_bpm,
                "danceability": song.danceability,
                "acousticness": song.acousticness,
            }
            score, _ = score_song(user_prefs, song_dict)
            scored.append((song, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"matches your favorite genre ({song.genre})")
        if song.mood == user.favorite_mood:
            reasons.append(f"matches your preferred mood ({song.mood})")
        energy_diff = abs(song.energy - user.target_energy)
        if energy_diff < 0.2:
            reasons.append("energy level is close to your preference")
        if not reasons:
            reasons.append("best overall match based on your taste profile")
        return "Recommended because: " + ", ".join(reasons) + "."
