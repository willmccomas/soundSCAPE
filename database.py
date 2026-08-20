import sqlite3
from datetime import datetime


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

def init_db():
    """Create the database tables if they do not already exist."""

    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    # Reviews table
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
            review_date TEXT,
            apple_music_url TEXT
        )
    """)

    # Queue table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            album_id TEXT UNIQUE,
            name TEXT,
            artist TEXT,
            art TEXT,
            release_date TEXT,
            color TEXT,
            apple_music_url TEXT,
            added_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# REVIEW DATABASE FUNCTIONS
# =========================================================

def save_review(
    album_id,
    name,
    artist,
    art,
    release_date,
    rating,
    review,
    color,
    apple_music_url
):
    """Save a new album review to the database."""

    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    review_date = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO reviews
        (
            album_id,
            name,
            artist,
            art,
            release_date,
            rating,
            review,
            color,
            review_date,
            apple_music_url
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        album_id,
        name,
        artist,
        art,
        release_date,
        rating,
        review,
        color,
        review_date,
        apple_music_url
    ))

    conn.commit()
    conn.close()


def get_reviews(album_id):
    """Get the review information for a specific album."""

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


def get_all_reviews(sort, year=None):
    """Get all reviews using the selected sorting and year filter."""

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

    query = """
        SELECT album_id, name, artist, art, release_date, rating, review
        FROM reviews
    """

    params = []

    # Filter reviews by release year when one is selected.
    if year:
        query += " WHERE release_date LIKE ?"
        params.append(f"{year}%")

    query += f" ORDER BY {order_by}"

    cursor.execute(query, params)

    reviews = cursor.fetchall()

    conn.close()

    return reviews


def get_rating_counts(year=None):
    """Get the number of albums at each rating level."""

    conn = sqlite3.connect("reviews.db")
    cursor = conn.cursor()

    query = """
        SELECT rating, COUNT(*)
        FROM reviews
    """

    params = []

    # Filter ratings by release year when one is selected.
    if year:
        query += " WHERE release_date LIKE ?"
        params.append(f"{year}%")

    query += """
        GROUP BY rating
        ORDER BY rating
    """

    cursor.execute(query, params)

    results = cursor.fetchall()

    conn.close()

    counts = {rating: count for rating, count in results}

    # Make sure every possible rating is represented.
    for rating in [
        0.5, 1.0, 1.5, 2.0, 2.5,
        3.0, 3.5, 4.0, 4.5, 5.0
    ]:
        if rating not in counts:
            counts[rating] = 0

    return dict(sorted(counts.items()))


def get_review_years():
    """Get all unique album release years from reviewed albums."""

    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT SUBSTR(release_date, 1, 4)
        FROM reviews
        WHERE release_date IS NOT NULL
        ORDER BY SUBSTR(release_date, 1, 4) DESC
    """)

    years = [row[0] for row in cursor.fetchall()]

    conn.close()

    return years


def review_exists(album_id):
    """Check whether an album has an existing review."""

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
    """Get saved ratings for a list of album IDs."""

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
    """Get the five most recently reviewed albums."""

    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            album_id,
            name,
            artist,
            art,
            release_date,
            rating,
            review,
            review_date
        FROM reviews
        ORDER BY review_date DESC
        LIMIT 5
    """)

    reviews = cursor.fetchall()

    conn.close()

    return reviews


# =========================================================
# REVIEW DISPLAY HELPERS
# =========================================================

def days_ago(review_date):
    """Return a human-readable description of when a review was made."""

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
    """Convert an album release date into a readable format."""

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


# =========================================================
# REVIEW INFORMATION
# =========================================================

def get_review_color(album_id):
    """Get the saved color for a reviewed album."""

    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT color
        FROM reviews
        WHERE album_id = ?
    """, (album_id,))

    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None


def get_review_apple_music_url(album_id):
    """Get the Apple Music URL saved with a review."""

    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT apple_music_url
        FROM reviews
        WHERE album_id = ?
    """, (album_id,))

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return None


def get_saved_apple_music_url(album_id):
    """
    Get a saved Apple Music URL from either the reviews
    or queue table.
    """

    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    # Check reviewed albums first.
    cursor.execute("""
        SELECT apple_music_url
        FROM reviews
        WHERE album_id = ?
    """, (album_id,))

    result = cursor.fetchone()

    if result and result[0]:
        conn.close()
        return result[0]

    # If not reviewed, check the queue.
    cursor.execute("""
        SELECT apple_music_url
        FROM queue
        WHERE album_id = ?
    """, (album_id,))

    result = cursor.fetchone()

    conn.close()

    if result and result[0]:
        return result[0]

    return None


def save_apple_music_url(album_id, apple_music_url):
    """
    Save an Apple Music URL to both the reviews and
    queue tables when the album exists there.
    """

    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    # Update the reviewed album if it exists.
    cursor.execute("""
        UPDATE reviews
        SET apple_music_url = ?
        WHERE album_id = ?
    """, (apple_music_url, album_id))

    # Update the queued album if it exists.
    cursor.execute("""
        UPDATE queue
        SET apple_music_url = ?
        WHERE album_id = ?
    """, (apple_music_url, album_id))

    conn.commit()
    conn.close()


# =========================================================
# QUEUE DATABASE FUNCTIONS
# =========================================================

def add_to_queue(
    album_id,
    name,
    artist,
    art,
    release_date,
    color,
    apple_music_url
):
    """Add an album to the queue."""

    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO queue
        (
            album_id,
            name,
            artist,
            art,
            release_date,
            color,
            apple_music_url
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        album_id,
        name,
        artist,
        art,
        release_date,
        color,
        apple_music_url
    ))

    conn.commit()
    conn.close()


def remove_from_queue(album_id):
    """Remove an album from the queue."""

    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM queue
        WHERE album_id = ?
    """, (album_id,))

    conn.commit()
    conn.close()


def is_in_queue(album_id):
    """Check whether an album is currently in the queue."""

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
    """Get all queued albums, newest additions first."""

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
    """Return one randomly selected album from the queue."""

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


def get_queue_color(album_id):
    """Get the saved color for a queued album."""

    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT color
        FROM queue
        WHERE album_id = ?
    """, (album_id,))

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return None


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

if __name__ == "__main__":
    init_db()