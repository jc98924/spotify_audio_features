# Is it a Banger? Predicting Song Popularity through Spotify's Audio Features

#### Introduction

Using supervised classification techniques, I wanted to see if it would be possible to take Spotify's audio features to predict if a song would be a hit or not.

Music is a huge part of my life and I have always been fascinated by the pervasiveness of music across geography and different cultures. The idea for this project had been in the back of my mind ever since I read a Medium article where the author took 'audio features' generated from all of his past Spotify playlists to see how his musical tastes changed over the years. The web app was developed by The Echo Nest which as since been acquired by Spotify. The audio features given are as listed:

* **acousticness**
* **danceability**
* **energy**
* **instumentalness**
* **key**
* **liveness**
* **loudness**
* **mode**
* **speechiness**
* **tempo**
* **valence**

For further details about each feature, the descriptions are listed in the **model_analysis.ipynb** file. 

#### Business Use

In today's digital age the barrier to releasing songs has become almost trivial, but this has also led to an exponential increase in the 'noise'. One of the largest barriers to breaking into the music industry is simply the act of getting noticed. Although by no means is it a guarantee of sustained success, being able to produce a top 'hit' goes a long ways towards getting your foot in the door. By using Spotify's audio features to create a model, I hope to provide recommendations for emerging producers on how to best create songs that have the highest chance to produce a hit. 

## Process Flow

### Data Acquisition & Cleaning

Before diving into any project, it's very important to make sure to frame your problem correctly. The first challenge I ran into was how I would classify if a song was a hit or not. After much deliberation, I ended up using a song's presence on the Billboard Top 100 as my measure. To generate my positive class, I scraped the Billboard Hot 100 list for each week from from 2018 - June 2019 which gave me approximately 900~ unique entries. If a song from the Spotify playlist was on the Billboard list, it would be labeled (1). 

The audio features themselves could only be obtained through Spotify's Developer API, which was the first step to getting my data. I ended up using a Python wrapper called **Spotipy** to access the API as this would allow me to loop through and grab all of the data that I needed at once. On my first run-through, I simply typed year: 2018, threw 10,000 songs onto a playlist, and grabbed all of the audio features that way. Unfortunately, this led to a lot of duplicate songs since Spotify views a song as unique if it's on a different album. I also ran into issues with fuzzy-merging the Billboard and Spotify dataframes due to this.

This led me to create a more carefully-curated playlist where I only added albums that were released in 2018 (US albums only) based on Wikipedia's list. I then went back and manually added singles from 2018 that I knew were on the Billboard Hot 100 to try to alleviate my class imbalance issues. In addition, I went back and grabbed artist genres as I suspected that would significantly impact my model's results.  For my final dataset, I had 5393 observations with 7.56% labeled in the positive class. 

### EDA

Going into this project, I suspected that the songs that would be the most popular would be songs that rated high on danceability, energy, and loudness. After all, these are the songs that would be popular in clubs and on the radio.

![audio_feature_pairplot](https://github.com/jc98924/spotify_audio_features_success/img/audio_feature_pairplot.png)



Based on the pairplot shown above we can see that there is slight separation of hit and non-hit songs for both danceability and energy but it isn't substantial.

### Model Results

For classification problems, the metric used to score the model is very important. Given that my product is geared towards upcoming producers, I felt that recall was way more important than precision since it's completely expected for a new producer to grind and produce a lot of tracks that go unrecognized. Being able to capture all of the successes is more valuable than making the correct predictions. However, precision should not be completely ignored as time is a finite resource. After some consideration, I settled on using F**β**  (with **β**  = 2) which essentially gives recall twice the importance of precision. 

After cross-validating my data across a range of models, the Random Forest Classifier gave me the best validation F**β** score. After tuning the hyperparameters via GridSearchCV, the test-set F**β** score came out to be **57.78%**.

The table below shows the features with the top 10 importance values.

| Variable         | Importance |
| ---------------- | :--------: |
| rap + hip/hop    |   0.300    |
| danceability     |   0.102    |
| rock             |   0.082    |
| instrumentalness |   0.075    |
| energy           |   0.067    |
| acousticness     |   0.053    |
| minutes          |   0.500    |
| loudness         |   0.047    |
| valence          |   0.041    |
| tempo            |   0.041    |

What really surprised me about the results was that rap & hip/hop had such a strong effect on my model. Apparently, I had missed the memo when rap/hip-hop overtook pop as the most popular genre in 2017. I was also surprised that pop did not show up as an important feature but I believe that is due to how the elements of pop are being incorporated in the other genres. The graph below shows the artists with the most hits in my dataset. As you can see, rap/hip-hop/r&b artists have dominated with the only except being Ariana Grande. 

![success_songs](https://github.com/jc98924/spotify_audio_features_success/img/success_songs.png)



The feature importances for the audio features were mostly in line with what I expected. However, I was also surprised by the inclusion of instrumentalness 

![audio_features](https://github.com/jc98924/spotify_audio_features_success/img/audio_features.png)

### Conclusion

Although my model shows some success in classifying hit songs, there is still much work to be done before it is ready for production use. As is the case with machine-learning in general, the integrity of the data is by far the most important part of the model. There are two main avenues that can be taken to refine this project:

* Dataset should be way more comprehensive than just 5,400 songs. In addition, the genres need to be much more granular as Spotify only provides the genre on an artist-level. 
* While the Billboard Top 100 is still relevant to a degree, music streaming has definitely changed the game. The positive class should be expanded to include measures such as popularity on the various streaming services (including Spotify's own)

