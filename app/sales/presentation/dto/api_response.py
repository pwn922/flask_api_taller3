from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class ApiResponse:
    success: bool
    message: str
    data: dict[str, Any]
