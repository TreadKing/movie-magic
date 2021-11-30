import React from 'react';


function SimilarMoviesButton(props) {
    const getSimilarMovies = props.getSimilarMovies

    if (getSimilarMovies !== undefined) {
        return <span className="similar-mobies-button-container">
            <button className="similar-mobies-button"
                onClick={getSimilarMovies}>
                Get Similar
            </button>
        </span>
    } else {
        return <span className="similar-mobies-button-empty"></span>
    }
}

export default SimilarMoviesButton;