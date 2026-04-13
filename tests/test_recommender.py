import pytest
from src.recommender import Song, UserProfile, Recommender, score_song, recommend_songs


# ── helpers ───────────────────────────────────────────────────────────────────

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


def song_dict(**overrides) -> dict:
    """Return a baseline song dict with optional field overrides."""
    base = {
        "id": 99,
        "title": "Adversarial Track",
        "artist": "Edge Artist",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.5,
        "tempo_bpm": 120,
        "valence": 0.5,
        "danceability": 0.5,
        "acousticness": 0.5,
    }
    base.update(overrides)
    return base


def user_prefs(**overrides) -> dict:
    """Return a baseline user_prefs dict with optional field overrides."""
    base = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "valence": 0.8,
        "tempo_bpm": 120,
        "danceability": 0.8,
        "acousticness": 0.2,
    }
    base.update(overrides)
    return base


# ── existing tests (unchanged) ────────────────────────────────────────────────

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
    # Starter expectation: the pop, happy, high energy song should score higher
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


# ── adversarial / edge-case tests ─────────────────────────────────────────────
# NOTE: these tests target score_song() directly because Recommender.recommend()
# is currently a stub that bypasses the scoring logic entirely.


class TestOutOfClusterMood:
    """Moods absent from MOOD_CLUSTERS only score on exact string match."""

    def test_two_unrecognised_moods_get_zero_mood_points(self):
        # "gritty" and "nostalgic" are both absent from every cluster →
        # no exact match, no cluster overlap → 0 mood points
        prefs = user_prefs(mood="gritty")
        song = song_dict(mood="nostalgic")
        _, reasons = score_song(prefs, song)
        mood_reasons = [r for r in reasons if "mood" in r]
        assert mood_reasons == [], f"Expected 0 mood points, got: {mood_reasons}"

    def test_unrecognised_mood_exact_match_still_gets_full_points(self):
        # Same out-of-cluster mood on both sides → exact string match → 5.0 pts
        prefs = user_prefs(mood="gritty")
        song = song_dict(mood="gritty")
        _, reasons = score_song(prefs, song)
        assert any("mood match" in r for r in reasons), (
            "Exact mood match should award 5.0 pts even for out-of-cluster moods"
        )

    def test_in_cluster_user_vs_out_of_cluster_song_gets_no_partial_credit(self):
        # User wants "happy" (cluster 1); song is "gritty" (no cluster) →
        # no cluster overlap → 0 mood pts, even though they feel adjacent
        prefs = user_prefs(mood="happy")
        song = song_dict(mood="gritty")
        _, reasons = score_song(prefs, song)
        mood_reasons = [r for r in reasons if "mood" in r]
        assert mood_reasons == []


class TestGenreNotInCatalog:
    """A genre preference absent from all songs yields 0 genre points everywhere."""

    def test_unknown_genre_scores_zero_for_every_song(self):
        prefs = user_prefs(genre="jazz")
        songs = [
            song_dict(id=1, genre="pop"),
            song_dict(id=2, genre="rock"),
            song_dict(id=3, genre="lofi"),
        ]
        for s in songs:
            _, reasons = score_song(prefs, s)
            genre_reasons = [r for r in reasons if "genre" in r]
            assert genre_reasons == [], (
                f"Song genre '{s['genre']}' should not match user genre 'jazz'"
            )

    def test_unknown_genre_ranking_falls_back_to_numeric_features(self):
        # When no genre ever matches, the song closer in numeric features wins
        prefs = user_prefs(genre="jazz", energy=0.9, valence=0.9)
        high_match = song_dict(id=1, genre="pop", energy=0.9, valence=0.9)
        low_match  = song_dict(id=2, genre="pop", energy=0.1, valence=0.1)
        s_high, _ = score_song(prefs, high_match)
        s_low, _  = score_song(prefs, low_match)
        assert s_high > s_low, (
            "Numerically closer song should rank higher when no genre matches"
        )


class TestExtremeTempoNegativeContribution:
    """Tempo diff > 200 BPM makes the tempo term go negative."""

    def test_extreme_tempo_diff_produces_negative_tempo_pts(self):
        # user: 60 BPM, song: 400 BPM → diff 340 → 1.0*(1 - 340/200) = -0.70
        prefs = user_prefs(tempo_bpm=60)
        song = song_dict(tempo_bpm=400)
        _, reasons = score_song(prefs, song)

        tempo_reason = next(r for r in reasons if r.startswith("tempo_bpm"))
        # format: "tempo_bpm (+X.XX)"  — negative shows as "(+-0.70)"
        pts = float(tempo_reason.split("(+")[1].rstrip(")"))
        assert pts < 0, f"Expected negative tempo contribution, got {pts}"

    def test_extreme_tempo_lowers_overall_score_vs_close_tempo(self):
        prefs = user_prefs(tempo_bpm=60)
        normal_song  = song_dict(id=1, tempo_bpm=70)   # diff 10
        extreme_song = song_dict(id=2, tempo_bpm=400)  # diff 340
        s_normal,  _ = score_song(prefs, normal_song)
        s_extreme, _ = score_song(prefs, extreme_song)
        assert s_normal > s_extreme


class TestAllZeroContinuousPrefs:
    """User with all-zero numeric prefs should rank zero-feature songs highest."""

    def test_all_zero_prefs_ranks_minimal_song_above_maximal(self):
        prefs = user_prefs(
            energy=0.0, valence=0.0, tempo_bpm=0.0,
            danceability=0.0, acousticness=0.0,
        )
        minimal = song_dict(id=1, energy=0.0, valence=0.0, tempo_bpm=0.0,
                            danceability=0.0, acousticness=0.0)
        maximal = song_dict(id=2, energy=1.0, valence=1.0, tempo_bpm=200.0,
                            danceability=1.0, acousticness=1.0)
        s_min, _ = score_song(prefs, minimal)
        s_max, _ = score_song(prefs, maximal)
        assert s_min > s_max, (
            "Zero-feature song should score higher for an all-zero user"
        )


class TestMissingKey:
    """score_song() has no input validation — missing keys crash with KeyError.
    These tests document the current (unguarded) behaviour as known bugs."""

    def test_missing_energy_key_raises_key_error(self):
        prefs = user_prefs()
        del prefs["energy"]
        with pytest.raises(KeyError):
            score_song(prefs, song_dict())

    def test_missing_mood_key_raises_key_error(self):
        prefs = user_prefs()
        del prefs["mood"]
        with pytest.raises(KeyError):
            score_song(prefs, song_dict())

    def test_missing_genre_key_raises_key_error(self):
        prefs = user_prefs()
        del prefs["genre"]
        with pytest.raises(KeyError):
            score_song(prefs, song_dict())
