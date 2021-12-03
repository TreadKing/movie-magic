import React from 'react';
import PropTypes from 'prop-types';

function Genres(props) {
  const { genres } = props;

  if (genres !== undefined) {
    return (
      <span className="movie-genres-container">
        <span className="movie-genres">
          {genres.join(' ')}
        </span>
      </span>
    );
  }
  return <span className="movie-delete-button-empty" />;
}

Genres.propTypes = {
  genres: PropTypes.string.isRequired,
};

export default Genres;
