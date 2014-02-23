# Olympic Medal Counter

# Overviedw

A simple python script to scrape google and display the current medal standings for the 2014 Sochi Olympics.
It also reads results from a local json file so that it will keep wokring (in a sense) after Google stops posting results.

Built on a rainy day while I was refreshing my Python skillz.

# Usage and Example Output:

$ python bin/get_medal_count_from_google.py --help
    usage: get_medal_count_from_google.py [-h] [--source {FromFile,FromWeb}]
                                          [--top TOP] [--ordered {total,gold}]

    optional arguments:
      -h, --help            show this help message and exit
      --source {FromFile,FromWeb}
                            where do we get the datas?
      --top TOP             How many coutries to list?
      --ordered {total,gold}
                            How to sort countries : gold count or total count?

Lets order by the number of gold medals and get the data from Google

    $ python bin/get_medal_count_from_google.py --source FromWeb --ordered gold
    Instantiating FromWeb
    Russia               - 33  : 13 Gold, 11 Silver, 9  Bronze
    Norway               - 26  : 11 Gold, 5  Silver, 10 Bronze
    Canada               - 25  : 10 Gold, 10 Silver, 5  Bronze
    United States        - 28  : 9  Gold, 7  Silver, 12 Bronze
    Germany              - 19  : 8  Gold, 6  Silver, 5  Bronze

Lets order by the total medal count this time

    $ python bin/get_medal_count_from_google.py --source FromWeb --ordered total
    Instantiating FromWeb
    Russia               - 33  : 13 Gold, 11 Silver, 9  Bronze
    United States        - 28  : 9  Gold, 7  Silver, 12 Bronze
    Norway               - 26  : 11 Gold, 5  Silver, 10 Bronze
    Canada               - 25  : 10 Gold, 10 Silver, 5  Bronze
    Netherlands          - 24  : 8  Gold, 7  Silver, 9  Bronze

I just want to know who is the BEST. (Russia is BEST!!)

    $ python bin/get_medal_count_from_google.py --source FromWeb --ordered total --top 1
    Instantiating FromWeb
    Russia               - 33  : 13 Gold, 11 Silver, 9  Bronze

Ahh google is a)blocking me, or 2) Not postingresults, 3) Changed their format, lets use the local results.json 

    $ python bin/get_medal_count_from_google.py --source FromFile
    Instantiating FromFile
    Russia               - 33  : 13 Gold, 11 Silver, 9  Bronze
    United States        - 28  : 9  Gold, 7  Silver, 12 Bronze
    Norway               - 26  : 11 Gold, 5  Silver, 10 Bronze
    Canada               - 25  : 10 Gold, 10 Silver, 5  Bronze
    Netherlands          - 24  : 8  Gold, 7  Silver, 9  Bronze

# Dependancies:

- Python 2. Lets say 2.7
- Python lxml library - I had trouble installing with pip as it has C dependancies. I had success on ubuntu just installing the deb via 'sudo apt-get install python-lxml'
- Internets. Specifically a cooperative Google.

# Bugs

- None of the tie breaks are implemented 
    - (ordered=gold and #gold == #gold, use #silver then #bronze) 
    - (ordered=total and #total == #total, use #gold then #silver then #bronze)
