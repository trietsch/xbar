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
            return self.get_uuid() == other.get_uuid()
        except AttributeError:
            return NotImplemented

    def __hash__(self):
        return hash(f'{self.slug}-{self.id}')

    def __post_init__(self):
        self.id = str(self.id) if isinstance(self.id, int) else self.id
        self.overall_status = PullRequestStatus[self.overall_status] if isinstance(self.overall_status,
                                                                                   str) else self.overall_status

    def get_uuid(self):
        return f'{self.slug}-{self.id}'


@dataclass
class PullRequestsOverview(object):
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
        new = list(filter(lambda pr: pr.id not in [_pr.id for _pr in other.prs_to_review], self.prs_to_review))

        new_id_status_pairs = [(_pr.id, _pr.overall_status) for _pr in new]
        current_without_new = filter(lambda pr: (pr.id, pr.overall_status) not in new_id_status_pairs,
                                     self.prs_to_review)

        previous_id_status_pairs = [(_pr.id, _pr.overall_status) for _pr in other.prs_to_review]
        # Consider a PR to be changed if a reviewer's vote has been reset
        changed = list(filter(lambda pr: pr.overall_status == PullRequestStatus.UNAPPROVED and
                                         (pr.id, pr.overall_status) not in previous_id_status_pairs,
                              current_without_new))

        return new, changed

    def store(self, cache_file):
        pickle.dump(self, open(cache_file, 'wb'))

    @staticmethod
    def load_cached(cache_file):
        try:
            return pickle.load(open(cache_file, 'rb'))
        except Exception as e:
            return PullRequestsOverview(list(), list(), None)
