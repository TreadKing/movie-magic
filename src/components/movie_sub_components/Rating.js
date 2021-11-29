import React, { useState } from 'react';

function Rating(props) {

    const rating = props.rating

    if (rating !== undefined) {
        return <span className="movie-rating-container">
            <span className="movie-rating-label">Rating (out of ten) </span>
            <span className="movie-rating">{rating}</span>
        </span >
    } else {
        return <span className="movie-rating-empty"></span>
    }
}

export default Rating;