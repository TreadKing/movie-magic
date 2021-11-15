import React, { useState, useEffect } from 'react';
import Movie from './Movie.js';



function MovieSearch() {


    const [watchlist, setWatchlist] = useState([])

    useEffect(getMovies)

    function getWatchlist() {

        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'auth_token': authToken
            })
        }

        fetch('/getWatchlist', options)
            .then(response => response.json())
            .then(searchResult => setWatchlistMovies(searchResult))
    }

    function displayMovies() {
        const display = []
        const movie
        for (var i = 0; i < watchlistMovies.length; i++) {
            movie = watchlistMovies[i]
            display.push(<Movie
                movieId={movie['movie_id']}
                movieTitle={movie['movie_title']}
                movieId={movie['movie_id']}
                movieImage={movie['movie_image']}
                rating={movie['rating']}
                status={movie['status']}
                comment={movie['comment']}
                key={i}
            />
            )
        }
        return <div className="watchlist-display">{display}</div>
    }

    return <>
        {displayMovies()}
    </>
}

export default MovieSearch;