import React, { useState } from 'react';
import Movie from './Movie.js';



function MovieList(props) {

    const [displaySimilarMovies, setDisplaySimilarMovies] = useState(false)
    const [similarMovies, setSimilarMovies] = useState([])

    // authToken identifies a user
    const authToken = props.authToken

    // listOfMovies is a list of the following types of objects
    // {
    //      movie_title (string)
    //      movie_id (not for display)
    //      movieImage (a url string)
    //      rating (a integer from 0-10)
    //      status ("unwatched", "watching", "dropped", or "finished")
    //      comment (string)
    //      onWatchlist (boolean)
    // }
    const listOfMovies = props.listOfMovies

    // the data for each movie is passed to a respective Movie component
    // which will display the data
    function displayMovies() {
        const display = []
        for (var i = 0; i < listOfMovies.length; i++) {
            var movie = listOfMovies[i]
            display.push(<Movie
                authToken={authToken}
                title={movie['movie_title']}
                id={movie['movie_id']}
                image={movie['movie_image']}
                rating={movie['rating']}
                status={movie['status']}
                comment={movie['comment']}
                genres={movie['genres']}
                releaseDate={movie['release_date']}
                onWatchlist={movie['on_watchlist']}
                setSimilarMovies={setSimilarMovies}
                setDisplaySimilarMovies={setDisplaySimilarMovies}
                key={i}
            />)
        }
        return <div className="movie-list">{display}</div>
    }

    if (displaySimilarMovies) {
        return <MovieList listOfMovies={similarMovies} />
    } else {
        return <>
            <h1>{props.listName}</h1>
            {displayMovies()}
        </>

    }

}

export default MovieList;