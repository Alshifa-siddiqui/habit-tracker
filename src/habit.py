from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class Habit:
    task: str
    periodicity: str
    creation_date: datetime = datetime.now(timezone.utc)
    
    def complete(self):
        return datetime.now(timezone.utc)