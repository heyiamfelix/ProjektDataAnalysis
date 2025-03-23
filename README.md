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

# Ergebnisse

## LSA mit BoW (analyze_result_bow.txt)
| Thema | Coherence Wert | Wörter | Vermutetes Thema |
|-|-|-|-|
| Thema 0 | 0.6321 | duisburg, impfung, finden, uhr, marientor, eintragen, kollege, kommen, standort, impfunge | Impfungen |
| Thema 1 | 0.5207 | jemand, gerne, duisburg, geben, jahr, gehen, suchen, zusammen, impfung, schon | Soziale Kontakte / Impfungen |
| Thema 2 | 0.3171 | duisburg, jemand, kommen, monat, geben, zurueck, zimmer, machen, uhr, packen | Wohnungssuche |
| Thema 3 | 0.3167 | duisburg, zimmer, jemand, gehen, monat, umgebung, marburg, suchen, uhr, schon | Wohnungssuche |
| Thema 4 | 0.6311 | duisburg, zurueck, typ, usw, danach, scheinen, packen, monat, fragen, euro   | Rückkehr / Alltag / Kosten |

## LDA mit BoW (analyze_result_bow.txt)
| Thema | Coherence Wert | Wörter | Vermutetes Thema |
|-|-|-|-|
| Thema 0 | 0.6479 | duisburg, jemand, zusammen, gut, suchen, gehen, geben, jahr, gerne, waere | Gemeinschaft / Treffen |
| Thema 1 | 0.5146 | jemand, duisburg, gerne, geben, gut, gehen, schon, jahr, leider, finden | Kontakte |
| Thema 2 | 0.2497 | duisburg, finden, impfung, zeit, geben, schon, suchen, uhr, marientor, kaufen | Impfungen / Termine |
| Thema 3 | 0.3043 | duisburg, finden, jemand, neu, impfung, zusammen, suchen, uhr, frage, gut | Impfungen |
| Thema 4 | 0.4402 | duisburg, jemand, zusammen, geben, gehen, gerne, weiss, werden, leider, kommen | Kommunikation / Treffen |

## LSA mit TF-IDF (analyze_result_tfidf.txt)
| Thema | Coherence Wert | Wörter | Vermutetes Thema |
|-|-|-|-|
| Thema 0 | 0.5046 | impfung, duisburg, uhr, finden, marientor, eintragen, kollege, standort, jemand, apotheke | Impfungen / Termine |
| Thema 1 | 0.2658 | impfung, jemand, marientor, gut, gerne, kollege, zusammen, eintragen, uhr, standort | Impfungen |
| Thema 2 | 0.3247 | jemand, weiss, gut, sagen, gehoert, moechten, kennt, neu, freuen, jahr | Fragen und Empfehlungen |
| Thema 3 | 0.3196 | weiss, gut, suchen, zugaenglich, frei, vielen, bzw, schauen, voraus, willkommen | Zugänglichkeit / Informationen |
| Thema 4 | 0.3723 | schauen, sagen, gehoert, duisser, gehen, neu, erfahrung, empfehlen, schon, stadtteil | Stadtteile |

## LDA mit TF-IDF (analyze_result_tfidf.txt)
| Thema | Coherence Wert | Wörter | Vermutetes Thema |
|-|-|-|-|
| Thema 0 | 0.4600 | duisburg, weiss, jemand, wg, gut, suchen, leute, vielen, finden, kennt | WG-Suche |
| Thema 1 | 0.4384 | donnerstag, duisburg, warum, sagen, neu, gehoert, warnsiren, erfahrung, landschaftspark, gehen | Veranstaltungen |
| Thema 2 | 0.3179 | jemand, duisburg, geben, impfung, ganz, beispiel, sagen, gehen, highfield, ja | Impfungen / Konzerte |
| Thema 3 | 0.3442 | duisburg, jemand, kurz, umgebung, schoen, zusammen, schauen, hochfeld, essen, machen | Kommunikation / Treffen |
| Thema 4 | 0.3819 | gut, jemand, zusammen, suchen, finden, tipp, neu, geben, duisburg, lassen | Tipps und Hilfe |
