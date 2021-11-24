import './App.css';
import Login from './components/Login';
import MovieSearch from './components/MovieSearch.js';
import { getAuth, onAuthStateChanged } from "firebase/auth";


function App() {
  // var authToken = document.cookie.slice(11)
  return (
    <Login />
  );
}

export default App;
