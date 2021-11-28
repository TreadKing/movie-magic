import React, { useState } from 'react';

function MovieImage(props) {
    const imageHeight = "200px"
    const image = props.image

    if (image !== undefined) {
        return <>
            <span className="movie-image-container">
                <img className="movie-image"
                    src={image}
                    height={imageHeight}
                />
            </span>
        </>
    } else {
        return <span className="movie-image-empty"></span>
    }
}

export default MovieImage;