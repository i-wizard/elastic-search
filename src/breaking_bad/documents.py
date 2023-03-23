from elasticsearch_dsl import Document, Date, Text
from elasticsearch_dsl.connections import connections
from .models import Character

connections.create_connection()

class CharacterIndex(Document):
    first_name = Text()
    last_name = Text()
    created_at = Date()

    class Index:
        name = 'character'

    class Django:
        model = Character