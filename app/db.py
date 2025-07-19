from psycopg2.extras import execute_batch
import psycopg2
import os,time

def get_connection():
    for attempt in range(10):
        try:
            print(f"Attempt {attempt+1} to connect to DB...")
            return psycopg2.connect(
                dbname=os.environ["DB_NAME"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASSWORD"],
                host=os.environ["DB_HOST"],
                port=int(os.environ.get("DB_PORT", 5432)),
            )
        except psycopg2.OperationalError as e:
            print(f"Connection failed: {e}")
            time.sleep(2)
    raise Exception("Failed to connect to DB after multiple attempts.")

def init_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            article_id TEXT PRIMARY KEY,
            title TEXT,
            url TEXT UNIQUE,
            published TIMESTAMP,
            source TEXT
        );
        """)
        conn.commit()

def insert_articles(conn, articles):
    with conn.cursor() as cur:
        execute_batch(cur, """
            INSERT INTO articles (article_id, title, url, published, source)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (article_id) DO NOTHING;
        """, [
            (
                article.get('article_id'),
                article.get('title'),
                article.get('url'),
                article.get('published'),  
                article.get('source')
            )
            for article in articles
        ])
        conn.commit()

def get_latest_articles(conn, limit=5):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT title, url, published, source
            FROM articles
            where published is not NULL
            ORDER BY published DESC
            LIMIT %s;
        """, (limit,))
        return cur.fetchall()
