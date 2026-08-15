from flask import Flask, session, render_template, request, url_for, redirect
from spotify_api import get_album, search_albums
from image_colors import get_dom_color
from database import get_review_years, get_rating_counts, format_release_date, days_ago, get_all_reviews, save_review, get_reviews, get_recent_reviews, review_exists, get_ratings_for_albums, add_to_queue, remove_from_queue, is_in_queue, get_queue, get_random_queue_album
import sqlite3

def star_rating(rating):
    rating = float(rating)
    full_stars = int(rating)
    half_star = rating - full_stars >= 0.5

    stars = "\u2605" * full_stars

    if half_star:
        stars += "½"

    return stars

app = Flask(__name__)
app.secret_key = "Key_Secret812"

app.jinja_env.globals.update(star_rating=star_rating)

# Home page route
@app.route('/')
def home():
    recent_reviews = get_recent_reviews()

    return render_template('index.html', recent_reviews=recent_reviews, days_ago=days_ago, format_release_date=format_release_date)

# All rankings page route
@app.route('/all_rankings')
def all_rankings():
    sort = request.args.get('sort')
    year = request.args.get('year')

    if sort:
        session['sort'] = sort
    else:
        sort = session.get('sort', 'release_desc')

    reviews = get_all_reviews(sort, year)
    rating_counts = get_rating_counts(year)
    years = get_review_years()

    return render_template('all_rankings.html', albums=reviews, current_sort=sort, rating_counts=rating_counts, years=years)

# Album ranking form page route
@app.route('/album/<album_id>', methods=["GET", "POST"])
def album_review(album_id):
    if review_exists(album_id):
        return redirect(url_for('ranking', album_id=album_id))

    spotify_data = get_album(album_id)
    reviews = get_reviews(album_id)
    in_queue = is_in_queue(album_id)

    color = get_dom_color(spotify_data['art'])
    color = f"rgb{color}"

    if request.method == "POST":
        rating = float(request.form.get("rating"))
        review = request.form.get("review")

        save_review(album_id, spotify_data["name"], spotify_data["artist"], spotify_data["art"], spotify_data["release_date"], rating, review, color)

        return redirect(url_for('ranking', album_id=album_id))
    
    return render_template('ranking_form.html', spotify=spotify_data, color=color, reviews=reviews, in_queue=in_queue, format_release_date=format_release_date)

# Personal ranking page route
@app.route('/ranking/<album_id>')
def ranking(album_id):
    spotify_data = get_album(album_id)
    reviews = get_reviews(album_id)
    in_queue = is_in_queue(album_id)

    color = reviews[0][2]

    return render_template('ranking.html', spotify=spotify_data, reviews=reviews, color=color,in_queue=in_queue, format_release_date=format_release_date)

# Search page route
@app.route('/search')
def search():
    query = request.args.get("query", "").strip()

    albums = []
    ratings = {}

    if query:
        albums = search_albums(query)

        album_ids = [album["id"] for album in albums]

        ratings = get_ratings_for_albums(album_ids)

    return render_template(
        'search.html', albums=albums, query=query, ratings=ratings, format_release_date=format_release_date)

# Queue page route
@app.route('/queue')
def queue():
    albums = get_queue()
    reviews = get_all_reviews('release_desc')

    reviewed_album_ids = {review[0] for review in reviews}

    return render_template(
        'queue.html',
        albums=albums,
        reviewed_album_ids=reviewed_album_ids
    )

# Toggle queue route
@app.route('/toggle_queue/<album_id>')
def toggle_queue(album_id):
    spotify_data = get_album(album_id)

    if is_in_queue(album_id):
        remove_from_queue(album_id)
    else:
        add_to_queue(
            album_id,
            spotify_data["name"],
            spotify_data["artist"],
            spotify_data["art"],
            spotify_data["release_date"]
        )

    return redirect(request.referrer or url_for('queue'))

# Pick a random album from queue route
@app.route('/random_queue')
def random_queue():
    album = get_random_queue_album()

    if not album:
        return redirect(url_for('queue'))

    album_id = album[0]

    if review_exists(album_id):
        return redirect(url_for('ranking', album_id=album_id))
    else:
        return redirect(url_for('album_review', album_id=album_id))

# Edit review route
@app.route('/edit_review/<album_id>', methods=["GET", "Post"])
def edit_review(album_id):
    spotify_data = get_album(album_id)
    reviews = get_reviews(album_id)

    if request.method == "POST":
        rating = float(request.form.get("rating"))
        review = request.form.get("review")

        conn = sqlite3.connect('reviews.db')
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE reviews
            SET rating = ?, review = ?
            WHERE album_id = ?
        """, (rating, review, album_id))

        conn.commit()
        conn.close()

        return redirect(url_for('ranking', album_id=album_id))

    color = reviews[0][2]

    return render_template('ranking_form.html', spotify=spotify_data, color=color, reviews=reviews, editing=True, format_release_date=format_release_date)

# Delete review route
@app.route('/delete_review/<album_id>')
def delete_review(album_id):
    print("Delete route hit:", album_id)
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM reviews WHERE album_id = ?",
        (album_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('all_rankings'))

if __name__ == '__main__':
    app.run(debug=True)