# Systemanforderungen
Die folgenden Anforderungen wurden getestet, andere Konfigurationen könnten ebenfalls funktionieren, jedoch wird hierfür keine Garantie übernommen.<br><br>
Windows 11<br>
Python 3.12.6<br>

# Installation
Erstelle eine neue virtuelle Umgebung:
```cmd
python -m venv virtual
```

Aktiviere die virtuelle Umgebung:
```cmd
virtual\Scripts\activate
```

Installiere die benötigten Bibliotheken:
```cmd
pip install -r requirements.txt
```

Lade das benötigte spaCy-Modell herunter:
```cmd
python -m spacy download de_core_news_md
```

# Ausführung

Verbinde dich mit der Reddit-API und speichere die Daten in einer .csv-Datei:
```cmd
python download.py
```

Daten vorbereiten und in einer weiteren .csv-Datei speichern:
```cmd
python prepare.py
```

Analysiere die Daten und gebe die Ergebnisse aus:
```cmd
python analyze.py
```

# Konfiguration
Die Konfiguration erfolgt über die Datei `config.cfg`. Hier können die folgenden Parameter angepasst werden:
```cfg
[GLOBAL]
subreddit= # Name des Subreddits, innerhalb dieses Projekts "duisburg"

[REDDIT]
client_id= # Client-ID des Reddit-Entwicklerkontos
client_secret= # Client-Secret des Reddit-Entwicklerkontos
user_agent= # User-Agent zum senden von Anfragen an die Reddit-API

[PREPARE]
english_treshold= # Prozentualer Anteil der englischen Wörter in einem Text ab dem dieser als englisch betrachtet wird
word_treshold= # Minimale Anzahl an Wörtern in einem Text

[ANALYSE]
n_topics= # Anzahl der zu erstellenden Themen
vectorization_method= # Verwendete Methode zur Vektorisierung der Texte, "tfidf" oder "bow"
```
