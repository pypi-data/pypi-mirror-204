from typing import Optional
from datetime import datetime
from dataclasses import dataclass, asdict

from klu.common.models import BaseEngineModel


@dataclass
class Action(BaseEngineModel):
    guid: str
    name: str
    style: int
    prompt: str
    app_id: int
    model_id: int
    agent_type: str
    description: Optional[str]
    model_config: Optional[dict]
    experiment_id: Optional[int] = None
    updated_at: Optional[datetime] = None
    created_at: datetime = datetime.utcnow()

    @classmethod
    def _from_engine_format(cls, data: dict) -> "Action":
        return cls(
            **{
                "app_id": data.pop("appId", None),
                "model_id": data.pop("modelId", None),
                "updated_at": data.pop("updatedAt", None),
                "created_at": data.pop("createdAt", None),
                "experiment_id": data.pop("experimentId", None),
            },
            **data
        )

    def _to_engine_format(self) -> dict:
        base_dict = asdict(self)

        return {
            "appId": base_dict.pop("app_id"),
            "modelId": base_dict.pop("model_id"),
            "updatedAt": base_dict.pop("updated_at"),
            "createdAt": base_dict.pop("created_at"),
            "experimentId": base_dict.pop("experiment_id"),
            **base_dict,
        }


@dataclass
class PromptResponse:
    msg: str


@dataclass
class ActionPromptResponse(PromptResponse):
    feedback_url: str


@dataclass
class PlaygroundPromptResponse(PromptResponse):
    streaming: bool
    streaming_url: Optional[str] = None
