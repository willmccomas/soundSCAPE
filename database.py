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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            album_id TEXT UNIQUE,
            name TEXT,
            artist TEXT,
            art TEXT,
            release_date TEXT,
            added_date TEXT DEFAULT CURRENT_TIMESTAMP
            )""")

    conn.commit()
    conn.close()

# Reviews Database Functions
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
        'release_desc': 'release_date DESC, name ASC',
        'release_asc': 'release_date ASC, name ASC',
        'rating_desc': 'rating DESC, name ASC',
        'rating_asc': 'rating ASC, name ASC',
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

def get_recent_reviews():
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT album_id, name, artist, art, release_date, rating, review, review_date
        FROM reviews
        ORDER BY review_date DESC
        LIMIT 5
    """)

    reviews = cursor.fetchall()
    conn.close()

    return reviews

def days_ago(review_date):
    review_date = datetime.fromisoformat(review_date).date()
    today = datetime.today().date()

    days = (today - review_date).days

    if days == 0:
        return "Rated today"
    elif days == 1:
        return "Rated yesterday"
    else:
        return f"Rated {days} days ago"

def format_release_date(release_date):
    if len(release_date) == 4:
        return release_date

    date = datetime.strptime(release_date, "%Y-%m-%d")

    day = date.day

    if 11 <= day <= 13:
        suffix = "th"
    elif day % 10 == 1:
        suffix = "st"
    elif day % 10 == 2:
        suffix = "nd"
    elif day % 10 == 3:
        suffix = "rd"
    else:
        suffix = "th"

    return f"{date.strftime('%B')} {day}{suffix}, {date.year}"

# Queue Database Functions

def add_to_queue(album_id, name, artist, art, release_date):
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO queue
        (album_id, name, artist, art, release_date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        album_id,
        name,
        artist,
        art,
        release_date
    ))

    conn.commit()
    conn.close()

def remove_from_queue(album_id):
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM queue
        WHERE album_id = ?
    """, (album_id,))

    conn.commit()
    conn.close()

def is_in_queue(album_id):
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1
        FROM queue
        WHERE album_id = ?
    """, (album_id,))

    result = cursor.fetchone()

    conn.close()

    return result is not None

def get_queue():
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT album_id, name, artist, art, release_date, added_date
        FROM queue
        ORDER BY added_date DESC
    """)

    albums = cursor.fetchall()

    conn.close()

    return albums

def get_random_queue_album():
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT album_id, name, artist, art, release_date
        FROM queue
        ORDER BY RANDOM()
        LIMIT 1
    """)

    album = cursor.fetchone()

    conn.close()

    return album

if __name__ == "__main__":
    init_db()