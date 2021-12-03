import React from 'react';
import PropTypes from 'prop-types';

function MovieImage(props) {
  const imageHeight = '200px';
  const { image } = props;

  if (image !== undefined) {
    return (
      <span className="movie-image-container">
        <img
          className="movie-image"
          src={image}
          height={imageHeight}
          alt="movie"
        />
      </span>
    );
  }
  return <span className="movie-image-empty" />;
}

MovieImage.propTypes = {
  image: PropTypes.string.isRequired,
};

export default MovieImage;
