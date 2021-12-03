import React from 'react';
import PropTypes from 'prop-types';

function SimilarMoviesButton(props) {
  const { getSimilarMovies } = props;

  if (getSimilarMovies !== undefined) {
    return (
      <span className="similar-mobies-button-container">
        <button
          className="similar-mobies-button"
          onClick={getSimilarMovies}
          type="button"
        >
          Get Similar
        </button>
      </span>
    );
  }
  return <span className="similar-mobies-button-empty" />;
}

SimilarMoviesButton.propTypes = {
  getSimilarMovies: PropTypes.func.isRequired,
};

export default SimilarMoviesButton;
