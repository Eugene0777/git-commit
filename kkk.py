import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

TWEETS_FILE = "all_tweets_min.json"
LEADERBOARD_FILE = "leaderboard.json"


def load_tweets():
    with open(TWEETS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def build_leaderboard(tweets):
    leaderboard = {}

    for t in tweets:
        user = t.get("user", {})
        username = user.get("screen_name") or user.get("name")
        if not username:
            continue

        # Создаём запись, если её ещё нет
        stats = leaderboard.setdefault(username, {
            "posts": 0,
            "likes": 0,
            "retweets": 0,
            "comments": 0,
            "quotes": 0,       # у тебя нет quotes— ок, будет 0
            "views": 0
        })

        stats["posts"] += 1
        stats["likes"] += t.get("favorite_count", 0)
        stats["retweets"] += t.get("retweet_count", 0)
        stats["comments"] += t.get("reply_count", 0)
        stats["quotes"] += t.get("quote_count", 0) if "quote_count" in t else 0
        stats["views"] += t.get("views_count", 0)

    # Превращаем в список формата:
    # [ ["username", {stats}], ["username2", {stats}], ... ]
    leaderboard_list = [[user, stats] for user, stats in leaderboard.items()]

    return leaderboard_list


if __name__ == "__main__":
    tweets = load_tweets()
    leaderboard = build_leaderboard(tweets)
    save_leaderboard(leaderboard)

    logging.info(f"🏆 Leaderboard построен: {len(leaderboard)} пользователей.")
