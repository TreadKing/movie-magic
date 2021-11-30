import React from 'react';

function AddButton(props) {

    const add = props.add
    const onWatchlist = props.onWatchlist

    if (add !== undefined) {
        return <span className="movie-add-button-container">
            <button className="movie-add-button"
                onClick={add}
                disabled={onWatchlist}>
                +
            </button>
        </span>
    } else {
        return <span className="movie-add-button-empty"></span>
    }
}

export default AddButton;