import React, { useState } from 'react';

function Genres(props) {

    const genres = props.genres

    if (genres !== undefined) {
        return <span className="movie-genres-container">
            <span className="movie-genres">
                {genres.join(' ')}
            </span>
        </span>
    } else {
        return <span className="movie-delete-button-empty"></span>
    }
}

export default Genres;