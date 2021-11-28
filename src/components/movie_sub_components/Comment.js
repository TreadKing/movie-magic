import React, { useState } from 'react';

function Comment(props) {

    const comment = props.comment

    if (comment !== undefined) {
        return <span className="movie-comment-container">
            <span className="movie-comment">
                {comment}
            </span>
        </span>
    } else {
        return <span className="movie-comment-empty"></span>
    }
}

export default Comment;