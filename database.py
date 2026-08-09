import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            album_id TEXT,
            name TEXT,
            artist TEXT,
            art TEXT,
            release_date TEXT,
            rating REAL,
            review TEXT,
            color TEXT,
            review_date TEXT
            )""")

    conn.commit()
    conn.close()

def save_review(album_id, name, artist, art, release_date, rating, review, color):
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    review_date = datetime.now().isoformat()
    cursor.execute("""
    INSERT INTO reviews
    (album_id, name, artist, art, release_date, rating, review, color, review_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        album_id,
        name,
        artist,
        art,
        release_date,
        rating,
        review,
        color,
        review_date
    ))

    conn.commit()
    conn.close()

def get_reviews(album_id):
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT rating, review, color 
        FROM reviews 
        WHERE album_id = ?
    """, (album_id,))
    reviews = cursor.fetchall()
    conn.close()
    return reviews

def get_all_reviews(sort):
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    sort_options = {
        'release_desc': 'release_date DESC',
        'release_asc': 'release_date ASC',
        'rating_desc': 'rating DESC',
        'rating_asc': 'rating ASC',
        'review_asc': 'review_date ASC',
        'review_desc': 'review_date DESC',
        'name_asc': 'name ASC',
        'name_desc': 'name DESC'
    }

    order_by = sort_options.get(sort, 'release_date DESC')

    cursor.execute(f"""
        SELECT album_id, name, artist, art, release_date, rating, review
        FROM reviews
        ORDER BY {order_by}
    """)

    reviews = cursor.fetchall()

    conn.close()

    return reviews

def has_reviews(album_id):
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id 
        FROM reviews 
        WHERE album_id = ?
    """, (album_id,))
    review = cursor.fetchone()
    conn.close()
    return review is not None

def review_exists(album_id):
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM reviews WHERE album_id = ? LIMIT 1",
        (album_id,)
    )

    exists = cursor.fetchone() is not None

    conn.close()

    return exists

def get_ratings_for_albums(album_ids):
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    placeholders = ",".join("?" for _ in album_ids)

    if not album_ids:
        conn.close()
        return {}

    cursor.execute(f"""
        SELECT album_id, rating
        FROM reviews
        WHERE album_id IN ({placeholders})
    """, album_ids)

    ratings = cursor.fetchall()
    conn.close()

    return dict(ratings)


if __name__ == "__main__":
    init_db()
