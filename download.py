import configparser
import csv
import praw

image_links = ["i.redd.it", "reddit.com/gallery", "imgur.com"]
video_links = ["v.redd.it", "youtube.com", "youtu.be"]

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.cfg")
    
    r_client_id = str(config["REDDIT"]["client_id"])
    r_client_secret = str(config["REDDIT"]["client_secret"])
    g_subreddit_name = str(config["GLOBAL"]["subreddit"])
    r_user_agent = str(config["REDDIT"]["user_agent"])
    
    if not r_client_id or not r_client_secret or not g_subreddit_name or not r_user_agent:
        print("Alle Felder in der Konfigurationsdatei müssen ausgefüllt sein.")
        exit(1)
    
    reddit = praw.Reddit(
        client_id=r_client_id,
        client_secret=r_client_secret,
        user_agent=r_user_agent
    )
    
    print(f"Laden von maximal 1000 Beiträgen aus dem Subreddit r/{g_subreddit_name}")
    print("(Aufgrund der Begrenzung der Reddit-API können nicht mehr als 1000 Beiträge geladen werden)")

    submission_list = []

    subreddit = reddit.subreddit(g_subreddit_name)
    submissions = subreddit.new(limit=1000)
    for submission in submissions:
        author = ""
        if submission.author:
            author = submission.author.name
        else:
            author = "unknown_or_deleted"
        
        type = ""
        if(submission.is_self):
            type = "text"
        elif any(link in submission.url for link in image_links):
            type = "image"
        elif any(link in submission.url for link in video_links):
            type = "video"
        else:
            type = "link"
        
        submission_list.append({"author": author, "title": submission.title, "content": submission.selftext, "type": type})
    
    for submission in submission_list:
        submission["content"] = submission["content"].replace("\n", " ")
    
    print()
    print(f"{len(submission_list)} Beiträge werden in die Datei {g_subreddit_name}.csv geschrieben")
    print("Enthaltene Felder: author, title, content, type")
    print()

    with open(f"{g_subreddit_name}.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["author", "title", "content", "type"])
        writer.writeheader()
        for submission in submission_list:
            writer.writerow(submission)