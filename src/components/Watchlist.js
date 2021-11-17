import React, { useState, useEffect } from 'react';
import MovieSearch from './MovieSearch.js';
import Movie from './Movie.js';



function Watchlist(props) {

    const [watchlist, setWatchlist] = useState([])
    const [switchToSearch, setSwitchToSearch] = useState(false)
    const authToken = props.authToken

    useEffect(getWatchlist, [])

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

        fetch('/getWatchList', options)
            .then(response => response.json())
            .then(searchResult => setWatchlist(searchResult))
    }

    function displayMovies() {
        const display = []
        for (var i = 0; i < watchlist.length; i++) {
            var movie = watchlist[i]
            display.push(<Movie
                movieId={movie['movie_id']}
                movieTitle={movie['movie_title']}
                movieId={movie['movie_id']}
                movieImage={movie['movie_image']}
                rating={movie['rating']}
                status={movie['status']}
                comment={movie['comment']}
                key={i}
                onWatchlist={true}
                authToken={authToken}
            />
            )
        }
        return <div className="watchlist-display">{display}</div>
    }

    if (switchToSearch) {
        return <MovieSearch authToken={authToken}></MovieSearch>
    } else {
        return <>
        <button onClick={() => setSwitchToSearch(true)}>Search</button>
        {displayMovies()}
    </>
    }

}

export default Watchlist;