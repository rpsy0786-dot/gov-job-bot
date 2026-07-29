"""
Job Data Model
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Job:
    title: str = ""
    organisation: str = ""
    department: str = ""
    qualification: str = ""
    experience: str = ""
    age_limit: str = ""
    vacancies: str = ""
    salary: str = ""
    location: str = ""
    job_type: str = ""
    advertisement_no: str = ""
    notification_date: str = ""
    last_date: str = ""
    application_mode: str = ""
    apply_link: str = ""
    notification_pdf: str = ""
    description: str = ""
    source: str = ""
    score: float = 0.0
    notified: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        return {
            "title": self.title,
            "organisation": self.organisation,
            "department": self.department,
            "qualification": self.qualification,
            "experience": self.experience,
            "age_limit": self.age_limit,
            "vacancies": self.vacancies,
            "salary": self.salary,
            "location": self.location,
            "job_type": self.job_type,
            "advertisement_no": self.advertisement_no,
            "notification_date": self.notification_date,
            "last_date": self.last_date,
            "application_mode": self.application_mode,
            "apply_link": self.apply_link,
            "notification_pdf": self.notification_pdf,
            "description": self.description,
            "source": self.source,
            "score": self.score,
            "notified": self.notified,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if isinstance(self.created_at, datetime) else str(self.created_at)
        }
