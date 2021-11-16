import React, { useState } from 'react';
import MovieSearch from './MovieSearch.js';

function Login() {

    const switchToSearch = useState(false)

    function doLogin() {
        const options = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        }

        fetch('/api/login', options).then(() => switchToSearch(true))
    }

    if (switchToSearch) {
        return <MovieSearch></MovieSearch>
    } else {
        return <button onClick={doLogin}>Login</button>
    }

}

export default Login;