import json
from mongoengine import connect
from models import Author, Quote

try:
    connect(
        db='nataly-db',
        username='nataly-db',
        password='Y2FAaVc9S4eiADtz',
        host='mongodb+srv://cluster0.d0plr.mongodb.net',
        ssl=True
    )
    print("Connected to MongoDB")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit(1)

def load_authors(authors_file):
    with open(authors_file, 'r', encoding='utf-8') as file:
        authors = json.load(file)
        for author_data in authors:
            author = Author(**author_data)
            author.save()
            print(f"Saved author: {author.fullname}")

def load_quotes(quotes_file):
    with open(quotes_file, 'r', encoding='utf-8') as file:
        quotes = json.load(file)
        for quote_data in quotes:
            author_name = quote_data.pop('author')
         # objects - это высокоуровневый аналог find (find возвращает курсор и требует доп обработки)
            author = Author.objects(fullname=author_name).first()
            if author:
                quote = Quote(author=author, **quote_data)
                quote.save()
                print(f"Saved quote: {author.fullname}")

if __name__ == "__main__":
    load_authors('authors.json')
    load_quotes('quotes.json')
