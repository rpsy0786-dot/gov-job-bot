"""
Database Persistence Manager
AI Powered Government Jobs Telegram Bot
"""

import sqlite3
from datetime import datetime, date
from typing import List, Optional
from pathlib import Path
from .models.job import Job
from .config import DATABASE_PATH
from .utils.logger import database_logger


class Database:
    """
    SQLite database interface for storing, querying, and filtering jobs.
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or DATABASE_PATH
        self._init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")  # Enable Write-Ahead Logging
        return conn

    def _init_db(self):
        with self.get_connection() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                organisation TEXT NOT NULL,
                department TEXT,
                qualification TEXT,
                experience TEXT,
                age_limit TEXT,
                vacancies TEXT,
                salary TEXT,
                location TEXT,
                job_type TEXT,
                advertisement_no TEXT,
                notification_date TEXT,
                last_date TEXT,
                application_mode TEXT,
                apply_link TEXT UNIQUE,
                notification_pdf TEXT,
                description TEXT,
                source TEXT,
                score REAL DEFAULT 0.0,
                notified INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
            conn.commit()
            database_logger.info("Database initialized successfully at %s", self.db_path)

    def row_to_job(self, row) -> Job:
        job = Job()
        job.title = row["title"] or ""
        job.organisation = row["organisation"] or ""
        job.department = row["department"] or ""
        job.qualification = row["qualification"] or ""
        job.experience = row["experience"] or ""
        job.age_limit = row["age_limit"] or ""
        job.vacancies = row["vacancies"] or ""
        job.salary = row["salary"] or ""
        job.location = row["location"] or ""
        job.job_type = row["job_type"] or ""
        job.advertisement_no = row["advertisement_no"] or ""
        job.notification_date = row["notification_date"] or ""
        job.last_date = row["last_date"] or ""
        job.application_mode = row["application_mode"] or ""
        job.apply_link = row["apply_link"] or ""
        job.notification_pdf = row["notification_pdf"] or ""
        job.description = row["description"] or ""
        job.source = row["source"] or ""
        job.score = float(row["score"] or 0.0)
        job.notified = bool(row["notified"])
        return job

    def insert_job(self, job: Job) -> bool:
        try:
            with self.get_connection() as conn:
                conn.execute("""
                INSERT OR IGNORE INTO jobs (
                    title, organisation, department, qualification, experience, age_limit,
                    vacancies, salary, location, job_type, advertisement_no, notification_date,
                    last_date, application_mode, apply_link, notification_pdf, description,
                    source, score, notified
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """, (
                    job.title, job.organisation, job.department, job.qualification,
                    job.experience, job.age_limit, job.vacancies, job.salary,
                    job.location, job.job_type, job.advertisement_no, job.notification_date,
                    job.last_date, job.application_mode, job.apply_link, job.notification_pdf,
                    job.description, job.source, job.score, 1 if job.notified else 0
                ))
                conn.commit()
                return True
        except Exception as e:
            database_logger.error("Error inserting job %s: %s", job.title, e)
            return False

    def get_all_jobs(self) -> List[Job]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM jobs ORDER BY id DESC")
            return [self.row_to_job(row) for row in cursor.fetchall()]

    def get_today_jobs(self) -> List[Job]:
        today_str = date.today().strftime("%Y-%m-%d")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM jobs WHERE DATE(created_at) = ? ORDER BY score DESC", (today_str,))
            rows = cursor.fetchall()
            if not rows:
                cursor.execute("SELECT * FROM jobs ORDER BY id DESC LIMIT 10")
                rows = cursor.fetchall()
            return [self.row_to_job(row) for row in rows]

    def search_jobs(self, keyword: str) -> List[Job]:
        pattern = f"%{keyword.strip().lower()}%"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT * FROM jobs 
            WHERE LOWER(title) LIKE ? 
               OR LOWER(organisation) LIKE ? 
               OR LOWER(department) LIKE ? 
               OR LOWER(qualification) LIKE ?
            ORDER BY score DESC LIMIT 15
            """, (pattern, pattern, pattern, pattern))
            return [self.row_to_job(row) for row in cursor.fetchall()]

    def get_jobs_by_type(self, job_type: str) -> List[Job]:
        pattern = f"%{job_type.strip().lower()}%"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT * FROM jobs 
            WHERE LOWER(job_type) LIKE ? OR LOWER(organisation) LIKE ?
            ORDER BY score DESC LIMIT 15
            """, (pattern, pattern))
            return [self.row_to_job(row) for row in cursor.fetchall()]

    def total_jobs(self) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM jobs")
            return cursor.fetchone()[0]

    def today_count(self) -> int:
        today_str = date.today().strftime("%Y-%m-%d")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM jobs WHERE DATE(created_at) = ?", (today_str,))
            return cursor.fetchone()[0]

    def total_organisations(self) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(DISTINCT organisation) FROM jobs")
            return cursor.fetchone()[0]
          
