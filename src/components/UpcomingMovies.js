import React, { useState, useEffect } from 'react'
import MovieList from './MovieList.js';
import MovieSearch from './MovieSearch.js';
import WatchlistPage from './WatchlistPage.js';
import Logout from './Logout.js';
import makeOptions from '../api.js';
// import upcomingData from '../sample_data/upcomingData.js';

function UpcomingMovies(props) {

    const authToken = props.authToken

    const [upcomingMovies, setUpcomingMovies] = useState([])
    const [switchToSearch, setSwitchToSearch] = useState(false)
    const [switchToWatchlist, setSwitchToWatchlist] = useState(false)

    useEffect(getUpcomingMovies, [])

    function getUpcomingMovies() {
        // remove for production code
        // setUpcomingMovies(upcomingData)

        // **** API Documentation ****
        // /getUpcoming
        // send:
        //      nothing
        // receive:
        //      movie_id
        //      movie_title
        //      ovie_image
        //      genres
        //      release_date (YYYY-MM-DD)
        //      on_watchlist (Boolean)
        const body = {
            'auth_token': authToken
        };
        const options = makeOptions(body);
        fetch('/getUpcoming', options)
            .then(response => response.json())
            .then(results => setUpcomingMovies(results));

    }

    if (switchToSearch) {
        return <MovieSearch authToken={authToken}></MovieSearch>
    } else if (switchToWatchlist) {
        return <WatchlistPage authToken={authToken} />
    } else {
        return <>

            <span className="menu">
                <Logout></Logout>
                <span className="switch-search-button-container">
                    <button className="switch-search-button"
                        onClick={() => setSwitchToSearch(true)}>
                        Search
                </button>
                </span>
                <span className="watchlist-button-container">
                    <button onClick={() => setSwitchToWatchlist(true)}
                        className="watchlist-button">
                        Watchlist
                    </button>
                </span>
            </span>
            <MovieList listOfMovies={upcomingMovies} authToken={authToken} listName="Upcoming Movies" />
        </>
    }

}

export default UpcomingMovies;