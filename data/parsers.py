from flask_restful import reqparse


manga_parser = reqparse.RequestParser()
manga_parser.add_argument('name', required=True)
manga_parser.add_argument('author', required=True)
manga_parser.add_argument('painter', required=True)
manga_parser.add_argument('translate', required=True)
manga_parser.add_argument('date_of_release', required=True)
manga_parser.add_argument('translators', required=True)
manga_parser.add_argument('description', required=True)
manga_parser.add_argument('apikey', required=True)

genre_parser = reqparse.RequestParser()
genre_parser.add_argument('name_of_genre', required=True)
genre_parser.add_argument('description', required=True)
manga_parser.add_argument('apikey', required=True)