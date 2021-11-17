import React, { useState } from 'react';
import Movie from './Movie.js';
import Watchlist from './Watchlist.js';


function MovieSearch(props) {

    const authToken = props.authToken
    const username = props.username

    const [searchKey, setSearchKey] = useState('')
    const [searchResults, setSearchResults] = useState([])
    const [switchToWatchlist, setSwitchToWatchlist] = useState(false)

    function getMovies() {
        setSearchKey('')

        const options = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                'auth_token': authToken,
                'search_key': searchKey
            })
        }

        fetch('/search', options)
            .then(response => response.json())
            .then(result => setSearchResults(result))
    }

    function updateSearchKey(e) {
        setSearchKey(e.target.value)
    }

    function displayMovies() {
        const display = []
        for (var i = 0; i < searchResults.length; i++) {
            var movie = searchResults[i]
            display.push(<Movie
                authToken={authToken}
                movieTitle={movie['movie_title']}
                movieId={movie['movie_id']}
                movieImage={movie['movie_image']}
                rating={movie['rating']}
                status={movie['status']}
                comment={movie['comment']}
                authToken={authToken}
                key={i}
            />)
        }
        return <div className="movie-search-result">{display}</div>
    }

    if (switchToWatchlist) {
        return <Watchlist authToken={authToken}></Watchlist>
    } else {
        return <>
            <button onClick={() => setSwitchToWatchlist(true)}>Watchlist</button>
            <span className="search-input-container">
                <input placeholder="Enter an actor's name"
                    className="search-input"
                    type="text"
                    value={searchKey}
                    onChange={updateSearchKey} />
            </span>
            <button className="search-button" onClick={getMovies}>Search</button>
            {displayMovies()}
        </>
    }


}

export default MovieSearch;