import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import MovieList from './MovieList';
import MovieSearch from './MovieSearch';
import WatchlistPage from './WatchlistPage';
import Logout from './Logout';
import makeOptions from '../api';
// import upcomingData from '../sample_data/upcomingData';

function UpcomingMovies(props) {
  const { authToken } = props;

  const [upcomingMovies, setUpcomingMovies] = useState([]);
  const [switchToSearch, setSwitchToSearch] = useState(false);
  const [switchToWatchlist, setSwitchToWatchlist] = useState(false);

  // eslint-disable-next-line no-use-before-define
  useEffect(getUpcomingMovies, []);

  function getUpcomingMovies() {
    // remove for production code
    // setUpcomingMovies(upcomingData)

    // **** API Documentation ****
    // /getUpcoming
    // send:
    //      nothing
    // receive:
    //      movie_id
    //      movie_title
    //      ovie_image
    //      genres
    //      release_date (YYYY-MM-DD)
    //      on_watchlist (Boolean)
    const body = {
      auth_token: authToken,
    };
    const options = makeOptions(body);
    fetch('/getUpcoming', options)
      .then((response) => response.json())
      .then((results) => setUpcomingMovies(results));
  }

  if (switchToSearch) {
    return <MovieSearch authToken={authToken} />;
  } if (switchToWatchlist) {
    return <WatchlistPage authToken={authToken} />;
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
        <span className="watchlist-button-container">
          <button
            onClick={() => setSwitchToWatchlist(true)}
            className="watchlist-button"
            type="button"
          >
            Watchlist
          </button>
        </span>
      </span>
      <MovieList listOfMovies={upcomingMovies} authToken={authToken} listName="Upcoming Movies" />
    </>
  );
}

UpcomingMovies.propTypes = {
  authToken: PropTypes.string.isRequired,
};

export default UpcomingMovies;
