import React from 'react';
import PropTypes from 'prop-types';

function Comment(props) {
  const { comment } = props;

  if (comment !== undefined) {
    return (
      <span className="movie-comment-container">
        <span className="movie-comment">
          {comment}
        </span>
      </span>
    );
  }
  return <span className="movie-comment-empty" />;
}

Comment.propTypes = {
  comment: PropTypes.string,
};

export default Comment;
