import React, { useState } from 'react';
import WatchlistPage from './WatchlistPage.js';
import MovieList from './MovieList.js';
import UpcomingMovies from './UpcomingMovies.js';
import Logout from './Logout.js';

import makeOptions from '../api.js';

// import movieSearchData from '../sample_data/movieSearchData.js';

function MovieSearch(props) {

    // Collect props (just need user information...their id and name)
    const authToken = props.authToken
    const username = props.username

    // This is the search input
    const [searchKey, setSearchKey] = useState('')

    // This is the result of the search
    // It is a list of movies
    const [searchResults, setSearchResults] = useState([])




    const [switchToWatchlist, setSwitchToWatchlist] = useState(false)
    const [switchToUpcoming, setSwitchToUpcoming] = useState(false)

    const [genre, setGenre] = useState(null)
    const [year, setYear] = useState(null)
    const [yearBeforeAfter, setYearBeforeAfter] = useState(true)
    const [rating, setRating] = useState(null)
    const [ratingBeforeAfter, setRatingBeforeAfter] = useState(true)

    function search() {

        // setSearchResults(movieSearchData)

        // ******* API DOCUMENTATION ******
        // /search
        // send:
        //     auth_token
        //     search_key
        //     genre (from list or null)
        //     year (number or null)
        //     year_before_after (boolean)
        //     rating (0-10 or null)
        //     rating_before_after (boolean)
        // receive:
        //      movie_id
        //      movie_title
        //      movie_image
        //      rating
        //      on_watchlist

        // ***** Production Code *******
        // setSearchKey('')

        const body = {
            'auth_token': authToken,
            'search_key': searchKey,
            'genre': genre,
            'year': year,
            'year_before_after': yearBeforeAfter,
            'rating': rating,
            'rating_before_after': ratingBeforeAfter
        }

        const options = makeOptions(body)

        fetch('/search', options)
            .then(response => response.json())
            .then(result => setSearchResults(result))
    }

    function genreOnChange(e) {
        setGenre(e.target.value)
    }

    function yearBeforeAfterOnChange(e) {
        setYearBeforeAfter(e.target.value)
    }

    function yearOnChange(e) {
        if (e.target.value === "") {
            setYear(null)
        } else {
            setYear(e.target.value)
        }

    }

    function ratingBeforeAfterOnChange(e) {
        setRatingBeforeAfter(e.target.value)
    }

    function ratingOnChange(e) {
        setRating(e.target.value)
    }

    function updateSearchKey(e) {
        setSearchKey(e.target.value)
    }

    if (switchToWatchlist) {
        return <WatchlistPage authToken={authToken} />
    } else if (switchToUpcoming) {
        return <UpcomingMovies authToken={authToken} />
    } else {
        return <>
            <span className="menu">
                <Logout></Logout>
                <span className="watchlist-button-container">
                    <button onClick={() => setSwitchToWatchlist(true)}
                        className="watchlist-button">
                        Watchlist
                </button>
                </span>
                <span className="upcoming-movies-button-container">
                    <button onClick={() => setSwitchToUpcoming(true)}
                        className="upcoming-movies-button">
                        Upcoming
                </button>
                </span>
            </span>
            <span className="search-form-container">
                <span className="search-input-container">
                    <input placeholder="Enter an actor's name"
                        className="search-input"
                        type="text"
                        value={searchKey}
                        onChange={updateSearchKey} />
                </span>
                <button className="search-button" onClick={search}>Search</button>
                <p className="select-genre-container">
                    <span className="select-genre-label">Genre</span>
                    <select className="select-genre" onChange={genreOnChange}>
                        <option value={null}></option>
                        <option value="Action">Action</option>
                        <option value="Adventure">Adventure</option>
                        <option value="Animation">Animation</option>
                        <option value="Comedy">Comedy</option>
                        <option value="Crime">Crime</option>
                        <option value="Documentary">Documentary</option>
                        <option value="Drama">Drama</option>
                        <option value="Family">Family</option>
                        <option value="Fantasy">Fantasy</option>
                        <option value="History">History</option>
                        <option value="Horror">Horror</option>
                        <option value="Music">Music</option>
                        <option value="Mystery">Mystery</option>
                        <option value="Romance">Romance</option>
                        <option value="Science Fiction">Science Fiction</option>
                        <option value="TV Movie">TV Movie</option>
                        <option value="Thriller">Thriller</option>
                        <option value="War">War</option>
                        <option value="Western">Western</option>
                    </select>
                </p>
                <p className="input-year-container-2">
                    <span className="input-year-label-2">Year</span>
                    <select className="year-before-after-input-2" onChange={yearBeforeAfterOnChange}>
                        <option value={true}>before</option>
                        <option value={false}>after</option>
                    </select>
                    <input className="year-input-2" type="number" onChange={yearOnChange} />
                </p>
                <p className="rating-container">
                    <span className="rating-label">Rating</span>
                    <select className="rating-less-greater-input" onChange={ratingBeforeAfterOnChange}>
                        <option value={true}>less than</option>
                        <option value={false}>greater than</option>
                    </select>
                    <select className="rating-input" onChange={ratingOnChange}>
                        <option value={null}></option>
                        <option value={0}>0</option>
                        <option value={1}>1</option>
                        <option value={2}>2</option>
                        <option value={3}>3</option>
                        <option value={4}>4</option>
                        <option value={5}>5</option>
                        <option value={6}>6</option>
                        <option value={7}>7</option>
                        <option value={8}>8</option>
                        <option value={9}>9</option>
                        <option value={10}>10</option>
                    </select>
                </p>
            </span>

            <MovieList
                authToken={authToken}
                listOfMovies={searchResults}
            />
        </>
    }
}

export default MovieSearch;