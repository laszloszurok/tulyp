# tulyp

tulyp is a simple python script which displays the lyrics of the currently playing spotify song in the terminal. It checks for lyrics from 3 sources (stops at the first successful result): first genius.com, then azlyrics.com and finally google.

Once it finds lyrics, it pipes the text into a command line utility, called bat. Bat provides line numbering, and paging (so you can scroll through long lyrics with j/k or the arrow keys).

If one of the sources is provided as the first argument, only that source will be tried. Can be used like this:
```
./tulyp genius
./tulyp azlyrics
./tulyp google
```
