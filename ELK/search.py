# Script to connect ot elasticsearch and search for a query
import json
from pprint import pprint
import os
import time
import pandas as pd
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers

load_dotenv()


# Set the connection parameters
es_host = "https://localhost:9200"  # Adjust this if using a different host or port
es_user = "elastic"  # The Elasticsearch username
es_password = "changeme"  # The Elasticsearch password
ca_cert_path = "/tmp/ca.crt"  # Path to your CA certificate

index_name = "spotify"


class Search:
    def __init__(self):
        self.es = Elasticsearch(
            es_host,
            ca_certs=ca_cert_path,  # Path to the CA certificate
            basic_auth=(es_user, es_password),
        )
        client_info = self.es.info()
        print("Connected to Elasticsearch!")
        pprint(client_info.body)


def create_spotify_index(search: Search):
    # Defined schema for music data
    # Prepared mappings for Elasticsearch
    mapping = {
        "mappings": {
            "properties": {
                "id": {"type": "integer"},
                "track_id": {"type": "keyword"},
                "artists": {"type": "text"},
                "album_name": {"type": "text"},
                "track_name": {"type": "text"},
                "popularity": {"type": "integer"},
                "duration_ms": {"type": "integer"},
                "explicit": {"type": "boolean"},
                "danceability": {"type": "float"},
                "energy": {"type": "float"},
                "key": {"type": "integer"},
                "loudness": {"type": "float"},
                "mode": {"type": "integer"},
                "speechiness": {"type": "float"},
                "acousticness": {"type": "float"},
                "instrumentalness": {"type": "float"},
                "liveness": {"type": "float"},
                "valence": {"type": "float"},
                "tempo": {"type": "float"},
                "time_signature": {"type": "integer"},
                "track_genre": {"type": "keyword"},
                "mode": {"type": "keyword"},
            }
        }
    }

    if not search.es.indices.exists(index=index_name):
        response = search.es.indices.create(index=index_name, body=mapping)
        print(response)
    else:
        print("Index already exists!")


def generate_documents(df):
    for index, row in df.iterrows():
        doc = row.to_dict()
        yield {
            "_op_type": "update",
            "_index": index_name,
            "_id": doc.get("id"),
            "_source": {
                "doc": doc,
                "doc_as_upsert": True,  # upsert if document does not exist
            },
        }


def load_data(search: Search, data_path: str):
    try:
        df = pd.read_csv(data_path)
        # replace NaN with None
        df = df.where(pd.notnull(df), None)

        # add mode_value column - average of liveness, tempo and valence
        df["mode_value"] = df[["liveness", "valence"]].fillna(0).mean(axis=1)

        # Drop rows where 'mode_value' is NaN
        df = df.dropna(subset=["mode_value"])

        # Now you can safely apply pd.cut
        df["mode"] = pd.cut(
            df["mode_value"],
            bins=[0, 0.3, 0.5, 0.8, 1.0],
            labels=[0, 1, 2, 3],
            include_lowest=True,
        ).astype(int)

        # bulk upsert the data
        success, failed = helpers.bulk(
            search.es, generate_documents(df), raise_on_error=False
        )
        # Handle failed documents
        if failed:
            print("Failed documents:", failed)
        else:
            print(f"Data loaded successfully! {success} documents indexed.")
    except Exception as e:
        print(f"Error inserting documents: {e}")


if __name__ == "__main__":
    es = Search()
    data_path = "/home/alehak/Desktop/Projects/InfinityLabs/DataEngineeringCourse/ETL/data/songs.csv"

    create_spotify_index(search=es)

    load_data(search=es, data_path=data_path)
