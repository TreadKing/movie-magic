import React from 'react';

function MovieTitle(props) {
    const title = props.title

    if (title !== undefined) {
        return <>
            <span className="movie-title-container">
                <span className="movie-title">
                    {title}
                </span>
            </span>
        </>
    } else {
        return <span className="movie-title-empty"></span>
    }

}

export default MovieTitle;