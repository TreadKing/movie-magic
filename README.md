# movie-magic
### Description
A web app for maintaining and sharing movie watchlists. Users can search movies to add to their watchlist where they can specify what the current status of that movie is. Users can add friends and view their friends' watchlists.

### Link to Heroku Website
[Movie-Magic Link](https://movie-magic-1.herokuapp.com/)

### Bugs
1. Currently our app does not work on Heroku. We think this is because we have included Google Authentication to our project which is crashing Heroku. Our app does run locally though. As such we have not implemented Continous Deployment. 

### Tools Used
* Google Authentication
* Flask
* React 

### Installation and Use
1. Install the required files via running -pip install requirements.txt
2. Create a .env file containing the following information:
    1. MOVIEDB_KEY
        - Can be obtained by creating an account from [TheMovieDB](https://www.themoviedb.org/) and navigate to API under profile settings. 
    2. FIREBASE_PROJECT_ID
    3. FIREBASE_PRIVATE_KEY
    4. FIREBASE_CLIENT_EMAIL
    5. DATABASE_URL
        - Can be obtained by creating an account and project at [Firebase](https://firebase.google.com/)
    6. GOOGLE_CLIENT_ID
    7. GOOGLE_CLIENT_SECRET
        - Can be obtained by creating a Google Account and creating a Google API Project. Documentation can be found [here](https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid)

### Running
1. On loading the page, if the user is not already logged in, the user will be taken to a login screen. The user logs into the website by clicking on the login button. From there the user is taken to a Google login screen which will handle the rest of the login. This includes registering the user if they do not have a Google account.

2. After login, the user will be redirected to the search page. From here, the user can type input into a textbox to find movies that matched their search. The user can either input an actor's name or a movie's name. The webpage will then output all movies to the page once the input is submitted. There is an add and remove button under each movie. Only one button is active at a time depending on whether the movie is on your watchlist or not. The user can click between the buttons to add or remove the movie from the watchlist

3. The watchlist can be accessed from the search page by clicking on the button that says watchlist. The user is then directed to their personal watchlist. They can see all the movies they have added. Additionally they can also remove movies from their watchlist.