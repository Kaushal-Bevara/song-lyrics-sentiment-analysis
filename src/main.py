import requests
from re import sub as reSub, split as reSplit
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup

def generateGeniusUrl(artist, songName):
    artist = reSub(r'[^a-zA-Z0-9\s]', '', artist)
    artist = artist.replace(' ', '-')
    
    

    songName = reSub(r'[^a-zA-Z0-9\s]', '', songName)
    songName = songName.replace(' ', '-')
    url = "https://genius.com/" + artist + "-" + songName + "-lyrics"
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
    

def displayStanzaSentiments(lyrics):
    # filters out the brackets which denote Intro, outro etc
    stanzas = reSplit(r'\[.*?\]', lyrics)[1:]
    for stanza in stanzas:
        
        words = stanza.split(" ")
        analyzer = SentimentIntensityAnalyzer()
        english_stop_words = stopwords.words()
        filtered_words = ""
        for word in words:
            if word not in english_stop_words:
                filtered_words += word + " "
        print(stanza + "\n")
        # prints out compound polarity score
        print("Polarity Score (Compound): " + str(analyzer.polarity_scores(filtered_words)['compound']))


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
    displayStanzaSentiments(lyrics)

if __name__ == "__main__":
    main()