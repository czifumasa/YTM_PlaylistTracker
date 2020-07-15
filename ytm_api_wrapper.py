from ytmusicapi import YTMusic

from common import *


def open_api():
    log('Logging into YouTube Music...')
    api = YTMusic('headers_auth.json')
    log('Login Successful.')
    return api


def get_all_songs_from_my_library(api):
    library_songs = api.get_library_songs(100000)

    log('\nFetched ' + str(len(library_songs)) + ' tracks from Library')
    return library_songs


# returns [{id: playlistId, name: playlistName},...]
def get_my_playlist_ids_and_names(api):
    my_playlists = api.get_library_playlists(200)
    playlist_ids = []
    for playlist in my_playlists:
        playlist_ids.append({'id': playlist['playlistId'], 'name': playlist['title']})
    return playlist_ids


def get_songs_from_playlist(api, playlist_id):
    playlist = api.get_playlist(playlist_id, 5000)

    log('\nFetched ' + str(len(playlist['tracks'])) + ' tracks from \'' + playlist['title'] + '\' playlist')
    return playlist['tracks']


# returns [id1:[song1,song2,song3], id2: [song4],...]
def get_songs_from_playlist_grouped_by_id(api, playlist_id):
    playlist = get_songs_from_playlist(api, playlist_id)
    return group_songs_by_id(playlist['tracks'])


def group_songs_by_id(songs_list):
    songs_by_id = {}

    for track in songs_list:
        if track['videoId'] in songs_by_id:
            songs_by_id[track['videoId']].append(track)
        else:
            songs_by_id[track['videoId']] = [track]

    return songs_by_id


def create_list_of_duplicated_sons(grouped_songs_by_id):
    duplicated_songs = flatten_list(
        [get_list_of_duplicated_songs(song_id, songs_list) for (song_id, songs_list) in grouped_songs_by_id.items()])

    log('Found ' + str(len(duplicated_songs)) + ' duplicated tracks')
    return duplicated_songs


def get_list_of_duplicated_songs(song_id, songs_list):
    if len(songs_list) > 1:
        if song_id is not None:
            return [songs_list[0]]
        else:
            song_strings = [song_string_representation(song) for song in songs_list]
            duplicated_song_strings = get_duplicated_items_from_list(song_strings)

            return [next(song for song in songs_list if song_string_representation(song) == song_string) for song_string
                    in duplicated_song_strings]
    else:
        return []


def export_songs(songs, playlist):
    export_result = []
    for song in songs:
        song_row = [song_artists_string_representation(song['artists']),
                    song['title'],
                    song_string_representation(song),
                    song_album_string_representation(song['album']),
                    song['videoId'],
                    set_video_id_string_representation(song),
                    playlist['name'],
                    playlist['id']]
        export_result.append(song_row)
    return export_result


def song_string_representation(song):
    artists = song_artists_string_representation(song['artists'])
    title = song['title']

    if artists:
        return artists + ' - ' + title
    return ' - ' + title  # todo fix 6.24


def song_artists_string_representation(artists):
    if artists:
        artists_names = [artist['name'] for artist in artists]
        return ','.join(artists_names)
    return None


def song_album_string_representation(album):
    if album:
        if "name" in album:
            return album["name"]
    return None


def set_video_id_string_representation(song):
    return song['setVideoId'] if 'setVideoId' in song else None


def create_temporary_id_for_songs_without_one(playlist, counter):
    return 'missingId_from_' + playlist['id'] + '_' + str(counter)

































