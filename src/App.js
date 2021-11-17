import './App.css';
import MovieSearch from './components/MovieSearch.js';

function App() {
  var authToken = document.cookie.slice(11)
  return (
    <MovieSearch authToken={authToken} />
  );
}

export default App;
