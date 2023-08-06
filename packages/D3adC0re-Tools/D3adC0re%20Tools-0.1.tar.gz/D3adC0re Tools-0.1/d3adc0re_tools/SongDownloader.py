from time import sleep as wait
from googlesearch import search
import requests
import os

headers = {
    'authority': 'loader.to',
    'accept': '*/*',
    'origin': 'https://en.loader.to',
    'referer': 'https://en.loader.to/'
}

def _get_song_id(song_url: str, print_: bool):
    song_request = requests.get('https://loader.to/ajax/download.php', params={
            'format': 'mp3',
            'url': song_url,
        }, headers=headers).json()

    if print_:
        print(f'Song Title: {song_request["title"]}\nSong ID: {song_request["id"]}')

    return (song_request['id'], song_request['title'])

def download_song(query: str = 'DVRST - Close Eyes', download_dir: str = './', print_: bool = True):
    """Simple wrapper for loader.to (for downloading songs), with song metadata!"""

    song_url = query

    if song_url.startswith('http'):
        song_id = _get_song_id(song_url, print_)

    elif not song_url.startswith('http'):
        for result in search(song_url, num_results=100):
            if 'youtube.com' and 'watch' in result or 'soundcloud' in result:  
                song_url = result
                break

        song_id = _get_song_id(song_url, print_)

    while True:
        get_download_progress = requests.get('https://loader.to/ajax/progress.php', params={'id': song_id[0]}, headers=headers).json()
        
        if print_:
            print('Download progress: '+str(int(get_download_progress['progress'] / 10)) if int(get_download_progress['progress'] / 10)!=0 else '')

        wait(1)

        if get_download_progress['success'] == 1:
            dwnload_url = get_download_progress['download_url']
            if print_:
                print('Downloaded')
            break

    with open(download_dir+str(song_id[1] if not str(song_id[1]).startswith('http') else os.path.basename(song_id[1]))+'.mp3', 'wb') as mp3:
        mp3.write(requests.get(dwnload_url).content)
    
    if print_:
        print('Saved!')

print('SongDownloader initialized!')