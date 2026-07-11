from app.repositories.conversation_repository import ConversationRepository

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
    
    