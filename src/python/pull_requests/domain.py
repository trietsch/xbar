import logging
import pickle
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional

PullRequestStatus = Enum('PullRequestStatus',
                         'UNAPPROVED NEEDS_WORK APPROVED REJECTED WAITING_FOR_AUTHOR NO_VOTE APPROVED_WITH_SUGGESTIONS')
PullRequestSort = Enum('PullRequestSort', 'ACTIVITY NAME')


@dataclass
class PullRequestException(object):
    source: str
    message: str
    exception: Exception


@dataclass
class PullRequest(object):
    id: str
    title: str
    slug: str
    from_ref: str
    to_ref: str
    overall_status: PullRequestStatus
    activity: datetime
    time_ago: str
    repo_href: str
    href: str

    def __post_init__(self):
        self.id = str(self.id) if isinstance(self.id, int) else self.id
        self.overall_status = PullRequestStatus[self.overall_status] if isinstance(self.overall_status,
                                                                                   str) else self.overall_status

    def get_uuid(self):
        return f'{self.slug}-{self.id}'


@dataclass
class PullRequestsOverview(object):
    logger = logging.getLogger(__name__)

    prs_to_review: List[PullRequest]
    prs_authored_with_work: List[PullRequest]
    exceptions: List[PullRequestException]

    @classmethod
    def create(cls, prs_to_review, prs_authored_with_work, exception: Optional[PullRequestException]):
        if exception is not None:
            return cls(prs_to_review, prs_authored_with_work, [exception])
        else:
            return cls(prs_to_review, prs_authored_with_work, list())

    def join(self, other):
        self.prs_to_review += other.prs_to_review
        self.prs_authored_with_work += other.prs_authored_with_work
        self.exceptions += other.exceptions

        return self

    def determine_new_pull_requests_to_review(self, other):
        current = [_pr.get_uuid() for _pr in self.prs_to_review]
        previous = [_pr.get_uuid() for _pr in other.prs_to_review]
        new = set(current) - set(previous)

        return [_pr for _pr in self.prs_to_review if _pr.get_uuid() in new]

    def store(self, cache_file):
        pickle.dump(self, open(cache_file, 'wb'))

    @staticmethod
    def load_cached(cache_file):
        try:
            return pickle.load(open(cache_file, 'rb'))
        except Exception as e:
            return PullRequestsOverview(list(), list(), None)
