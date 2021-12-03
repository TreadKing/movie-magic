import React, { useState } from 'react';
import PropTypes from 'prop-types';
import makeOptions from '../../api';

function WatchlistStatus(props) {
  // const movieId = props.movieId
  // const authToken = props.authToken

  // const [status, setStatus] = useState(props.status);
  const [{ status }, setStatus] = useState(props);

  function addToWatchlist(e) {
    setStatus(e.target.value);
    const { authToken } = props;
    const { id } = props;
    const { title } = props;
    const { image } = props;
    const { rating } = props;
    // const status = props.status

    // ******* API DOCUMENTATION ******
    // /addToWatchList
    // send:
    //      auth_token
    //      status (unwatched, watching, dropped, finished)
    //      movie_id
    // receive:
    //      message ("add successful" or "movie already on watchlist")

    const body = {
      auth_token: authToken,
      movie_id: id,
      movie_title: title,
      movie_image: image,
      rating,
      status: e.target.value,
    };

    const options = makeOptions(body);
    fetch('/addToWatchList', options)
      .then((response) => response.json());
    // .then(jsonData => setDeleteMessage(jsonData['message']))

    // setOnWatchlist(true)
  }

  if (status === undefined) {
    return <span className="empty-watchlist-status" />;
  }
  return (
    <select onChange={addToWatchlist} value={status}>
      <option value="unwatched">Unwatched</option>
      <option value="watching">Watching</option>
      <option value="finished">Finished</option>
      <option value="dropped">Drop</option>
    </select>
  );
}

WatchlistStatus.propTypes = {
  authToken: PropTypes.string.isRequired,
  id: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  image: PropTypes.string.isRequired,
  rating: PropTypes.string.isRequired,
};

export default WatchlistStatus;
