import React from 'react';
import PropTypes from 'prop-types';

function AddButton(props) {
  const { add } = props;
  const { onWatchlist } = props;

  if (add !== undefined) {
    return (
      <span className="movie-add-button-container">
        <button
          className="movie-add-button"
          onClick={add}
          disabled={onWatchlist}
          type="button"
        >
          +
        </button>
      </span>
    );
  }
  return <span className="movie-add-button-empty" />;
}

AddButton.propTypes = {
  add: PropTypes.func.isRequired,
  onWatchlist: PropTypes.bool.isRequired,
};

export default AddButton;
