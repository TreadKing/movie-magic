import React, { useState } from 'react';
import MovieSearch from './MovieSearch.js';
import { getAuth, signInWithPopup, GoogleAuthProvider, setPersistence, browserSessionPersistence, onAuthStateChanged } from "firebase/auth";
import firebase from 'firebase/compat/app';
import {  } from 'firebase/compat/auth'
import { } from 'firebase/compat/firestore'
require('dotenv').config({path:__dirname+'/./../../.env'})

// var firebase = require('firebase');
var firebaseui = require('firebaseui');

const firebaseConfig = {
    apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
    authDomain: process.env.REACT_APP_FIREBASE_PROJECT_ID + '.firebaseapp.com',
    databaseURL: process.env.REACT_APP_FIREBASE_DATABASE_URL,
    projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
    storageBucket: process.env.REACT_APP_FIREBASE_PROJECT_ID + '.appspot.com',
    messagingSenderId: process.env.REACT_APP_FIREBASE_SENDER_ID,
    appId: process.env.REACT_APP_FIREBASE_APP_ID,
};

firebase.initializeApp(firebaseConfig);


function Login() {

    const [switchToSearch, setSwitchToSearch] = useState(false)
    const [accessToken, setAccessToken] = useState('')
    const auth = getAuth();

    onAuthStateChanged(auth, (user) => {
        if (user) {
            // User is signed in, see docs for a list of available properties
            // https://firebase.google.com/docs/reference/js/firebase.User
            setAccessToken(user.accessToken);
            
            setSwitchToSearch(true);
            // ...
        } else {
            // User is signed out
            // ...
            setSwitchToSearch(false);
        }
    });
    

    function doLogin() {
        
        const provider = new GoogleAuthProvider();
        
        setPersistence(auth, browserSessionPersistence)
            .then(() => {
                
                return signInWithPopup(auth, provider)
                    .then((result) => {
                        // The signed-in user info.
                        const user = result.user;
                        console.log(user)

                        const options = {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ 'access_token': user.accessToken})
                        }

                        fetch('/login', options).then(() => {
                            console.log('you logged in!')

                        }).catch((error) => {
                            console.log(error)
                        })

                    }).catch((error) => {
                        // Handle Errors here.
                        const errorCode = error.code;
                        const errorMessage = error.message;
                        console.log(errorCode);
                        console.log(errorMessage);
                    });
            }).catch((error) => {
                // Handle Errors here.
                const errorCode = error.code;
                const errorMessage = error.message;
            });
    }

    if (switchToSearch) {
        return <MovieSearch authToken={accessToken} ></MovieSearch>
    } else {
        return <button onClick={doLogin}>Login</button>
    }

}

export default Login;