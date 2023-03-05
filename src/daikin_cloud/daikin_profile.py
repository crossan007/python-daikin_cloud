"""Module"""
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class DaikinProfile:
    """Daikin user profile object"""

    name: str
    lastName: str
    toc: bool
    commercial: bool
    support: bool
    commercial_date: str
    support_date: str
    email: str
