# Movie-Magic App 







<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#app-link">App Link</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
     <li><a href="#known-issues">Known Issues</a></li>
      <li><a href="#developers">Developers</a></li>
        

  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


A web app for maintaining and sharing movie watchlists. Users can search movies to add to their watchlist where they can specify what the current status of that movie is. Users can add friends and view their friends' watchlists.

### App Link
[Movie-Magic Link](https://movie-magic-2.herokuapp.com/)







### Built With

Here is a list of major frameworks we employed while building this project:
  
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [Google FireBase](https://firebase.google.com)
* [React](https://reactjs.org/docs/getting-started.html)



<!-- GETTING STARTED -->
## Getting Started

To get started with this project, simply follow the steps below. It is assumed one has access to a shell to execute the necessary commands.




### Installation


1. Install the required files via running -pip install requirements.txt
2. Create a .env file containing the following information:
    * ``` MOVIEDB_KEY ```
        - Can be obtained by creating an account from [TheMovieDB](https://www.themoviedb.org/) and navigate to API under profile settings. 
    * All enviroment variables that start with ```FIREBASE``` are for Google Firebase 
       - Can be obtained by creating an account and project at [Firebase](https://firebase.google.com/)
    * ``` FIREBASE_PROJECT_ID ```
    * ``` FIREBASE_PRIVATE_KEY ```
    * ``` FIREBASE_CLIENT_EMAIL ```
    * All enviroment variables that start with ```REACT_APP_FIREBASE``` are for Google Firebase's login process
        - Can be obtained by creating an account and project at [Firebase](https://firebase.google.com/)
    * ```REACT_APP_FIREBASE_API_KEY```
    * ```REACT_APP_FIREBASE_APP_ID```
    * ```REACT_APP_FIREBASE_DATABASE_URL```
    * ```REACT_APP_FIREBASE_PROJECT_ID```
    * ```REACT_APP_FIREBASE_SENDER_ID```




<!-- USAGE EXAMPLES -->
## Usage

1. On loading the page, if the user is not already logged in, the user will be taken to a login screen. The user logs into the website by clicking on the login button. From there the user is taken to a Google login screen which will handle the rest of the login. This includes registering the user if they do not have a Google account.

2. After login, the user will be redirected to the search page. From here, the user can type input into a textbox to find movies that matched their search. The user can either input an actor's name or a movie's name. The webpage will then output all movies to the page once the input is submitted. There is an add and remove button under each movie. Only one button is active at a time depending on whether the movie is on your watchlist or not. The user can click between the buttons to add or remove the movie from the watchlist

3. The watchlist can be accessed from the search page by clicking on the button that says watchlist. The user is then directed to their personal watchlist. They can see all the movies they have added. Additionally they can also remove movies from their watchlist.



<!-- KNOWN ISSUES -->
## Known Issues

1. <del>Currently our app does not work on Heroku. We think this is because we have included Google Authentication to our project which is crashing Heroku. Our app does run locally though. As such we have not implemented Continous Deployment. </del> As of the latest release, this bug has been resolved.

## Linting
### Python
1. E0401 (Import error)
Disabled because pylint was not correctly detecting import files even though the code was able to import files to run
2. W1508 (Invalid envvar default)
Disabled because the int 8080 was present in os.getenv. The number was needed to host the app. 

### JavaScript
1. `react/function-component-definition` was set to `[2, { "namedComponents": "function-declaration" }]` to aloow for function declerations to not error, this is not the default for this, but the fuinction decleration method is personal preference in most cases so we chose this
2. `"react/jsx-filename-extension"` is set to `"off"` to because we didn't realise we needed to have .jsx and not .js for jsx files. 
3. `"react/jsx-no-bind"` is set to `[2, {"allowFunctions": true, "allowArrowFunctions": true}]` so that we can have funcions passes into components without errors.
4. `"react/forbid-prop-types"` is set to `"off` because we wanted to pass any datatype in as a prop. We are passing may different types of data to props os it was easiest to just disable the warning instead of specify every data type.
5. `"react/require-default-props"` is set to `"off"` because out app is so dynamic and backend heavy we can't have default values for props.
6. `"import/no-cycle"` is set to `"off"` because we had a prop import cycle that didn't break the app but was needed to render differnt pages in similar ways. 


<!-- DEVELOPERS -->
## Developers

* Nana Krampah
* Brandon Hodges
* Devang Patels
* Steven Maharath


