from typing import Any, Literal

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Any | None = None


class ErrorResponse(BaseModel):
    success: Literal[False] = False
    error: ErrorDetail


class BlockData(BaseModel):
    index: int
    timestamp: str
    mining_time: float | None = None
    data: str
    difficulty: int
    previous_hash: str
    hash: str


class BlockchainDisplayData(BaseModel):
    blockchain: list[BlockData]


class AddBlockData(BaseModel):
    mining_time: float
    difficulty: int


class DifficultyStateData(BaseModel):
    mode: Literal["manual", "automatic"]
    current_difficulty: int


class TimeoutData(BaseModel):
    timeout: int


class LogsData(BaseModel):
    logs: list[str]


class StatusData(BaseModel):
    ddm_enabled: bool
    ddm_mode: Literal["auto", "manual"]
    timeout: int
    difficulty: int
    failed_difficulty: int | None = None


class BlockchainStatusResponse(BaseModel):
    success: Literal[True] = True
    message: str
    data: dict[str, str]


class BlockchainDisplayResponse(BaseModel):
    success: Literal[True] = True
    message: str
    data: BlockchainDisplayData


class AddBlockResponse(BaseModel):
    success: Literal[True] = True
    message: str
    data: AddBlockData


class LastBlockResponse(BaseModel):
    success: Literal[True] = True
    message: str
    data: BlockData


class DifficultyStateResponse(BaseModel):
    success: Literal[True] = True
    message: str
    data: DifficultyStateData


class MiningTimeoutResponse(BaseModel):
    success: Literal[True] = True
    message: str
    data: TimeoutData


class LogsResponse(BaseModel):
    success: Literal[True] = True
    message: str
    data: LogsData


class StatusResponse(BaseModel):
    success: Literal[True] = True
    message: str
    data: StatusData


def success_response(message: str, data: Any) -> dict[str, Any]:
    return {
        "success": True,
        "message": message,
        "data": data,
    }