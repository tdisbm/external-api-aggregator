from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.components.dto.SecurityPolicy import SecurityPolicy
from app.components.dto.Vulnerability import Vulnerability


class Security(BaseModel):
    vulnerabilities: List[Vulnerability] = Field(default_factory=list)
    policies: List[SecurityPolicy] = Field(default_factory=list)
    last_vulnerability_scan: Optional[datetime] = Field(default_factory=lambda: None)
    last_compliance_scan: Optional[datetime] = Field(default_factory=lambda: None)
