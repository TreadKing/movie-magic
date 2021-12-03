import React from 'react';
import firebase from 'firebase/compat/app';

function Logout() {
  return (
    <span className="watchlist-button-container">
      <button
        onClick={function signOut() { firebase.auth().signOut(); }}
        className="watchlist-button"
        type="button"
      >
        Logout
      </button>
    </span>
  );
}

export default Logout;
