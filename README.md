# tulyp

tulyp is a simple python script which displays the lyrics of the currently playing spotify song in the terminal. It checks for lyrics from 3 sources (stops at the first successful result): first genius.com, then azlyrics.com and finally google.

Players other than spotify can be used too, if they are compliant with the mpris specification. Change the value of the player variable in the script to the name of the player (for ex. player = "ncspot").

Once tulyp finds lyrics, it pipes the text into a command line utility, called bat. Bat provides line numbering, and paging (so you can scroll through long lyrics with j/k or the arrow keys).

If one of the sources is provided as the first argument, only that source will be tried. Can be used like this:
```
./tulyp genius
./tulyp azlyrics
./tulyp google
```

Without arguments it performs checks automatically, as needed.

## Requirements

* bat to display the lyrics (it is available in most linux distributions default repositories)
* lyricsgenius python lib to be able to get lyrics from genius.com (pip install lyricsgenius)
* python-dbus to get the currently playing song (also available in default repos)

## Naming

Bat provides paging, so we got a terminal user interface => tu
We are dealing with lyrics => ly
The script is written in python => p
tu + ly + p = tulyp
I am so good at naming things.
