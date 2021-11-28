import React, { useState } from 'react';

function DeleteButton(props) {

    const _delete = props.delete
    const onWatchlist = props.onWatchlist

    if (_delete !== undefined) {
        return <span className="movie-delete-button-container">
            <button className="movie-delete-button"
                onClick={_delete}
                disabled={!onWatchlist}>
                -
            </button>
        </span>
    } else {
        return <span className="movie-delete-button-empty"></span>
    }
}

export default DeleteButton;