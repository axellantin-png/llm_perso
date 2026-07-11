from app.repositories.conversation_repository import ConversationRepository
from app.models.conversation import Conversation
from app.models.message import Message

class SQLiteRepository(
    ConversationRepository
):

    def __init__(self, database):

        self.database = database

    def create(self):

        conversation = Conversation()

        connection = self.database.get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO conversations
            (
                id,
                title
            )

            VALUES
            (?, ?)
            """,
            (
                conversation.id,
                conversation.title
            )
        )

        connection.commit()

        connection.close()

        return conversation
    
    def get(self, conversation_id) : 

        connection = self.database.get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, title
            FROM conversations
            WHERE id = ?
            """,
            (conversation_id,)
        )

        conversation_row = cursor.fetchone()

        if conversation_row is None:
            raise ValueError(
        f"Conversation {conversation_id} not found")

        conversation = Conversation()

        conversation.ConversationFromHistory( id=conversation_row["id"],title=conversation_row["title"])

        cursor.execute(
            """
            SELECT role, content

            FROM messages

            WHERE conversation_id = ?

            ORDER BY id
            """,
            (conversation_id,)
        )

        rows = cursor.fetchall()

        for row in rows:

            conversation.messages.append(
                Message(
                    role=row["role"],
                    content=row["content"]
                )
            )
        
        connection.close()

        return conversation
    
