import React from 'react';
import PropTypes from 'prop-types';

function Rating(props) {
  const { rating } = props;

  if (rating !== undefined) {
    return (
      <span className="movie-rating-container">
        <span className="movie-rating-label">Rating (out of ten) </span>
        <span className="movie-rating">{rating}</span>
      </span>
    );
  }
  return <span className="movie-rating-empty" />;
}

Rating.propTypes = {
  rating: PropTypes.any,
};

export default Rating;
