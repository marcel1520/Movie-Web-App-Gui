from flask import Flask, request, render_template, url_for, redirect
from data_manager import SQLiteDataManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

data_manager = SQLiteDataManager(app)


# helper function movie serialization
def serialize_movie():
    return {
        'title': request.form['title'],
        'release_year': request.form['release_year'],
        'genre': request.form['genre'],
        'director': request.form['director'],
        'rating': request.form['rating']
    }


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        db_users = data_manager.get_all_users()
        return render_template('users.html', users=db_users)

    elif request.method == 'POST':
        name = request.form['name']
        data_manager.add_user({'name': name})
        return redirect(url_for('users'))


@app.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
def user_movies(user_id):
    if request.method == 'POST':
        movie_data = serialize_movie()
        data_manager.add_movie(user_id, movie_data)
        return redirect(url_for('user_movies', user_id=user_id))

    user = data_manager.get_user(user_id)
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/edit', methods=['GET', 'POST'])
def edit_movie(user_id, movie_id):
    movie = data_manager.get_movie(user_id, movie_id)
    if request.method == 'POST':
        updated_data = serialize_movie()
        data_manager.update_movie(user_id, movie_id, updated_data)
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('edit_movie.html', movie=movie, user_id=user_id)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(user_id, movie_id)
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    data_manager.delete_user(user_id)
    return redirect(url_for('users'))


if __name__ == "__main__":
    app.run(debug=True)

