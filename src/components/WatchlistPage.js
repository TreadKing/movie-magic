import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import MovieSearch from './MovieSearch';
import MovieList from './MovieList';
import UpcomingMovies from './UpcomingMovies';
import makeOptions from '../api';
import Logout from './Logout';

function WatchlistPage(props) {
  const [watchlist, setWatchlist] = useState([]);
  // const [similarMovies, setSimilarMovies] = useState([])
  const [switchToSearch, setSwitchToSearch] = useState(false);

  const [switchToUpcoming, setSwitchToUpcoming] = useState(false);

  const { authToken } = props;

  // eslint-disable-next-line no-use-before-define
  useEffect(getWatchlist, []);

  function getWatchlist() {
    // setWatchlist(watchlistData)

    const body = { auth_token: authToken };

    const options = makeOptions(body);
    fetch('/getWatchList', options)
      .then((response) => response.json())
      .then((searchResult) => setWatchlist(searchResult));
  }

  if (switchToSearch) {
    return <MovieSearch authToken={authToken} />;
  } if (switchToUpcoming) {
    return <UpcomingMovies authToken={authToken} />;
  }
  return (
    <>

      <span className="menu">
        <Logout />
        <span className="switch-search-button-container">
          <button
            className="switch-search-button"
            onClick={() => setSwitchToSearch(true)}
            type="button"
          >
            Search
          </button>
        </span>
        <span className="upcoming-movies-button-container">
          <button
            onClick={() => setSwitchToUpcoming(true)}
            className="upcoming-movies-button"
            type="button"
          >
            Upcoming
          </button>
        </span>
      </span>
      <MovieList
        listName="Your Watchlist"
        authToken={authToken}
        listOfMovies={watchlist}
      />
    </>
  );
}

WatchlistPage.propTypes = {
  authToken: PropTypes.string.isRequired,
};

export default WatchlistPage;
