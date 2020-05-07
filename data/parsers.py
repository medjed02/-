from flask_restful import reqparse


manga_parser = reqparse.RequestParser()
manga_parser.add_argument('name')
manga_parser.add_argument('author')
manga_parser.add_argument('painter')
manga_parser.add_argument('translate')
manga_parser.add_argument('date_of_release')
manga_parser.add_argument('translators')
manga_parser.add_argument('description')
manga_parser.add_argument('apikey', required=True)

genre_parser = reqparse.RequestParser()
genre_parser.add_argument('name_of_genre')
genre_parser.add_argument('description')
manga_parser.add_argument('apikey', required=True)

chapter_parser = reqparse.RequestParser()
chapter_parser.add_argument('name')
chapter_parser.add_argument('content')
chapter_parser.add_argument('number', type=int)
chapter_parser.add_argument('apikey', required=True)

delete_parser = reqparse.RequestParser()
delete_parser.add_argument('apikey', required=True)