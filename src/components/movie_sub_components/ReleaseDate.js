import React from 'react';
import PropTypes from 'prop-types';

function ReleaseDate(props) {
  const { releaseDate } = props;

  if (releaseDate !== undefined) {
    return (
      <span className="movie-release-date-container">
        <span className="movie-release-date">
          {releaseDate}
        </span>
      </span>
    );
  }
  return <span className="movie-release-date-empty" />;
}

ReleaseDate.propTypes = {
  releaseDate: PropTypes.string.isRequired,
};

export default ReleaseDate;
