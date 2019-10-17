
def user_playlist_tracks_full(spotify_connection, user, playlist_id=None, fields=None, market=None):
    """
    args:
        user: User ID of playlist owner
        playlist_id: ID of the Spotify playlist
        fields: Can select specific fields to return. Refer to Spotify documentation for further details
        market: Country code
    """
    # first run through also retrieves total no of songs in library
    response = spotify_connection.user_playlist_tracks(user, playlist_id, fields=fields, limit=100, market=market)
    results = response["items"]

    # subsequently runs until it hits the user-defined limit or has read all songs in the library
    while len(results) < response["total"]:
        response = spotify_connection.user_playlist_tracks(
            user, playlist_id, fields=fields, limit=100, offset=len(results), market=market)
        results.extend(response["items"])
    return results



def scrape_spotify(spotify_connection, user, playlist):
    '''
    Function to create a dataframe of audio features, given the user name and playlist id
    Args:
        spotify_connection: spotipy.Spotify(auth = token) object
        user: Name of user that playlist is extracted from. Enter in string format
        playlist_id: id of Spotify playlist. Under share, select copy Spotify uri

    Returns: DataFrame object
    '''
    search = user_playlist_tracks_full(spotify_connection, user, playlist_id = playlist, market = 'US')

    artist_name = [search[i]['track']['artists'][0]['name'] for i in range(len(search))]
    artist_id = [search[i]['track']['artists'][0]['id'] for i in range(len(search))]
    track_name = [search[i]['track']['name'] for i in range(len(search))]
    track_id = [search[i]['track']['id'] for i in range(len(search))]
    release_date = [search[i]['track']['album']['release_date'] for i in range(len(search))]
    popularity_metric = [search[i]['track']['popularity'] for i in range(len(search))]

    audio_features = spotify.audio_features(track_id[0:100])
    for i in range(0, int(len(search)/100)-1):
        audio_features.extend(spotify.audio_features(track_id[100+100*i: 200+100*i]))

    song_df = pd.DataFrame(audio_features)
    song_df['track'] = track_name
    song_df['artist'] = artist_name
    song_df['release_date'] = release_date
    song_df['artist_id'] = artist_id
    song_df['track_id'] = track_id
    song_df['popularity'] = popularity_metric

    return song_df


def scrape_billboard(ranking_week): #format '2018-01-06'

    data_path = os.getcwd() + '/data/billboard_weeks/billboard_{}.pickle'.format(ranking_week)
    url = 'https://www.billboard.com/charts/hot-100/{}'.format(ranking_week)
    response = requests.get(url)
    page = response.text
    soup = BS(page, 'lxml')

    items = soup.find_all('div', {'class': 'chart-list-item'})
    rank = soup.find_all('div', {'class': 'chart-list-item__rank'})
    song_title = soup.find_all('div', {'class': 'chart-list-item__title'})
    artist_name = soup.find_all('div', {'class': 'chart-list-item__artist'})

    headers = ['ranking', 'title', 'artist', 'rank_week']
    weekly_rank = [rank[i].string.replace('\n','').strip() for i in range(len(items))]
    title = [song_title[i].text.replace('\n','').strip() for i in range(len(items))]
    artist = [artist_name[i].text.replace('\n','').strip() for i in range(len(items))]
    wk_ranking = [ranking_week] * len(items)

    billboard_top = dict(zip(headers, [weekly_rank, title, artist, wk_ranking]))

    return pd.DataFrame(billboard_top).to_pickle(data_path)


def generate_billboard_weeks(start_date, end_date):
    '''
    Returns a pickle file for the range of weeks given;
    '''
    start = dt.datetime.strptime(start_date, '%m/%d/%y')
    assert start.weekday() == 5, 'The start of the week must begin on a Saturday'
    end = dt.datetime.strptime(end_date, '%m/%d/%y')

    for week in range(0, ((end-start).days// 7) + 1):
        scrape_billboard(dt.datetime.strftime(start + dt.timedelta(days = 7 * week), '%Y-%m-%d'))
    return None



def merge_billboard(start_date, end_date):

    start = dt.datetime.strptime(start_date, '%m/%d/%y')
    assert start.weekday() == 5, 'The start of the week must begin on a Saturday'
    end = dt.datetime.strptime(end_date, '%m/%d/%y')
    '''
    Merges the pickle files in the given date range
    start = dt.datetime.strptime(start_date, '%m/%d/%y')
    assert start.weekday() == 5, 'The start of the week must begin on a Saturday'
    end = dt.datetime.strptime(end_date, '%m/%d/%y')
    '''
    dfs = []
    for week in range(0, ((end-start).days// 7) + 1):
        formatted_date = dt.datetime.strftime(start + dt.timedelta(days = 7 * week), '%Y-%m-%d')
        dfs.append(pd.read_pickle(os.getcwd() + '/data/billboard_weeks/billboard_{}.pickle'.format(formatted_date)))
        billboard_df = pd.concat(dfs, axis = 0, ignore_index = True)
    return billboard_df
