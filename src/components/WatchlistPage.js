/* eslint-disable react-hooks/exhaustive-deps */
import React, { useState, useEffect } from 'react';
import MovieSearch from './MovieSearch.js';
import MovieList from './MovieList.js';
import UpcomingMovies from './UpcomingMovies.js';
import makeOptions from '../api.js';
import Logout from './Logout.js';

function WatchlistPage(props) {

    const [watchlist, setWatchlist] = useState([])
    // const [similarMovies, setSimilarMovies] = useState([])
    const [switchToSearch, setSwitchToSearch] = useState(false)

    const [switchToUpcoming, setSwitchToUpcoming] = useState(false)

    const authToken = props.authToken

    useEffect(getWatchlist, [])

    function getWatchlist() {

        // setWatchlist(watchlistData)

        const body = { 'auth_token': authToken }

        const options = makeOptions(body)

        fetch('/getWatchList', options)
            .then(response => response.json())
            .then(searchResult => setWatchlist(searchResult))
    }

    if (switchToSearch) {
        return <MovieSearch authToken={authToken}></MovieSearch>
    } else if (switchToUpcoming) {
        return <UpcomingMovies authToken={authToken} />
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
                <span className="upcoming-movies-button-container">
                    <button onClick={() => setSwitchToUpcoming(true)}
                        className="upcoming-movies-button">
                        Upcoming
                </button>
                </span>
            </span>
            <MovieList
                listName="Your Watchlist"
                authToken={authToken}
                listOfMovies={watchlist}
            />
        </>
    }

}

export default WatchlistPage;