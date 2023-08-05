from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from dataclasses import dataclass, field, asdict

from klu.common.models import BaseEngineModel


@dataclass
class Workspace(BaseEngineModel):
    id: int
    name: str

    project_guid: UUID = uuid4()
    updated_at: Optional[datetime] = None
    created_at: datetime = datetime.utcnow()

    @classmethod
    def _from_engine_format(cls, data: dict) -> "Workspace":
        return cls(
            **{
                "updated_at": data.pop("updatedAt"),
                "created_at": data.pop("createdAt"),
            },
            **data
        )

    def _to_engine_format(self) -> dict:
        base_dict = asdict(self)

        return {
            "updatedAt": base_dict.pop('updated_at'),
            "createdAt": base_dict.pop('created_at'),
            **base_dict,
        }
