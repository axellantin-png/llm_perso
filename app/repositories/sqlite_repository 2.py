from app.repositories.conversation_repository import ConversationRepository
from app.models.conversation import Conversation
from app.models.message import Message

class SQLiteRepository(
    ConversationRepository
):

    def __init__(self, database):

        self.database = database

    def create(self):

        conversation = Conversation.new()


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
        
        conversation = Conversation.from_database(id=conversation_row["id"],title=conversation_row["title"])

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
    
    def delete(self, conversation_id: str):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        # Si tes clés étrangères ne sont pas configurées en ON DELETE CASCADE,
        # il faut supprimer manuellement les messages liés d'abord.
        cursor.execute(
            "DELETE FROM messages WHERE conversation_id = ?",
            (conversation_id,)
        )
        
        cursor.execute(
            "DELETE FROM conversations WHERE id = ?",
            (conversation_id,)
        )

        connection.commit()
        connection.close()

    def save(self, conversation: Conversation):
        connection = self.database.get_connection()
        cursor = connection.cursor()

        # 1. Mise à jour des métadonnées de la conversation (comme le titre)
        cursor.execute(
            """
            UPDATE conversations
            SET title = ?
            WHERE id = ?
            """,
            (conversation.title, conversation.id)
        )

        # 2. Synchronisation des messages
        # Pour éviter les doublons ou gérer les ajouts proprement, la méthode 
        # la plus robuste consiste à vider les messages existants de cette 
        # conversation puis à réinsérer la liste actuelle.
        cursor.execute(
            "DELETE FROM messages WHERE conversation_id = ?",
            (conversation.id,)
        )

        for message in conversation.messages:
            cursor.execute(
                """
                INSERT INTO messages (conversation_id, role, content)
                VALUES (?, ?, ?)
                """,
                (conversation.id, message.role, message.content)
            )

        connection.commit()
        connection.close()


    def list(self):

        connection = self.database.get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, title
            FROM conversations
            ORDER BY created_at DESC
            """
        )

        rows = cursor.fetchall()

        connection.close()

        return [
            {
                "id": row["id"],
                "title": row["title"]
            }
            for row in rows
    ]
        
    def rename(self, conversation_id, title):

        connection = self.database.get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE conversations
            SET title = ?
            WHERE id = ?
            """,
            (
                title,
                conversation_id
            )
        )

        connection.commit()

        connection.close()
    
    


