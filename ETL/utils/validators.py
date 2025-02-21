import pandas as pd


def validate_songs_df(songs_df):
    # drop rows with missing critical values
    songs_df.dropna(
        subset=["popularity", "track_id", "artists", "track_name", "duration_ms"],
        inplace=True,
    )
    # fill nan values with 0
    songs_df.fillna(0, inplace=True)
    # drop duplicate rows
    songs_df.drop_duplicates(inplace=True)

    # Validate the range for numerical columns
    songs_df = songs_df[(songs_df["duration_ms"] > 0)]  # duration_ms must be positive
    songs_df = songs_df[(songs_df["danceability"].between(0, 1))]  # between 0 and 1
    songs_df = songs_df[(songs_df["energy"].between(0, 1))]
    songs_df = songs_df[
        (songs_df["loudness"].between(-80, 5))
    ]  # loudness should be in a reasonable range
    songs_df = songs_df[(songs_df["mode"].isin([1, 0]))]  # mode or 0 or 1
    songs_df = songs_df[(songs_df["speechiness"].between(0, 1))]  #
    songs_df = songs_df[(songs_df["acousticness"].between(0, 1))]  #
    songs_df = songs_df[(songs_df["instrumentalness"].between(0, 1))]  #
    songs_df = songs_df[(songs_df["liveness"].between(0, 1))]  #
    songs_df = songs_df[(songs_df["valence"].between(0, 1))]  #
    songs_df = songs_df[(songs_df["tempo"] > 0)]  # tempo must be positive

    return songs_df


def validate_users_df(users_df):
    # drop rows with missing critical values
    users_df.dropna(subset=["user_id", "user_name"], inplace=True)
    # fillna with 0
    users_df.fillna(0, inplace=True)
    # drop duplicates
    users_df.drop_duplicates(subset=["user_id"], inplace=True)

    return users_df


def validate_streams_df(streams_df, songs_df, users_df):
    # Ensure that track_id in stream_df exists in songs_df
    streams_df = streams_df[streams_df["track_id"].isin(songs_df["track_id"])]
    # Ensure that user_id in stream_df exists in users_df
    streams_df = streams_df[streams_df["user_id"].isin(users_df["user_id"])]

    return streams_df
