import logging
import pickle
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional

from ..common.util import zip_list_of_dicts

PullRequestStatus = Enum('PullRequestStatus',
                         'UNAPPROVED NEEDS_WORK APPROVED REJECTED WAITING_FOR_AUTHOR NO_VOTE APPROVED_WITH_SUGGESTIONS')
PullRequestSort = Enum('PullRequestSort', 'ACTIVITY NAME')


@dataclass
class PullRequestException(object):
    source: str
    message: str
    exception: Exception
    traceback: str


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
    all_prs_href: str
    href: str

    def __eq__(self, other):
        try:
            return f'{self.slug}-{self.id}' == f'{other.slug}-{other.id}'
        except AttributeError:
            return NotImplemented

    def __hash__(self):
        return hash(f'{self.slug}-{self.id}')

    def __post_init__(self):
        self.id = str(self.id) if isinstance(self.id, int) else self.id
        self.overall_status = PullRequestStatus[self.overall_status] if isinstance(self.overall_status,
                                                                                   str) else self.overall_status

    def _get_uuid(self):
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

    def determine_new_and_changed_pull_requests_to_review(self, other):
        new = set(self.prs_to_review) - set(other.prs_to_review)

        current = set((pr.id, pr.overall_status) for pr in self.prs_to_review)
        deleted = [(pr.id, pr.overall_status) for pr in (set(other.prs_to_review) - set(self.prs_to_review))]
        changed = [pr for pr in other.prs_to_review if ((pr.id, pr.overall_status) not in current and (pr.id, pr.overall_status) not in deleted)]

        return new, changed

    def store(self, cache_file):
        pickle.dump(self, open(cache_file, 'wb'))

    @staticmethod
    def load_cached(cache_file):
        try:
            return pickle.load(open(cache_file, 'rb'))
        except Exception as e:
            return PullRequestsOverview(list(), list(), None)
