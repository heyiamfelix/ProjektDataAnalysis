import configparser
import gensim
import gensim.corpora as corpora
from gensim.models import CoherenceModel, LdaMulticore, LsiModel
from nltk.tokenize import word_tokenize
import pandas as pd
import multiprocessing as mp


def count_submission_types(df):
    submission_type_count = df["type"].value_counts().to_dict()
    return submission_type_count


def count_submission_authors(df):
    submission_author_count = df["author"].value_counts().to_dict()
    return submission_author_count


def compute_coherence(args):
    topic_id, word_list, tokenized_texts, dictionary = args
    topic_words = [word for word, _ in word_list]
    coherence = CoherenceModel(topics=[topic_words], texts=tokenized_texts, dictionary=dictionary, coherence="c_v", processes=1).get_coherence()
    return {"topic_id": topic_id, "words": topic_words, "coherence": coherence}


def lsa(df, n_topics, vectorization_method):
    tokenized_texts = [word_tokenize(text, language="german") for text in df["content"]]
    
    dictionary = corpora.Dictionary(tokenized_texts)
    
    if vectorization_method == "bow":
        corpus = [dictionary.doc2bow(tokens) for tokens in tokenized_texts]
    elif vectorization_method == "tfidf":
        bow_corpus = [dictionary.doc2bow(tokens) for tokens in tokenized_texts]
        tfidf = gensim.models.TfidfModel(bow_corpus)
        corpus = tfidf[bow_corpus]
    else:
        raise ValueError("Inkorrekte Vektorisierungsmethode, 'bow' oder 'tfidf' zulässig")
    
    lsa_model = LsiModel(corpus, num_topics=n_topics, id2word=dictionary)
    topics = lsa_model.show_topics(num_topics=n_topics, num_words=10, formatted=False)
    
    with mp.get_context("spawn").Pool(processes=mp.cpu_count() - 1) as pool:
        topic_coherences = pool.map(compute_coherence, [(tid, wlist, tokenized_texts, dictionary) for tid, wlist in topics])
    
    return topic_coherences


def lda(df, n_topics, vectorization_method):
    tokenized_texts = [word_tokenize(text, language="german") for text in df["content"]]
    
    dictionary = corpora.Dictionary(tokenized_texts)
    
    if vectorization_method == "bow":
        corpus = [dictionary.doc2bow(tokens) for tokens in tokenized_texts]
    elif vectorization_method == "tfidf":
        bow_corpus = [dictionary.doc2bow(tokens) for tokens in tokenized_texts]
        tfidf = gensim.models.TfidfModel(bow_corpus)
        corpus = tfidf[bow_corpus]
    else:
        raise ValueError("Inkorrekte Vektorisierungsmethode, 'bow' oder 'tfidf' zulässig")
    
    lda_model = LdaMulticore(corpus, num_topics=n_topics, id2word=dictionary, workers=mp.cpu_count() - 1)
    topics = lda_model.show_topics(num_topics=n_topics, num_words=10, formatted=False)
    
    with mp.get_context("spawn").Pool(processes=mp.cpu_count() - 1) as pool:
        topic_coherences = pool.map(compute_coherence, [(tid, wlist, tokenized_texts, dictionary) for tid, wlist in topics])
    
    return topic_coherences


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.cfg")
    
    n_topics = int(config["ANALYSE"]["n_topics"])
    subreddit_name = str(config["GLOBAL"]["subreddit"])
    vectorization_method = str(config["ANALYSE"]["vectorization_method"]).lower()
    
    df = pd.read_csv(f"{subreddit_name}.csv")
    df_cleaned = pd.read_csv(f"{subreddit_name}_clean.csv")
    
    print(f"{len(df)} Beiträge aus der Datei {subreddit_name}.csv wurden geladen")
    print(f"{len(df_cleaned)} Beiträge aus der Datei {subreddit_name}_clean.csv wurden geladen")
    print()
    
    print("Beitrags-Typen und -Autoren werden analysiert")
    submission_type_count = count_submission_types(df)
    submission_author_count = count_submission_authors(df)
    
    print("LSA Analyse wird durchgeführt")
    submission_lsa_topics_with_coherences = lsa(df_cleaned, n_topics, vectorization_method)
    
    print("LDA Analyse wird durchgeführt")
    submission_lda_topics_with_coherences = lda(df_cleaned, n_topics, vectorization_method)
    
    print()
    print(f"------------------ ERGEBNISSE (mit der Vektorisierungsmethode '{vectorization_method}') ------------------")
    print()
    print("Beitrags-Typen nach Häufigkeit:")
    for type, count in submission_type_count.items():
        print(f"{type}: {count}")
    
    print()
    print("Häufigste Beitrags-Autoren:")
    for author, count in sorted(submission_author_count.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"{author}: {count}")
    
    print()
    print("LSA Themen mit Coherence-Werten:")
    for topic in submission_lsa_topics_with_coherences:
        print(f"Thema {topic['topic_id']}: {topic['words']} - Coherence: {topic['coherence']}")
    
    print()
    print("LDA Themen mit Coherence-Werten:")
    for topic in submission_lda_topics_with_coherences:
        print(f"Thema {topic['topic_id']}: {topic['words']} - Coherence: {topic['coherence']}")
    print()