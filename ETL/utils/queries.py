CREATE_TABLES_QUERIES = {
    "age_genres_distribution": """
        CREATE TABLE IF NOT EXISTS age_genres_distribution (
            age_group VARCHAR,
            track_genre VARCHAR,
            stream_count INT
        )
    """,
    "country_hours_distribution": """
        CREATE TABLE IF NOT EXISTS country_hours_distribution (
            hour INT,
            user_country VARCHAR,
            stream_count INT
        )
    """,
}


INSERT_QUERIES = {
    "age_genres_distribution": """
        INSERT INTO age_genres_distribution (age_group, track_genre, stream_count)
        VALUES (%s, %s, %s)
    """,
    "country_hours_distribution": """
        INSERT INTO country_hours_distribution (hour, user_country, stream_count)
        VALUES (%s, %s, %s)
    """,
}