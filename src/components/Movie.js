import React, { useState } from 'react';



function Movie(props) {
    const imageHeight = "200px"
    const authToken = props.authToken
    const movieTitle = props.movieTitle
    const movieId = props.movieId
    const movieImage = props.movieImage
    const rating = props.rating
    const comments = props.comments

    const [onWatchlist, setOnWatchlist] = useState(props.onWatchlist)

    function addMovie() {
        const options = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                'auth_token': authToken,
                'status': 'unwatched',
                'movid_id': movieId,
            })
        }

        fetch('/addToWatchList', options)

        setOnWatchlist(true)
    }

    function deleteMovie() {
        const options = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                'auth_token': authToken,
                'movie_id': movieId
            })
        }

        fetch('/deleteFromWatchList', options)

        setOnWatchlist(false)
    }

    return <>
        <div className="movie-container">
            <p className="movie-titles">{movieTitle}</p>
            <img className="movie-image" src={movieImage} height={imageHeight} />
            <div className="add-remove-container">
                <button className="add-movie-button"
                    onClick={addMovie}
                    disabled={onWatchlist}>
                    +
                    </button>
                <button className="remove-movie-button"
                    onClick={deleteMovie}
                    disabled={!onWatchlist}>
                    -
                    </button>
            </div>

        </div>
    </>
}

export default Movie;