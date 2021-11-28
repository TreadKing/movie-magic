import React, { useState } from 'react';

function WatchlistStatus(props) {
    const movieId = props.movieId
    const [status, setStatus] = useState(props.status)

    function addToWatchlist(e) {

        setStatus(e.target.value)

        // ******* API DOCUMENTATION ******
        // /addToWatchList
        // send:
        //      auth_token
        //      status (unwatched, watching, dropped, finished)
        //      movie_id
        // receive:
        //      message ("add successful" or "movie already on watchlist")

        // const body = {
        //     'auth_token': authToken,
        //     'status': { e.target.value },
        //     'movie_id': { movieId }
        // }

        // const options = makeOptions(body)
        // fetch('/addToWatchList', options)
        //     .then(response => response.json())
        //     .then(jsonData => setDeleteMessage(jsonData['message']))

        // setOnWatchlist(true)
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