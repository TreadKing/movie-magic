import React from 'react';
import PropTypes from 'prop-types';
import MovieList from './MovieList';

function SimilarMovies(props) {
  const { listOfMovies } = props;
  const { title } = props;
  const { authToken } = props;

  return (
    <>
      <span
        className="similar-movies-title"
      >
        Similar movies for:
        {' '}
        {title}
      </span>
      <MovieList listOfMovies={listOfMovies} authToken={authToken} />
    </>
  );
}

SimilarMovies.propTypes = {
  listOfMovies: PropTypes.any.isRequired,
  title: PropTypes.string.isRequired,
  authToken: PropTypes.string.isRequired,
};

export default SimilarMovies;
