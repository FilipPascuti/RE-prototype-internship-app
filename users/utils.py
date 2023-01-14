from enum import Enum, IntEnum


class DomainTypes(IntEnum):
    IT = 1
    MEDICAL = 2
    TOURISM = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class WorkTypes(Enum):
    PART_TIME = 'PART_TIME'
    FULL_TIME = 'FULL_TIME'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class ApplicationStatus(Enum):

    RECEIVED_CV = 'RECEIVED_CV'
    HR_INTERVIEW = 'HR_INTERVIEW'
    TECHNICAL_INTERVIEW = 'TECHNICAL_INTERVIEW'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Degree(Enum):

    HIGH_SCHOOL_DIPLOMA = 'HIGH_SCHOOL_DIPLOMA'
    BACHELORS_DEGREE = 'BACHELORS_DEGREE'
    MASTERS_DEGREE = 'MASTERS_DEGREE'
    DOCTORAL_DEGREE = 'DOCTORAL_DEGREE'
    OTHER = 'OTHER'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
