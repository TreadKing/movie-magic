import React, { useState } from 'react';



function Movie(props) {
    const imageHeight = "200px"
    const title = props.data.title
    const image = props.data.image
    const [onWatchlist, setOnWatchlist] = useState(props.data.onWatchlist)

    const [viewWatchlist, setViewWatchlist] = useState(false)

    function addMovie() {
        // const options = {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({
        //         'userId', userId,
        //         'title': title,
        //         'image': imgage,
        //         'onWatchlist': true
        //     })
        // }


        // fetch('/updateWatchlist', options)

        console.log('hello????')

        setOnWatchlist(true)
    }

    function removeMovie() {
        // const options = {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({
        //         'userId', userId,
        //         'title': title,
        //         'image': imgage,
        //         'onWatchlist': false
        //     })
        // }


        // fetch('/updateWatchlist', options)

        setOnWatchlist(false)
    }

    return <>
        <div className="movie-container">
            <p className="movie-titles">{title}</p>
            <img className="movie-image" src={image} height={imageHeight} />
            <div className="add-remove-container">
                <button className="add-movie-button"
                    onClick={addMovie}
                    disabled={onWatchlist}>
                    +
                    </button>
                <button className="remove-movie-button"
                    onClick={removeMovie}
                    disabled={!onWatchlist}>
                    -
                    </button>
            </div>

        </div>
    </>
}

export default Movie;