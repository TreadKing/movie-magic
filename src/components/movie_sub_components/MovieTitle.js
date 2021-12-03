import React from 'react';
import PropTypes from 'prop-types';

function MovieTitle(props) {
  const { title } = props;

  if (title !== undefined) {
    return (
      <span className="movie-title-container">
        <span className="movie-title">
          {title}
        </span>
      </span>
    );
  }
  return <span className="movie-title-empty" />;
}

MovieTitle.propTypes = {
  title: PropTypes.string.isRequired,
};

export default MovieTitle;
