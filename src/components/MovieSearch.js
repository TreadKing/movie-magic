import React, { useState } from 'react';
import Movie from './Movie.js';
import data1 from '../sample_data/01.js';
import data2 from '../sample_data/02.js';
import data3 from '../sample_data/03.js';
import data4 from '../sample_data/04.js';
import data5 from '../sample_data/05.js';
import data6 from '../sample_data/06.js';
import data7 from '../sample_data/07.js';


function MovieSearch() {

    const [textInput, setTextInput] = useState('')
    const [moviesData, setMoviesData] = useState([])

    function getMovies() {
        setMoviesData([data1, data2, data3, data4, data5, data6, data7])
        setTextInput('')

        // const options = {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({ 'search_key': textInput, 'userId': userId })
        // }

        // fetch('/search', options)
        //     .then(response => response.json())
        //     .then(searchResult => setMoviesData(searchResult))
    }

    function updateTextInput(e) {
        setTextInput(e.target.value)
    }

    function displayMovies() {
        const display = []
        for (var i = 0; i < moviesData.length; i++) {
            display.push(<Movie data={moviesData[i]} key={i} />)
        }
        return <div className="movie-search-result">{display}</div>
    }

    return <>
        <span className="search-input-container">
            {/* <span className="search-input-label">Enter an actor's name</span> */}
            <input placeholder="Enter an actor's name"
                className="search-input"
                type="text"
                value={textInput}
                onChange={updateTextInput} />
        </span>
        <button className="search-button" onClick={getMovies}>Search</button>

        {displayMovies()}
    </>
}

export default MovieSearch;