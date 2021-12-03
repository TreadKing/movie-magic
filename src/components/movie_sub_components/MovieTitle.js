import React from 'react';

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

MovieTitle.prototype = {
    
}

export default MovieTitle;
