# mongodb+srv://lokfaaddiiv:admin@lokfaaddiiv.pdegaqw.mongodb.net/?retryWrites=true&w=majority
import json
from sys import exit
from datetime import datetime
from mongoengine import EmbeddedDocument, Document, connect
from mongoengine.fields import DateField, EmbeddedDocumentField, ListField, StringField, ReferenceField

connect(host='mongodb+srv://lokfaaddiiv:admin@lokfaaddiiv.pdegaqw.mongodb.net/HW8?retryWrites=true&w=majority')

# -----------------------------------------------------------------


class Author(Document):
    fullname = StringField()
    born_date = DateField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()


# -----------------------------------------------------------------


def normalize(some):
    return some.encode('windows-1251').decode('utf-8')


def str_to_date(date_string: str):
    given_date_format = '%B %d, %Y'
    date_object = datetime.strptime(date_string, given_date_format).date()
    return date_object


def json_to_db():

    with open('authors.json', 'r') as fh:
        authors_doc = json.load(fh)

    with open('quotes.json', 'r') as fh:
        quotes_doc = json.load(fh)

    for author in authors_doc:
        authors = Author(fullname=author['fullname'],
                         born_date=str_to_date(author['born_date']),
                         born_location=author['born_location'],
                         description=author['description'])
        authors.save()

        for quote in quotes_doc:
            if quote['author'] == author['fullname']:
                quotes = Quote(tags=[i for i in quote['tags']],
                               quote=quote['quote'])
                quotes.author = authors
                quotes.save()


def main():

    while True:
        q = input('Input your request or "quit" to exit: ')
        if q == 'quit':
            exit('Bye!')
        raw = q.split(': ')
        if raw[0] == 'name':
            id_of = Author.objects(fullname=raw[1])[0].id
            q_list = Quote.objects(author=id_of)
            for i in q_list:
                print(normalize(i.quote))
        elif raw[0] == 'tag':
            q_list = Quote.objects(tags__=raw[1])
            for i in q_list:
                print(normalize(i.quote))
        elif raw[0] == 'tags':
            result = set()
            t_list = raw[1].split(',')
            for t in t_list:
                for j in Quote.objects(tags__=t):
                    result.add(j)
            for i in result:
                print(normalize(i.quote))


# -----------------------------------------------------------------

if __name__ == '__main__':
    json_to_db()
    main()

