import React, { useState } from 'react';
import makeOptions from '../api.js';
import MovieTitle from './movie_sub_components/MovieTitle.js';
import MovieImage from './movie_sub_components/MovieImage.js';
import AddButton from './movie_sub_components/AddButton.js';
import DeleteButton from './movie_sub_components/DeleteButton.js';
import Rating from './movie_sub_components/Rating.js';
import Genres from './movie_sub_components/Genres.js';
import ReleaseDate from './movie_sub_components/ReleaseDate.js';
import Comment from './movie_sub_components/Comment.js';
import WatchlistStatus from './movie_sub_components/WatchlistStatus.js';
import SimilarMoviesButton from './movie_sub_components/SimilarMoviesButton.js';

// import similarMoviesData from '../sample_data/similarMoviesData.js';


function Movie(props) {

    const authToken = props.authToken

    const title = props.title
    const id = props.id
    const image = props.image
    const rating = props.rating
    const status = props.status
    const comment = props.comment
    const genres = props.genres
    const releaseDate = props.releaseDate
    const [onWatchlist, setOnWatchlist] = useState(props.onWatchlist)

    // message after trying to add a movie to watchlist
    const [addMessage, setAddMessage] = useState(null)
    // message after trying to delete a movie from the watchlist
    const [deleteMessage, setDeleteMessage] = useState(null)

    const [similarMovies, setSimilarMovies] = useState([])
    const [displaySimilarMovies, setDisplaySimilarMovies] = useState(false)


    function addToWatchlist() {

        // ******* API DOCUMENTATION ******
        // /addToWatchList
        // send:
        //      auth_token
        //      status (unwatched, watching, dropped, finished)
        //      movie_id
        // receive:
        //      message ("add successful" or "movie already on watchlist")

        const body = {'auth_token': authToken,
            'status': 'unwatched',
            'movie_id': id
            
        }

        const options = makeOptions(body)
        fetch('/addToWatchList', options)
            .then(response => response.json())
            .then(jsonData => setDeleteMessage(jsonData['message']))

        setOnWatchlist(true)
    }

    function deleteFromWatchlist() {

        // /deleteFromWatchlist
        // send:
        //      auth_token
        //      movie_id
        // receive:
        //      message (“delete successful” or “delete not successful”)

        const body = {
            'auth_token': authToken,
            'movie_id': id
        }

        const options = makeOptions(body)
        fetch('/deleteFromWatchList', options)
            .then(response => response.json())
            .then(jsonData => setDeleteMessage(jsonData['message']))

        setOnWatchlist(false)
    }

    function getSimilarMovies() {
        // props.setSimilarMovies(similarMoviesData)
        // props.setDisplaySimilarMovies(true)

        // *** API DOC ***
        // /getSimilar
        // send:
        //      movie_id
        // receive:
        //   	movie_id
        //      movie_title
        //      movie_image
        //      genres
        //      release_date
        //      rating
        //      on_watchlist (bool)

        // *** PRODUCTION CODE ***
        const body = {
            'movie_id': { id }
        }

        const options = makeOptions(body)

        fetch('/getSimilar', options)
            .then(response => response.json())
            .then(result => props.setSimilarMovies(result))
            .then(nothing => props.setDisplaySimilarMovies(true))
    }

    return <>
        <div className="movie-container">
            <MovieTitle title={title} />
            <MovieImage image={image} />
            <span className="add-and-delete-container">
                <AddButton add={addToWatchlist}
                    onWatchlist={onWatchlist}
                />
                <DeleteButton delete={deleteFromWatchlist}
                    onWatchlist={onWatchlist}
                />
            </span>
            <WatchlistStatus
                status={status}
                movieId={id}
            />
            <Rating rating={rating} />
            <Genres genres={genres} />
            {/* <WatchlistStatus status={status} /> */}
            <ReleaseDate date={releaseDate} />
            <Comment comment={comment} />
            <SimilarMoviesButton getSimilarMovies={getSimilarMovies} />
        </div>
    </>
}

export default Movie;