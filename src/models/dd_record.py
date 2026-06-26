from dataclasses import dataclass
from datetime import datetime


@dataclass
class DDRecord:
    generated_time: datetime

    hostname: str
    model: str
    serial: str
    ddos: str

    pre_comp_used_tib: float
    post_comp_used_tib: float
    post_comp_size_tib: float
    post_comp_avail_tib: float

    reduction: float
    compression: float

    cleaning: float = 0.0