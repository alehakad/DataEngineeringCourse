import pandas as pd


def calculate_genres_age_distribution(users_df, songs_df, streams_total_df):
    """Calculate the distribution of genres listened to by different age groups"""
    age_bins = [0, 18, 25, 35, 45, 100]
    age_labels = ["Under 18", "18-25", "26-35", "36-45", "46+"]
    users_df["age_group"] = pd.cut(
        users_df["user_age"], bins=age_bins, labels=age_labels, right=False
    )

    merged_df = pd.merge(streams_total_df, users_df, on="user_id", how="inner")
    merged_df = pd.merge(merged_df, songs_df, on="track_id", how="inner")
    count_streams = (
        merged_df.groupby(["age_group", "track_genre"], observed=True)
        .size()
        .reset_index(name="stream_count")
    )

    return count_streams


def calculate_country_hours_distribution(songs_df, users_df, streams_total_df):
    """Calculate the distribution of hours listened by country"""
    merged_df = pd.merge(streams_total_df, users_df, on="user_id", how="inner")
    hours_country_df = (
        merged_df.groupby(by=[merged_df.listen_time.dt.hour, "user_country"])
        .size()
        .reset_index(name="stream_count")
    )
    return hours_country_df
