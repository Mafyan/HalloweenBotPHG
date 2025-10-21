"""
Работа с базой данных
"""
import sqlite3
from datetime import datetime
from typing import Optional, List, Dict
import json

class Database:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_file)
    
    def init_db(self):
        """Инициализация базы данных"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                club TEXT NOT NULL,
                phone TEXT NOT NULL,
                photo_file_id TEXT NOT NULL,
                status TEXT DEFAULT 'SUBMITTED',
                moderator_message_id INTEGER,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                moderated_at TIMESTAMP,
                moderator_user_id INTEGER
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bot_state (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_submission(self, user_id: int, username: str, first_name: str, 
                       last_name: str, club: str, phone: str, photo_file_id: str) -> int:
        """Добавить новую заявку"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO submissions 
            (user_id, username, first_name, last_name, club, phone, photo_file_id, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'SUBMITTED')
        """, (user_id, username, first_name, last_name, club, phone, photo_file_id))
        
        submission_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return submission_id
    
    def update_moderator_message(self, submission_id: int, message_id: int):
        """Сохранить ID сообщения модератора"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE submissions 
            SET moderator_message_id = ?
            WHERE id = ?
        """, (message_id, submission_id))
        
        conn.commit()
        conn.close()
    
    def update_submission_status(self, submission_id: int, status: str, 
                                  moderator_user_id: int):
        """Обновить статус заявки"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE submissions 
            SET status = ?, 
                moderated_at = CURRENT_TIMESTAMP,
                moderator_user_id = ?
            WHERE id = ?
        """, (status, moderator_user_id, submission_id))
        
        conn.commit()
        conn.close()
    
    def get_submission(self, submission_id: int) -> Optional[Dict]:
        """Получить заявку по ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, user_id, username, first_name, last_name, club, 
                   phone, photo_file_id, status, moderator_message_id,
                   submitted_at, moderated_at, moderator_user_id
            FROM submissions
            WHERE id = ?
        """, (submission_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'user_id': row[1],
                'username': row[2],
                'first_name': row[3],
                'last_name': row[4],
                'club': row[5],
                'phone': row[6],
                'photo_file_id': row[7],
                'status': row[8],
                'moderator_message_id': row[9],
                'submitted_at': row[10],
                'moderated_at': row[11],
                'moderator_user_id': row[12]
            }
        return None
    
    def get_approved_submissions(self) -> List[Dict]:
        """Получить все одобренные заявки"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, user_id, username, first_name, last_name, club, 
                   phone, photo_file_id, status, submitted_at
            FROM submissions
            WHERE status = 'APPROVED'
            ORDER BY submitted_at ASC
        """, )
        
        rows = cursor.fetchall()
        conn.close()
        
        submissions = []
        for row in rows:
            submissions.append({
                'id': row[0],
                'user_id': row[1],
                'username': row[2],
                'first_name': row[3],
                'last_name': row[4],
                'club': row[5],
                'phone': row[6],
                'photo_file_id': row[7],
                'status': row[8],
                'submitted_at': row[9]
            })
        
        return submissions
    
    def delete_rejected_photos(self):
        """Удалить отклонённые заявки"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM submissions
            WHERE status = 'REJECTED'
        """)
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count
    
    def set_bot_state(self, key: str, value: str):
        """Установить состояние бота"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO bot_state (key, value)
            VALUES (?, ?)
        """, (key, value))
        
        conn.commit()
        conn.close()
    
    def get_bot_state(self, key: str) -> Optional[str]:
        """Получить состояние бота"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT value FROM bot_state WHERE key = ?
        """, (key,))
        
        row = cursor.fetchone()
        conn.close()
        
        return row[0] if row else None
    
    def get_stats(self) -> Dict:
        """Получить статистику заявок"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM submissions
            GROUP BY status
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        stats = {row[0]: row[1] for row in rows}
        return stats

