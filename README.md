# Systemanforderungen
Die folgenden Anforderungen wurden getestet, andere Konfigurationen könnten ebenfalls funktionieren, jedoch wird hierfür keine Garantie übernommen.<br><br>
Windows 11<br>
Python 3.12.6<br>

# Herunterladen des Projekts

Option 1: Herunterladen des Projekts als ZIP-Datei<br>
Klicke auf den grünen "Code"-Button in GitHub und wähle "Download ZIP". Entpacke anschließend das heruntergeladene ZIP Verzeichnis<br><br>
Option 2: Klonen des Projekts mit Git<br>
Öffne die Kommandozeile und führe den folgenden Befehl aus:
```cmd
git clone https://github.com/heyiamfelix/ProjektDataAnalysis.git
```
Option 3: Herunterladen des Projekts mit dem Tool GitHub CLI<br>
Öffne die Kommandozeile und führe den folgenden Befehl aus:
```cmd
gh repo clone heyiamfelix/ProjektDataAnalysis
```

# Installation

Öffne eine neue Eingabeaufforderung und navigiere in das Verzeichnis des Projekts.<br><br>

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
Im Anschluss können die folgenden Skripte ausgeführt werden (es wird die Eingabeaufforderung aus den Installationsschritten benötigt):<br><br>

download.py: Verbindet sich mit der Reddit-API und lädt die Daten herunter und speichert diese in einer .csv-Datei<br>
```cmd
python download.py
```

prepare.py: Bereitet die Daten auf, indem sie bereinigt und in einer weiteren .csv-Datei gespeichert werden<br>
```cmd
python prepare.py
```

analyze.py: Analysiert die Daten und erstellt Themen, die Ausgabe erfolgt in der Konsole<br>
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
