from enum import Enum

from ..common.icons import Icons, Icon

PipelineStatus = Enum('Status', 'SUCCESS FAILURE FAILURE_BUILDING SUCCESS_BUILDING INACTIVE MANUAL ERROR UNKNOWN')
GitlabCiStatus = Enum('CiStatus', 'running pending success failed canceled skipped manual unknown')


class GitlabIcons(object):
    STATUS = {
        PipelineStatus.SUCCESS: Icons.GREEN_CIRCLE_CHECKMARK,
        PipelineStatus.FAILURE: Icons.RED_CIRCLE_CROSS,
        PipelineStatus.FAILURE_BUILDING: Icons.ORANGE_CIRCLE_SYNC,
        PipelineStatus.SUCCESS_BUILDING: Icons.GREEN_CIRCLE_SYNC,
        PipelineStatus.INACTIVE: Icons.GREY_CIRCLE,
        PipelineStatus.MANUAL: Icons.GREY_CIRCLE_PAUSE,
        PipelineStatus.ERROR: Icons.GREY_CIRCLE,
        PipelineStatus.UNKNOWN: Icons.GREY_CIRCLE,
    }

    GITLAB_LOGO = Icon("iVBORw0KGgoAAAANSUhEUgAAABAAAAAOCAYAAAAmL5yKAAAAAXNSR0IArs4c6QAAAi5JREFUKBV1Us9rE1EQnpm3+bFpatMG0tJE6o9YF+JJaIoKRbOlh5YcPBvx7kE8qBQvXvwH/Ac86aV/gBTBm17sWSVNLUYrWg+i2Cab7L43zm6zREIdeDvz3vfN92ZmH8DA9lwn/9l1Hsb7//l2zVnfdy9MxzjFATNVEej+l9p8MT4b9buSSIj3uqwvx9hQgGB13KKcAVWLwVGv2CxlLcojwmqMRQLvrlaywLwSMAMQ1GNw1BNxXQsFGJY/Lp+ZCPFIYMwPFiQodwMDYGDpQ9XJjya3FssnjIaaJxwLcI48+1LIscLPVJXXrJ9MvmaW8qYzB/i0fc35hpG8XCi6dg4K6TEzK3S2FKKeMmvwGjaRN0q26dtb9AkrZh8AFUD/F8HvPQIRiyzsbKJoIDlpgLWUXZBCT3GLUsmLVtBLLxJhRZeE+0cmcQhItuGAELSGSIIIGG0DJpB9RjRKwlF0LvD0FWJDHbnpq7KFe1ZELGCSJhMZFjWpV1ZSYpWQZMFCjspEut8t4gNK3tp+29fosg+bKidSp6VywdPj4biPLJXlo3bmpMNJRPb5FRrtYqP5JhpT+maz2fZ7102fH0l/XSoipGwGknmEKy0V0Kw8sxnoGR8eY7JTx8bO+1A+qmVwUeT8Z+UVAnpCu+j82BJY5lZYYOQytAzyXevG9ot/+YMfNTxKNHZeegpdKJrnWXnx2RlAc5I3PBW4o8nDrGMiGR4drs/f7jw4f0diaeR4+wuHx8azyo51NwAAAABJRU5ErkJggg==")
