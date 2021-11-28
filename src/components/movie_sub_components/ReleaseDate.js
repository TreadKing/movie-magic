import React, { useState } from 'react';

function ReleaseDate(props) {

    const releaseDate = props.releaseDate

    if (releaseDate !== undefined) {
        return <span className="movie-release-date-container">
            <span className="movie-release-date">
                {releaseDate}
            </span>
        </span>
    } else {
        return <span className="movie-release-date-empty"></span>
    }
}

export default ReleaseDate;