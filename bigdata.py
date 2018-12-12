import requests
import billboard
import pandas as pd
import re
import spotipy
import spotipy.oauth2 as oauth2
import time
import datetime

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

def getFeaturesForDate(date):
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

start = time.time()
print("start")

date = '1980-01-05'
num_date = int(date[0:4])
eighties = getFeaturesForDate(date)
date = billboard.ChartData('hot-100', date).nextDate
while num_date < 1990:
    print date
    df = getFeaturesForDate(date)
    date = billboard.ChartData('hot-100', date).nextDate
    num_date = int(date[0:4])
    eighties = eighties.append(df)
    eighties.to_csv('eighties.csv', sep=',', encoding='utf-8')

elapsed = time.time()
print(elapsed - start)

nineties = getFeaturesForDate(date)
date = billboard.ChartData('hot-100', date).nextDate
while num_date < 2000:
    print date
    df = getFeaturesForDate(date)
    date = billboard.ChartData('hot-100', date).nextDate
    num_date = int(date[0:4])
    nineties = nineties.append(df)
nineties.to_csv('nineties.csv', sep=',', encoding='utf-8')

elapsed = time.time()
print(elapsed - start)

zeros = getFeaturesForDate(date)
date = billboard.ChartData('hot-100', date).nextDate
while num_date < 2010:
    print date
    df = getFeaturesForDate(date)
    date = billboard.ChartData('hot-100', date).nextDate
    num_date = int(date[0:4])
    zeros = zeros.append(df)
zeros.to_csv('zeros.csv', sep=',', encoding='utf-8')

elapsed = time.time()
print(elapsed - start)

tens = getFeaturesForDate(date)
date = billboard.ChartData('hot-100', date).nextDate
while date != "2018-12-08":
    print date
    df = getFeaturesForDate(date)
    date = billboard.ChartData('hot-100', date).nextDate
    tens = tens.append(df)
tens.to_csv('tens.csv', sep=',', encoding='utf-8')

elapsed = time.time()
print(elapsed - start)