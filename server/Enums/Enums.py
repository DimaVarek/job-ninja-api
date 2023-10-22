import enum


class InterviewTypeEnum(enum.Enum):
    Application = 0
    Phone = 1
    Manager = 2
    HR = 3
    Technical = 4
    Offer = 5
    Finish = 6
    Default = 7


class InterviewStatusEnum(enum.Enum):
    Accepted = 0
    Pending = 1
    Rejected = 2
    Default = 3
