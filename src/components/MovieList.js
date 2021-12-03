import React, { useState } from 'react';
import PropTypes from 'prop-types';
import Movie from './Movie';

function MovieList(props) {
  const [displaySimilarMovies, setDisplaySimilarMovies] = useState(false);
  const [similarMovies, setSimilarMovies] = useState([]);

  const { listName } = props;

  // authToken identifies a user
  const { authToken } = props;

  // listOfMovies is a list of the following types of objects
  // {
  //      movie_title (string)
  //      movie_id (not for display)
  //      movieImage (a url string)
  //      rating (a integer from 0-10)
  //      status ("unwatched", "watching", "dropped", or "finished")
  //      comment (string)
  //      onWatchlist (boolean)
  // }
  const { listOfMovies } = props;

  // the data for each movie is passed to a respective Movie component
  // which will display the data
  function displayMovies() {
    const display = [];
    for (let i = 0; i < listOfMovies.length; i += 1) {
      const movie = listOfMovies[i];
      display.push(<Movie
        authToken={authToken}
        title={movie.movie_title}
        id={movie.movie_id}
        image={movie.movie_image}
        rating={movie.rating}
        status={movie.status}
        comment={movie.comment}
        genres={movie.genres}
        releaseDate={movie.release_date}
        onWatchlist={movie.on_watchlist}
        setSimilarMovies={setSimilarMovies}
        setDisplaySimilarMovies={setDisplaySimilarMovies}
        key={i}
      />);
    }
    return <div className="movie-list">{display}</div>;
  }

  if (displaySimilarMovies) {
    return <MovieList listOfMovies={similarMovies} authToken={authToken} />;
  }
  return (
    <>
      <h1>{listName}</h1>
      {displayMovies()}
    </>
  );
}

MovieList.propTypes = {
  listOfMovies: PropTypes.any.isRequired,
  authToken: PropTypes.string.isRequired,
  listName: PropTypes.any,
};

export default MovieList;
