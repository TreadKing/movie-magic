import React, { useState } from 'react';
import MovieSearch from './MovieSearch.js';
import { getAuth, signInWithPopup, GoogleAuthProvider } from "firebase/auth";
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

// console.log(firebaseConfig)

// const app = initializeApp(firebaseConfig);
// const db = getFirestore(app);

firebase.initializeApp(firebaseConfig);





function Login() {

    const [switchToSearch, setSwitchToSearch] = useState(false)

    function doLogin() {

        const provider = new GoogleAuthProvider();
        const auth = getAuth();

        signInWithPopup(auth, provider)
            .then((result) => {
                // This gives you a Google Access Token. You can use it to access the Google API.
                const credential = GoogleAuthProvider.credentialFromResult(result);
                const token = credential.accessToken;
                console.log(token)
                // The signed-in user info.
                const user = result.user;
                console.log(user)
                console.log(user.accessToken)

                const options = {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 'access_token': user.accessToken})
                }

                fetch('/login', options).then(() => {
                    sessionStorage.setItem('accessToken', user.accessToken)
                    // setSwitchToSearch(true)

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
    }

    if (switchToSearch) {
        return <MovieSearch></MovieSearch>
    } else {
        return <button onClick={doLogin}>Login</button>
    }

}

export default Login;