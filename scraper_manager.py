"""
Scraper Orchestrator Manager
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
from .models.job import Job
from .scrapers.upsc import UPSCScraper
from .scrapers.drdo import DRDOScraper
from .scrapers.ongc import ONGCScraper
from .scrapers.ntpc import NTPCScraper
from .scrapers.iocl import IOCLScraper
from .scrapers.hpcl import HPCLScraper
from .scrapers.bpcl import BPCLScraper
from .scrapers.gail import GAILScraper
from .scrapers.bhel import BHELScraper
from .scrapers.bel import BELScraper
from .scrapers.isro import ISROScraper
from .scrapers.barc import BARCScraper
from .scrapers.npcil import NPCILScraper
from .scrapers.rrb import RRBScraper
from .scrapers.ssc import SSCScraper
from .scrapers.employment_news import EmploymentNewsScraper
from .utils.logger import scraper_logger


class ScraperManager:

    def __init__(self):
        self.scrapers = [
            UPSCScraper(),
            DRDOScraper(),
            ONGCScraper(),
            NTPCScraper(),
            IOCLScraper(),
            HPCLScraper(),
            BPCLScraper(),
            GAILScraper(),
            BHELScraper(),
            BELScraper(),
            ISROScraper(),
            BARCScraper(),
            NPCILScraper(),
            RRBScraper(),
            SSCScraper(),
            EmploymentNewsScraper()
        ]

    def run_all(self) -> List[Job]:
        all_jobs = []
        scraper_logger.info("Executing %d scrapers concurrently...", len(self.scrapers))

        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_scraper = {
                executor.submit(scraper.scrape): scraper
                for scraper in self.scrapers
            }

            for future in as_completed(future_to_scraper):
                scraper = future_to_scraper[future]
                try:
                    jobs = future.result()
                    if jobs:
                        all_jobs.extend(jobs)
                        scraper_logger.info("[%s] Returned %d jobs.", scraper.name, len(jobs))
                except Exception as e:
                    scraper_logger.error("[%s] Scraper failed with exception: %s", scraper.name, e)

        return all_jobs
