import React from 'react';
import PropTypes from 'prop-types';

function DeleteButton(props) {
  const { deleteFromWatchlist } = props;
  const { onWatchlist } = props;

  if (deleteFromWatchlist !== undefined) {
    return (
      <span className="movie-delete-button-container">
        <button
          className="movie-delete-button"
          onClick={deleteFromWatchlist}
          disabled={!onWatchlist}
          type="button"
        >
          -
        </button>
      </span>
    );
  }
  return <span className="movie-delete-button-empty" />;
}

DeleteButton.propTypes = {
  deleteFromWatchlist: PropTypes.func.isRequired,
  onWatchlist: PropTypes.any.isRequired,
};

export default DeleteButton;
