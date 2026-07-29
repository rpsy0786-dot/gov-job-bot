"""
Job Processing Pipeline
"""

from typing import List
from .models.job import Job
from .models.profile import Profile
from .utils.ai_classifier import AIClassifier
from .utils.job_ranker import JobRanker
from .utils.validators import JobValidator
from .utils.duplicate_detector import DuplicateDetector


class JobPipeline:

    def __init__(self, database, notifier):
        self.database = database
        self.notifier = notifier
        self.profile = Profile()

    def process(self, jobs: List[Job]) -> List[Job]:
        if not jobs:
            return []

        # 1. AI Classification
        classified_jobs = [AIClassifier.classify(job) for job in jobs]

        # 2. Ranking against User Profile
        ranked_jobs = JobRanker.rank(classified_jobs, self.profile)

        # 3. Retrieve Existing Jobs from Database for Duplicate Filtering
        existing_jobs = self.database.get_all_jobs()
        existing_hashes = {
            DuplicateDetector.generate_hash(job)
            for job in existing_jobs
        }

        # 4. Remove Duplicates
        unique_jobs = DuplicateDetector.filter_new_jobs(
            ranked_jobs,
            existing_jobs,
            existing_hashes
        )

        # 5. Validation
        final_jobs = []
        for job in unique_jobs:
            valid, errors = JobValidator.validate(job)
            if valid:
                final_jobs.append(job)

        # 6. Save to DB
        for job in final_jobs:
            self.database.insert_job(job)

        # 7. Notify via Telegram
        if final_jobs and self.notifier:
            self.notifier.send_jobs(final_jobs)

        return final_jobs
