import React, { useState } from 'react';
import makeOptions from '../../api.js';

function WatchlistStatus(props) {
    const movieId = props.movieId
    const authToken = props.authToken
    const [status, setStatus] = useState(props.status)

    function addToWatchlist(e) {

        setStatus(e.target.value)
        const authToken = props.authToken
        const id = props.id
        const title = props.title
        const image = props.image
        const rating = props.rating
        const status = props.status

        // ******* API DOCUMENTATION ******
        // /addToWatchList
        // send:
        //      auth_token
        //      status (unwatched, watching, dropped, finished)
        //      movie_id
        // receive:
        //      message ("add successful" or "movie already on watchlist")

        const body = {
            'auth_token': authToken,
            'movie_id': id,
            'movie_title': title,
            'movie_image': image,
            'movie_rating': rating,
            'status': 'unwatched'
        }

        const options = makeOptions(body)
        fetch('/addToWatchList', options)
            .then(response => response.json())
            .then(jsonData => setDeleteMessage(jsonData['message']))

        setOnWatchlist(true)
    }

    if (status === undefined) {
        return <span className="empty-watchlist-status"></span>
    } else {
        return <select onChange={addToWatchlist} value={status}>
            <option value="unwatched">Unwatched</option>
            <option value="watching">Watching</option>
            <option value="finished">Finished</option>
            <option value="dropped">Drop</option>
        </select>
    }
}

export default WatchlistStatus;