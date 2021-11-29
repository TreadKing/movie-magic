import React from 'react';

function Logout() {
    return <>
        <span className="watchlist-button-container">
            <button onClick={() => firebase.auth().signOut()}
                className="watchlist-button">
                Logout
            </button>
        </span>
    </>
}

export default Logout;