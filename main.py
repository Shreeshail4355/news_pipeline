from app.scraper import getAllNewsInfo
from app.db import get_connection, init_db, insert_articles, get_latest_articles
import yaml


def load_config(path='config.yml'):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def main():
    config = load_config('config.yml')
    websites = config['websites']
    all_articles = getAllNewsInfo(websites)
    print(config)

    try:
        conn = get_connection()
    except Exception as e:
        print(f"Failed to connect to DB: {e}")
        raise

    init_db(conn)
    insert_articles(conn, all_articles)

    latest = get_latest_articles(conn)

    print("Top 5 Latest Articles:")
    for i, (title, url, published, source) in enumerate(latest, 1):
        print(f"{i}. [{source}] {title}\n   {url}\n   Published: {published}\n")

if __name__ == "__main__":
    main()
