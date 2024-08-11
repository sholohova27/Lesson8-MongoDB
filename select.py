import redis
import json
from models import Author, Quote
from mongoengine import connect

# кеширование
r = redis.Redis(host='localhost', port=6379)



def search_by_name(name):
    key = f"name:{name}"
    cached_result = r.get(key)

    if cached_result:
        quotes = json.loads(cached_result.decode('utf-8'))
    else:
        authors = Author.objects(fullname__icontains=name)
        quotes = [{"quote": quote.quote, "author": quote.author.fullname} for quote in
                  Quote.objects(author__in=authors)]
        if quotes:
            r.set(key, json.dumps(quotes), ex=3600)  # Кэш на 1 час

    for quote in quotes:
        print(f"{quote['quote']} - {quote['author']}")


def search_by_tag(tag):
    key = f"tag:{tag}"
    cached_result = r.get(key)

    if cached_result:
        quotes = json.loads(cached_result.decode('utf-8'))
    else:
        quotes = [{"quote": quote.quote, "author": quote.author.fullname} for quote in
                  Quote.objects(tags__icontains=tag)]
        if quotes:
            r.set(key, json.dumps(quotes), ex=3600)  # Кэш на 1 час

    for quote in quotes:
        print(f"{quote['quote']} - {quote['author']}")


def search_by_tags(tags):
    key = f"tags:{tags}"
    cached_result = r.get(key)

    if cached_result:
        quotes = json.loads(cached_result.decode('utf-8'))
    else:
        tags_list = tags.split(',')
        quotes = [{"quote": quote.quote, "author": quote.author.fullname} for quote in
                  Quote.objects(tags__in=tags_list)]
        if quotes:
            r.set(key, json.dumps(quotes), ex=3600)  # Кэш на 1 час

    for quote in quotes:
        print(f"{quote['quote']} - {quote['author']}")


if __name__ == "__main__":
    connect(
        db='nataly-db',
        host='mongodb+srv://nataly-db:Y2FAaVc9S4eiADtz@cluster0.d0plr.mongodb.net/nataly-db?retryWrites=true&w=majority',
        appname='Cluster0'
    )

    while True:
        command = input("Enter command: ")
        if command.startswith("name:"):
            search_by_name(command[len("name:"):].strip())
        elif command.startswith("tag:"):
            search_by_tag(command[len("tag:"):].strip())
        elif command.startswith("tags:"):
            search_by_tags(command[len("tags:"):].strip())
        elif command == "exit":
            break

