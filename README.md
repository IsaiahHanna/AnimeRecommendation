# AnimeRecommendation

This project aims to provide personalized anime recommendations based on user preferences, leveraging data from MyAnimeList.

## Overview 

The Anime Recommendation System analyzes user input to suggest anime titles that align with their interests. Utilizing a dataset sourced from MyAnimeList, the system considers various attributes such as genre, synopsis, and popularity to generate recommendations.

## Dataset Features

The dataset includes the following columns:
1. **uid** - ID of anime on MyAnimeList
2. **title** - title
3. **synopsis** - brief description
4. **genre** - list of genres
5. **aired** - the date range that the show broadcasted for (one date if entry is a movie)
6. **episodes** - total episodes
7. **members** - number of people that have saved the show to their watchlist
8. **popularity** - ranking based on number of members?
9. **ranked** - ranking on MyAnimeList
10. **score** - score out of 10 (like a review)

## Project Structure
- Main.py: Recommendation class implementation, allows process to be ran as standalone
- Display.py: Handles the display of recommendations - Useful for running in terminal
- SimilarityScores.py: Computes similarity scores between anime titles
- ExceptionsList.py: Manages exceptions and edge cases
- webpage.py: Contains code for the web interface (if applicable)
- templates/: HTML templates for the web interface
- static/: Static files (CSS, JS, images) for the web interface
- animes.csv: Dataset files containing anime information

