import configparser
import nltk
from nltk.corpus import stopwords, words
from nltk.tokenize import word_tokenize
import pandas as pd
import re
import spacy
nlp = spacy.load("de_core_news_md")

custom_stopwords = {"hallo", "moin", "hi", "servus", "tja", "na", "bitte", "danke", "grüße", "huhu", "heey"}

try:
    english_words = set(words.words())
    stopwords = set(stopwords.words("german"))
    stopwords = stopwords.union(custom_stopwords)
except LookupError:
    nltk.download("stopwords")
    nltk.download("words")
    english_words = set(words.words())
    stopwords = set(stopwords.words("german"))
    stopwords = stopwords.union(custom_stopwords)


umlaute = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}
german_abbr = {
    "hallöchen": "Hallo",
    "hbf": "Hauptbahnhof",
    "plz": "Postleitzahl",
    "str": "Straße",
    "vlt": "vielleicht",
    "vllt": "vielleicht",
}


def is_german(text, treshold):
    words = text.split()
    count_english_words = 0
    count_total_words = len(words)
    
    for word in words:
        if word.lower() in english_words:
            count_english_words += 1

    if count_english_words / count_total_words > treshold:
        return False
    
    return True


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.cfg")
    
    p_english_treshold = float(config["PREPARE"]["english_treshold"])
    g_subreddit_name = str(config["GLOBAL"]["subreddit"])
    p_word_treshold = int(config["PREPARE"]["word_treshold"])
    
    count_dropped_not_german = 0
    count_dropped_not_text_type = 0
    count_dropped_to_short = 0
    count_title_to_content = 0
    
    df = pd.read_csv(f"{g_subreddit_name}.csv")
    df_cleaned = pd.DataFrame(columns=["author", "title", "content", "type"])
    
    print(f"{len(df)} Beiträge aus der Datei {g_subreddit_name}.csv wurden geladen und werden bereinigt")
    
    for index, row in df.iterrows():
        if row["type"] != "text":
            count_dropped_not_text_type += 1
            continue
        
        tmpContent = row["content"]
        
        if pd.isna(row["content"]) or tmpContent == "":
            count_title_to_content += 1
            tmpContent = row["title"]
        
        if is_german(tmpContent, p_english_treshold) == False:
            count_dropped_not_german += 1
            continue
        
        tmpContent = re.sub(r"[^a-zA-ZäöüÄÖÜß0-9\s]", "", tmpContent)
        
        tokens = word_tokenize(tmpContent, language="german")
        cleaned_tokens = []
        
        for index, token in enumerate(tokens):
            if any(char.isdigit() for char in token):
                continue
            
            if re.match(r"^(http|www)", token):
                continue
            
            if token == "":
                continue
            
            if token.lower() in english_words:
                continue
            
            if token.lower() in german_abbr:
                token = german_abbr[token.lower()]
                
            if token.lower() in stopwords:
                continue
            
            for umlaut, replacement in umlaute.items():
                token = token.replace(umlaut, replacement)
            
            token = nlp(token)[0].lemma_
            
            cleaned_tokens.append(token)
        
        tokens = list(filter(None, cleaned_tokens))
        
        if len(tokens) < p_word_treshold:
            count_dropped_to_short += 1
            continue
        
        tmpContent = " ".join(tokens)
        
        tmpContent = tmpContent.lower()
        
        df_cleaned = pd.concat([df_cleaned, pd.DataFrame([{
            "author": row["author"],
            "title": row["title"],
            "content": tmpContent,
            "type": row["type"]
        }])], ignore_index=True)
    
    print()
    print(f"{count_dropped_not_text_type} Beiträge wurden gelöscht, da sie nicht vom Typ 'text' sind")
    print(f"{count_dropped_not_german} Beiträge wurden gelöscht, da sie zu viele englische Wörter enthalten und somit als nicht deutschsprachig eingestuft wurden")
    print(f"{count_dropped_to_short} Beiträge wurden gelöscht, da sie weniger als {p_word_treshold} Wörter enthalten")
    print(f"{count_title_to_content} Beiträge haben keinen Inhalt, weswegen der Titel als Inhalt genommen wurde")
    print(f"Verbleibende Beiträge: {len(df_cleaned)}")
    print()
    print(f"{len(df_cleaned)} bereinigte Beiträgen werden in die Datei {g_subreddit_name}_clean.csv geschrieben")
    print("Enthaltene Felder: author, title, content, type")
    print()
    df_cleaned.to_csv(f"{g_subreddit_name}_clean.csv", index=False)