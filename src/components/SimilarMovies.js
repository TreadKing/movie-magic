import React, { useState } from 'react';
import MovieList from './MovieList.js';
import Logout from './Logout.js';

function SimilarMovies(props) {
    const listOfMovies = props.listOfMovies
    const title = props.title
    const authToken = props.authToken

    return <>
        <span
            className="similar-movies-title"
        >
            Similar movies for: {title}
        </span>
        <MovieList listOfMovies={listOfMovies} authToken={authToken} />
    </>


}

export default SimilarMovies;