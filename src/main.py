import requests
from bs4 import BeautifulSoup

def generateGeniusUrl(artist, songName):
    url = ""
    for c in artist:
        if c.isalnum():
            url += c
        if c == " ":
            url += "-"
    url += "-"
    for c in songName:
        if c.isalnum():
            url += c
        if c == " ":
            url += "-"
    url = "https://genius.com/" + url + "-lyrics"
    return url

def extractLyrics(doc):
    bs = BeautifulSoup(doc, 'html.parser')
    lyricsDiv = bs.find_all("div", {"class" : "Lyrics__Container-sc-3d1d18a3-1 bjajog"} , recursive=True)
    
    # replace line break html elements with new lines
    for i in lyricsDiv:
        for br in i.find_all("br"):
            br.replace_with("\n")
    
    lyrics = "";
    for i in lyricsDiv:
        lyrics += i.text

    # removes all non-lyrical text from before lyrics
    # the lyrics officialy start at the brackets on the website
    lyrics = lyrics[lyrics.find("["):]
    return lyrics

    
def main():
    artistInput = input("Input Artist Stage Name Exactly: ")
    songInput = input("Input Song Name Exactly: ")

    geniusUrl = generateGeniusUrl(artistInput, songInput)
    print("Fetching from : " + geniusUrl)

    r = requests.get(geniusUrl)
    if r.status_code != 200:
        print("Either the song isn't available on genius.com or there is a typo")
        return
    lyrics = extractLyrics(r.text)
    print(lyrics)

if __name__ == "__main__":
    main()