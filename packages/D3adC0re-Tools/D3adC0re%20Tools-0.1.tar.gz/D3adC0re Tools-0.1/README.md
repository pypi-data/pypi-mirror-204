# Simple library with tools

### Installation
```
pip install d3adc0re-tools
```

### Get started
How to download song with lib:

```Python
from d3adc0re_tools import SongDownloader

# Download song by url
SongDownloader.download_song('https://www.youtube.com/watch?v=p7YXXieghto')

# Download song by name
SongDownloader.download_song('DVRST - Close Eyes')
```