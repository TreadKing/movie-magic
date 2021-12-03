import React, { useState } from 'react';
import PropTypes from 'prop-types';
import makeOptions from '../api';
import MovieTitle from './movie_sub_components/MovieTitle';
import MovieImage from './movie_sub_components/MovieImage';
import AddButton from './movie_sub_components/AddButton';
import DeleteButton from './movie_sub_components/DeleteButton';
import Rating from './movie_sub_components/Rating';
import Genres from './movie_sub_components/Genres';
import ReleaseDate from './movie_sub_components/ReleaseDate';
import Comment from './movie_sub_components/Comment';
import WatchlistStatus from './movie_sub_components/WatchlistStatus';
import SimilarMoviesButton from './movie_sub_components/SimilarMoviesButton';

// import similarMoviesData from '../sample_data/similarMoviesData';

function Movie(props) {
  const { authToken } = props;

  const { title } = props;
  const { id } = props;
  const { image } = props;
  const { rating } = props;
  const { status } = props;
  const { comment } = props;
  const { genres } = props;
  const { releaseDate } = props;
  // eslint-disable-next-line react/destructuring-assignment
  const [onWatchlist, setOnWatchlist] = useState(props.onWatchlist);

  // message after trying to add a movie to watchlist
  // const [addMessage, setAddMessage] = useState(null)

  // message after trying to delete a movie from the watchlist
  // const [deleteMessage, setDeleteMessage] = useState(null)

  // const [similarMovies, setSimilarMovies] = useState([])
  // const [displaySimilarMovies, setDisplaySimilarMovies] = useState(false)

  function addToWatchlist() {
    // ******* API DOCUMENTATION ******
    // /addToWatchList
    // send:
    //      auth_token
    //      status (unwatched, watching, dropped, finished)
    //      movie_id
    //      movie_title
    //      movie_image
    //      rating
    // receive:
    //      message ("add successful" or "movie already on watchlist")

    const body = {

      auth_token: authToken,
      movie_id: id,
      movie_title: title,
      movie_image: image,
      rating,
      status: 'unwatched',
    };

    const options = makeOptions(body);
    fetch('/addToWatchList', options)
      // eslint-disable-next-line no-undef, no-unused-vars
      .then((response) => response.json());
    // .then(jsonData => setDeleteMessage(jsonData['message']))

    setOnWatchlist(true);
  }

  function deleteFromWatchlist() {
    // /deleteFromWatchlist
    // send:
    //      auth_token
    //      movie_id
    // receive:
    //      message (“delete successful” or “delete not successful”)

    const body = {
      auth_token: authToken,
      movie_id: id,
    };

    const options = makeOptions(body);
    fetch('/deleteFromWatchList', options)
      // eslint-disable-next-line no-undef, no-unused-vars
      .then((response) => response.json());
    // .then(jsonData => setDeleteMessage(jsonData['message']))

    setOnWatchlist(false);
  }

  function getSimilarMovies() {
    // props.setSimilarMovies(similarMoviesData)
    // props.setDisplaySimilarMovies(true)

    // *** API DOC ***
    // /getSimilar
    // send:
    //      movie_id
    // receive:
    //      movie_id
    //      movie_title
    //      movie_image
    //      genres
    //      release_date
    //      rating
    //      on_watchlist (bool)

    // *** PRODUCTION CODE ***
    const body = {
      movie_id: id,
      auth_token: authToken,
    };

    const options = makeOptions(body);

    fetch('/getSimilar', options)
      .then((response) => response.json())
      // eslint-disable-next-line react/prop-types
      // eslint-disable-next-line react/destructuring-assignment
      .then((result) => props.setSimilarMovies(result))
      // eslint-disable-next-line react/prop-types
      // eslint-disable-next-line react/destructuring-assignment
      .then(() => props.setDisplaySimilarMovies(true));
  }

  return (
    <div className="movie-container">
      <MovieTitle title={title} />
      <MovieImage image={image} />
      <span className="add-and-delete-container">
        <AddButton
          add={addToWatchlist}
          onWatchlist={onWatchlist}
        />
        <DeleteButton
          deleteFromWatchlist={deleteFromWatchlist}
          onWatchlist={onWatchlist}
        />
      </span>
      <WatchlistStatus
        authToken={authToken}
        id={id}
        title={title}
        image={image}
        rating={rating}
        status={status}
      />
      <Rating rating={rating} />
      <Genres genres={genres} />
      {/* <WatchlistStatus status={status} /> */}
      <ReleaseDate releaseDate={releaseDate} />
      <Comment comment={comment} />
      <SimilarMoviesButton getSimilarMovies={getSimilarMovies} />
    </div>
  );
}

Movie.propTypes = {
  authToken: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  id: PropTypes.string.isRequired,
  image: PropTypes.string.isRequired,
  rating: PropTypes.string.isRequired,
  status: PropTypes.string.isRequired,
  comment: PropTypes.string,
  genres: PropTypes.string,
  releaseDate: PropTypes.string,
  onWatchlist: PropTypes.any.isRequired,
  setSimilarMovies: PropTypes.func.isRequired,
  setDisplaySimilarMovies: PropTypes.func.isRequired,
};

export default Movie;
