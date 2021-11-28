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
* [Google Authentication](https://developers.google.com/identity/protocols/oauth2)
* [React](https://reactjs.org/docs/getting-started.html)



<!-- GETTING STARTED -->
## Getting Started

To get started with this project, simply follow the steps below. It is assumed one has access to a shell to execute the necessary commands.




### Installation


1. Install the required files via running -pip install requirements.txt
2. Create a .env file containing the following information:
    * ``` MOVIEDB_KEY ```
        - Can be obtained by creating an account from [TheMovieDB](https://www.themoviedb.org/) and navigate to API under profile settings. 
    *  ``` FIREBASE_PROJECT_ID ```
    * ``` FIREBASE_PRIVATE_KEY ```
    * ``` FIREBASE_CLIENT_EMAIL ```
    * ``` DATABASE_URL ```
        - Can be obtained by creating an account and project at [Firebase](https://firebase.google.com/)
    * ``` GOOGLE_CLIENT_ID ```
    * ``` GOOGLE_CLIENT_SECRET ```
        - Can be obtained by creating a Google Account and creating a Google API Project. Documentation can be found [here](https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid)




<!-- USAGE EXAMPLES -->
## Usage

1. On loading the page, if the user is not already logged in, the user will be taken to a login screen. The user logs into the website by clicking on the login button. From there the user is taken to a Google login screen which will handle the rest of the login. This includes registering the user if they do not have a Google account.

2. After login, the user will be redirected to the search page. From here, the user can type input into a textbox to find movies that matched their search. The user can either input an actor's name or a movie's name. The webpage will then output all movies to the page once the input is submitted. There is an add and remove button under each movie. Only one button is active at a time depending on whether the movie is on your watchlist or not. The user can click between the buttons to add or remove the movie from the watchlist

3. The watchlist can be accessed from the search page by clicking on the button that says watchlist. The user is then directed to their personal watchlist. They can see all the movies they have added. Additionally they can also remove movies from their watchlist.



<!-- KNOWN ISSUES -->
## Known Issues

1. <del>Currently our app does not work on Heroku. We think this is because we have included Google Authentication to our project which is crashing Heroku. Our app does run locally though. As such we have not implemented Continous Deployment. </del> As of the latest release, this bug has been resolved.




<!-- DEVELOPERS -->
## Developers

* Nana Krampah
* Brandon Hodges
* Devang Patels
* Steven Maharath


