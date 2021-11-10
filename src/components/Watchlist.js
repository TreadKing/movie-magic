import React, { useState, useEffect } from 'react';
import Movie from './Movie.js';
import data1 from '../sample_data/01.js';
import data4 from '../sample_data/04.js';



function MovieSearch() {

    const [watchlistMovies, setWatchlistMovies] = useState([])

    useEffect(getMovies)

    function getMovies() {
        setWatchlistMovies([data1, data4])
        setTextInput('')

        // const options = {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({ 'userId': textInput, 'userId': userId })
        // }

        // fetch('/getWatchlist', options)
        //     .then(response => response.json())
        //     .then(searchResult => setWatchlistMovies(searchResult))
    }

    function displayMovies() {
        const display = []
        for (var i = 0; i < watchlistMovies.length; i++) {
            display.push(<Movie data={watchlistMovies[i]} key={i} />)
        }
        return <div className="wathlist-display">{display}</div>
    }

    return <>
        {displayMovies()}
    </>
}

export default MovieSearch;