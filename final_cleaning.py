
import requests
import billboard
import pandas as pd
import re
import spotipy
import spotipy.oauth2 as oauth2
import time

credentials = oauth2.SpotifyClientCredentials(
        client_id='f520bc427d104828bce0cf5ca8632561',
        client_secret='626e1070fcd7472b98417d021bcd08f6')

token = credentials.get_access_token()
sp = spotipy.Spotify(auth=token)

def getSpotifyURI(title, artist):
    q = title + ' artist:' + artist
    song = sp.search(q, limit=1, type='track', offset=0)
    if len(song['tracks']['items']) > 0:
        spID = song['tracks']['items'][0]['id']
        artist = sp.artist(song['tracks']['items'][0]['artists'][0]['id'])
        if len(artist['genres']) > 0:
            genre = artist['genres'][0]
        else:
            genre = "NA"
    else:
        spID = "NA"
        genre = "NA"

    return [spID, genre]


def getFeaturesForDateNewSongs(date):
    top = billboard.ChartData('hot-100', date, fetch=True)
    songs = []
    artists = []
    features = []
    dates = []
    ranks = []
    ids = []
    valence = []
    energy = []
    danceability = []
    tempo = []
    timesignature = []
    key = []
    mode = []
    genres = []
    for entry in range(100):
        if top[entry].isNew:
            aList = re.split('Featuring | x | & ', top[entry].artist)
            artist = aList[0]
            if len(aList) > 1:
                feature = aList[1]
            else:
                feature = "none"
            songs.append(top[entry].title)
            artists.append(artist)
            features.append(feature)
            dates.append(date)
            ranks.append(top[entry].rank)
            x = getSpotifyURI(top[entry].title, artist)
            sid = x[0]
            genres.append(x[1])
            ids.append(sid)
            ft = sp.audio_features(tracks=[sid])
            song = ft[0]
            if len(sid) > 5 and type(song) is dict:
                valence.append(song["valence"])
                energy.append(song["energy"])
                danceability.append(song["danceability"])
                tempo.append(song["tempo"])
                timesignature.append(song["time_signature"])
                key.append(song["key"])
                mode.append(song["mode"])
            else:
                valence.append(2.0)
                energy.append(2.0)
                danceability.append(2.0)
                tempo.append(2.0)
                timesignature.append(2.0)
                key.append(2.0)
                mode.append(2.0)
    df = pd.DataFrame(
        {'track': songs,
         'artist': artists,
         'featuring': features,
         'rank': ranks,
         'date': dates,
         'spotifyID': ids,
         'valence': valence,
         'energy': energy,
         'danceability': danceability,
         'tempo': tempo,
         'timesignature': timesignature,
         'key': key,
         'mode': mode,
         'genre': genres,
         })
    return df

def getFeaturesForDate(date, event):
    top = billboard.ChartData('hot-100', date, fetch=True)
    songs = []
    artists = []
    features = []
    dates = []
    ranks = []
    ids = []
    valence = []
    energy = []
    danceability = []
    tempo = []
    timesignature = []
    key = []
    mode = []
    genres = []
    events = []
    for entry in range(100):
        aList = re.split('Featuring | x | & ', top[entry].artist)
        artist = aList[0]
        if len(aList) > 1:
            feature = aList[1]
        else:
            feature = "none"
        songs.append(top[entry].title)
        artists.append(artist)
        features.append(feature)
        dates.append(date)
        ranks.append(top[entry].rank)
        x = getSpotifyURI(top[entry].title, artist)
        sid = x[0]
        genres.append(x[1])
        ids.append(sid)
        ft = sp.audio_features(tracks=[sid])
        song = ft[0]
        if len(sid) > 5 and type(song) is dict:
            valence.append(song["valence"])
            energy.append(song["energy"])
            danceability.append(song["danceability"])
            tempo.append(song["tempo"])
            timesignature.append(song["time_signature"])
            key.append(song["key"])
            mode.append(song["mode"])
        else:
            valence.append(2.0)
            energy.append(2.0)
            danceability.append(2.0)
            tempo.append(2.0)
            timesignature.append(2.0)
            key.append(2.0)
            mode.append(2.0)
        events.append(event)
    df = pd.DataFrame(
        {'track': songs,
         'artist': artists,
         'featuring': features,
         'rank': ranks,
         'date': dates,
         'spotifyID': ids,
         'valence': valence,
         'energy': energy,
         'danceability': danceability,
         'tempo': tempo,
         'timesignature': timesignature,
         'key': key,
         'mode': mode,
         'genre': genres,
         })
    return df

def two_weeks(date, event):
    df = getFeaturesForDate(date, event)
    new_date = billboard.ChartData('hot-100', date).nextDate
    new_df = getFeaturesForDate(new_date, event)
    df = df.append(new_df)
    return df

print "start"

bee_movie = two_weeks('2007-11-10', 'Bee Movie')
bee_movie.to_csv('bee_movie.csv', sep=',', encoding='utf-8')
print 'done'

beatles = two_weeks('1970-04-11', 'Beatles break up')
beatles.to_csv('beatles.csv', sep=',', encoding='utf-8')

vietnam_end = two_weeks('1973-03-31', 'End of Vietnam War')
vietnam_end.to_csv('v_end.csv', sep=',', encoding='utf-8')

black_monday = two_weeks('1987-10-17', 'Black Monday')
black_monday.to_csv("black_monday.csv", sep=',', encoding='utf-8')

berlin_wall = two_weeks('1989-11-18', 'Fall of the Berlin Wall')
berlin_wall.to_csv('berlin.csv', sep=',', encoding='utf-8')

columbine = two_weeks('1999-04-24', 'Columbine Shooting')
columbine.to_csv('columbine.csv', sep=',', encoding='utf-8')

print "done"

#60s
cubanMissile = two_weeks('1962-10-20', 'Cuban Missile Crisis')

vietnamStart = two_weeks('1964-08-08', 'Vietnam Start')
vietnamStart.to_csv('vietnam.csv', sep=',', encoding='utf-8')

MLK = two_weeks('1963-08-31', 'I Have a Dream Speech')
MLK.to_csv('MLK.csv', sep=',', encoding='utf-8')

JFK = two_weeks('1963-11-30', 'JFK Assassination')
JFK.to_csv('JFK.csv', sep=',', encoding='utf-8')

summer_of_love = two_weeks('1967-06-10', 'Summer of Love')
summer_of_love = summer_of_love.append(two_weeks('1967-06-24', 'Summer of Love'))
summer_of_love = summer_of_love.append(two_weeks('1967-07-08', 'Summer of Love'))
summer_of_love = summer_of_love.append(two_weeks('1967-07-22', 'Summer of Love'))
summer_of_love = summer_of_love.append(two_weeks('1967-08-05', 'Summer of Love'))
summer_of_love = summer_of_love.append(two_weeks('1967-08-19', 'Summer of Love'))
summer_of_love = summer_of_love.append(two_weeks('1967-09-02', 'Summer of Love'))
summer_of_love = summer_of_love.append(two_weeks('1967-09-16', 'Summer of Love'))
summer_of_love.to_csv('love.csv', sep=',', encoding='utf-8')

print "done"

apollo11 = two_weeks('1969-07-26', 'Apollo 11 moon landing')

#70s
beatles = two_weeks('1970-04-11', 'Beatles break up')
beatles.to_csv('beatles.csv', sep=',', encoding='utf-8')

watergate = two_weeks('1972-06-24', 'Watergate scandal')

vietnam_end = two_weeks('1973-03-31', 'End of Vietnam War')
vietnam_end.to_csv('v_end.csv', sep=',', encoding='utf-8')

elvis_dies = two_weeks('1977-08-20', 'Elvis Presley Dies')

#80s
mtv = two_weeks('1981-08-07', 'MTV Launch')

black_monday = two_weeks('1987-10-17', 'Black Monday')

berlin_wall = two_weeks('1989-11-18', 'Fall of the Berlin Wall')

#90s
internet = two_weeks('1991-08-10', 'Launch of the World Wide Web')

LA_riots = two_weeks('1992-04-02', 'Rodney King Riots')

storm = two_weeks('1993-03-13', 'Storm of the Century')

ok_bombing = two_weeks('1995-04-22', 'Oklahoma City Bombing')

OJ = two_weeks('1995-10-07', 'OJ Simpson Acquittal')

columbine = two_weeks('1999-04-24', 'Columbine Shooting')

#00s
y2k = two_weeks('2000-01-08', 'Y2K')








