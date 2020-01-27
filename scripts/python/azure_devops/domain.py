import os
import pickle
from pathlib import Path
from typing import List

from azure.devops.v5_1.git import GitPullRequest


class ReviewStatus(object):
    # 10 - approved 5 - approved with suggestions 0 - no vote -5 - waiting for author -10 - rejected
    _votes_mapping = {
        -10: "REJECTED",
        -5: "WAITING_FOR_AUTHOR",
        0: "NO_VOTE",
        5: "APPROVED_WITH_SUGGESTIONS",
        10: "APPROVED"
    }

    REJECTED = "REJECTED"
    WAITING_FOR_AUTHOR = "WAITING_FOR_AUTHOR"
    NO_VOTE = "NO_VOTE"
    APPROVED_WITH_SUGGESTIONS = "APPROVED_WITH_SUGGESTIONS"
    APPROVED = "APPROVED"

    @staticmethod
    def get_review_status(vote: int):
        return ReviewStatus._votes_mapping[vote]


class AzureDevOpsIcons(object):
    AZURE_DEVOPS = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAACXBIWXMAAAsTAAALEwEAmpwYAAABWWlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS40LjAiPgogICA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyI+CiAgICAgICAgIDx0aWZmOk9yaWVudGF0aW9uPjE8L3RpZmY6T3JpZW50YXRpb24+CiAgICAgIDwvcmRmOkRlc2NyaXB0aW9uPgogICA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgpMwidZAAAChUlEQVQ4EY1SS0hUURj+zn3MaDPiA3GhI1kQ1C0pKNq1chNt2qQURdCmRdBKsVsuvDtD2kQEYauo1bhtEwkSbRVLnUkRYooopKmmuY7zuI/Td+51DG3Tgfs43//9r+//gf3HmTci6F7uFOzVZ3ByXdFdSoGmrelDLCY7UsPXRR29pwM4wo/svl9Eqvs6qqWLsFdsCPGEuA/FtSAwIgJijDqc1TE7EjSDYux9D8zEWUj/MiAuEU/iQCew/SsPIe9gavDlLnd0oVtEl4n1PoT+FUg5xPs5Zk5BTwBehTkb/FZdBisDco6558khFxn+9wmMr7VB8/PoGsiQCLibkoQ1PqsM+I6Oi5BBDtMnvxAD7NwoOjMP8PsbLxIGnbPMmMGPwlMILQuEH9EyWKAWYeTQfDnSiPSRYQOVn6T5dZpMBjDOo7ENaOI5pqy3TT6yUsfcooZelxW9CSly3K6mCehKe9qZ0WAkD0bSJEKleJxcAo7lRSoDf8V1JrXIvu+lQJaq2t4Zn2XRSSjgv46BRCrJeTJMEJeYL5hcmPg/913i+LDEJDPM7LSwL6yBxtYLBrnGKmLRnEO1PZxZ3hz1OHE7YSiigjlDfrlI6thLAxDJIcY4yOo/ES5BhEXeyzBaSqhuudDTdUwfdbnet9Da8ZgbWqOGLQI3F0zMnPHgLHWgZn5Guqct2gfVVq2stKgzWY3ZOCpZpD7txPphtmrkVeIKbm8k8ehIHeMrx6DreWbeJMlDa3sGITtTC6Y6VOMLPC53msHdAkJ5IR6Nclbjmx78QDEn6LyB+yf6US3fQMN9FY1aOalgyTYQf4162Yr4JP977OWre0B7+TDuroxxjdf5PNy1cTv/AISCCLMovX8qAAAAAElFTkSuQmCC"

    PULL_REQUEST = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAVCAYAAABPPm7SAAAAAXNSR0IArs4c6QAAAAlwSFlzAAALEwAACxMBAJqcGAAAAVlpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KTMInWQAAAbVJREFUOBGNlD0ohVEYxw/XZ4muiZHFbMFgllLKJKuFYlAWm0ExKCmT3WBS7qyLO8soE5uPRVEGHxf/33H+b++te+Nfv/s85/l6zznvvTeE+mpWuC2lpmSnk0+sKfk1ZlGritgTxVxmTP63mMnFcAv59ZYWFJXEm7gRaFx8CXK7YlZMCCsbQsFqig7I0rQvXgQ5hmLNpfxBgQqclUQ/K6lPcMY78SzqaVjBU9ElqhQsCYaUBU87E2hIPAly64LGA+FjrcnPdCSPQrZdzKIh+EhzKdYr66GHxFpS4jVZBvg1dci/FSPCQ6lnl4gHZgM8COsB7yl/QWESZ+beMnkRpymKtU/Rp6DGryyfiw/yAIobyZdWN/+fAXUbHfQAnxtr3zV563piNUf4SFWcmS03EjlqULSe2P0bCz2yvrD8TuxjXcs3MWpFn9xuWfDqzkVebiZ2Iqihlp5lEZ1tHIkvDYlJFlKr8I74JZIbFYieqo/wGEMhPCTbnizGO+hMsftkqY39G3KYXBJs70q4CeuHsJNrwYUfC3o2RdS8PjnXjvAluZEC+/wm+NeqiAUR5ad5jXXDX7HwA+nmXWV5F/zGAAAAAElFTkSuQmCC"

    STATUS = {
        ReviewStatus.REJECTED: "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAAPRJREFUOBGlU0EOgjAQHKrxGXyAxEdwMPEfXrz6EG+Ei/8w4cAjTPwAzzARnSlthMYainspu7Mz25ZphiDuQPEEDhmwI5Q7uHsBzQq4FABbPsG+IVjdkHhm4chm4+vjlVhPrKbQiUIPYVbAka/MyzHhx3dLkb1E7CRNTiBLt3QcZDpzD9xi247tQsfh9O1aF8amr2eOkVXXQHENlXTbi0JcTfa/aolInrz1cIoEurCYkHeGl9EkECat4v79G428TaV6Ij0jEUdce4nyNjntDJ5vkZXFGQwkT8vbzCs5zHeFq8Mq/w6EszYNWVsOk0mIeI9En/MbQHpAGFjPgP0AAAAASUVORK5CYII=",
        ReviewStatus.WAITING_FOR_AUTHOR: "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAfElEQVQ4T2NkQAOpqanasxxmX0EXB/HTDqTqzJ49+yqyHCOMExoayrYqYPVPbBrRxcI2hLKvXr36F0gcbAApmmGGwQwBG/B/KcN/YmxGV8MYzcDIiM/PhAwFhQkjubbDDB81gIGB8jCgOBopTkhUScqkGoKRmZCTLKnZGQCX5FCXyXSbYwAAAABJRU5ErkJggg==",
        ReviewStatus.NO_VOTE: "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAQhJREFUOBFjZEADqamp2oyMjClAYTcgloNKPwLSu/7//z9n9uzZV6FiYIoRxgkNDWUTFBTsA/IzgZgJJo5G/wPyp79//75o9erVv0ByYANAmgUEBLYDbXZC04CVC3TJvg8fPniCDAHbBLKZWM1gW4EWQV3LwAj18yWgBC5nY3UFUPAf0CV6TNAAI1UzyFCwXpBGUGiTC9xABsCiihxD5MhxOopFIAMeoYiQxnkEMmAXaXpQVO9iAiVPoBAohZEKQNE4hwmatqeTqhuofjpILzgQQWkblDyJNQSkFqQHpJ4ZRFy7du2vsrLyCk5OTiEg1wSI4ZkMJI8EQF6dBswHcSiZCUkBA6nZGQBHemGgvqxYAAAAAABJRU5ErkJggg==",
        ReviewStatus.APPROVED_WITH_SUGGESTIONS: "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAARlJREFUOBGVk7FtAkEQRf8MyKGRIKcBJFfgyAGWC6ADElIKQMgFkFlO3IELsCAgcgVINOAcJAgR3DJ/zKGT2V2dN7nT/HkzO7t/BX/W6/dz71RgGIA+Qui6LPIjwKKh+Jg8ztdVxOK/a7oe3BXb/QwBoxCClvHqV0QKCN61fT+e9j4P1LwA4dNm92XwUxVI/guWjU7rhUW806VzPZhVrZEz9iuc+Vhgldp2ahccp6l4UD+wxMwpmHE2JKt+2rnMjEZWr1eVSUxKds3R60oCEUFhJonE64WMVTqsXvZtFlmlPd1ht3o2QoasurfNntnsmGgMWT9EettMvYzlRWOW64yJXoCeprdF5S03DjXmlO+Axa+vsez03+d8BpC2a0RVWrdkAAAAAElFTkSuQmCC",
        ReviewStatus.APPROVED: "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAARlJREFUOBGVk7FtAkEQRf8MyKGRIKcBJFfgyAGWC6ADElIKQMgFkFlO3IELsCAgcgVINOAcJAgR3DJ/zKGT2V2dN7nT/HkzO7t/BX/W6/dz71RgGIA+Qui6LPIjwKKh+Jg8ztdVxOK/a7oe3BXb/QwBoxCClvHqV0QKCN61fT+e9j4P1LwA4dNm92XwUxVI/guWjU7rhUW806VzPZhVrZEz9iuc+Vhgldp2ahccp6l4UD+wxMwpmHE2JKt+2rnMjEZWr1eVSUxKds3R60oCEUFhJonE64WMVTqsXvZtFlmlPd1ht3o2QoasurfNntnsmGgMWT9EettMvYzlRWOW64yJXoCeprdF5S03DjXmlO+Axa+vsez03+d8BpC2a0RVWrdkAAAAAElFTkSuQmCC"
    }


class PullRequestsOverview(object):
    CACHE_PATH = os.path.abspath(str(Path.home().absolute()) + '/Library/Caches/nl.robintrietsch.bitbar')
    CACHE_FILE = f'{CACHE_PATH}/azure_devops-last-pr-status'

    def __init__(self, _prs_to_review: List[GitPullRequest], _prs_authored_with_work: List[GitPullRequest], _exception):
        self.prs_to_review: List[GitPullRequest] = _prs_to_review
        self.prs_authored_with_work: List[GitPullRequest] = _prs_authored_with_work
        self.exception = _exception

    def determine_new_pull_requests_to_review(self, other):
        current = [_pr.pull_request_id for _pr in self.prs_to_review]
        previous = [_pr.pull_request_id for _pr in other.prs_to_review]
        new = set(current) - set(previous)

        return [_pr for _pr in self.prs_to_review if _pr.pull_request_id in new]

    def store(self):
        if not os.path.exists(PullRequestsOverview.CACHE_PATH):
            os.makedirs(PullRequestsOverview.CACHE_PATH)

        pickle.dump(self, open(PullRequestsOverview.CACHE_FILE, 'wb'))

    @staticmethod
    def load_cached():
        try:
            return pickle.load(open(PullRequestsOverview.CACHE_FILE, 'rb'))
        except Exception as e:
            return PullRequestsOverview(list(), list(), None)
