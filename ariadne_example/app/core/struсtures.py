import enum
from typing import Optional
from dataclasses import dataclass

from ariadne import EnumType, ScalarType


class ErrorTypes(enum.Enum):
    SERVER_ERROR = enum.auto()
    NOT_FOUND_ERROR = enum.auto()
    VALIDATION_ERROR = enum.auto()


@dataclass
class ErrorScalar:
    message: Optional[str]
    code: ErrorTypes
    text: Optional[str]


class TaskStatusEnum(enum.Enum):
    draft = "draft"
    in_process = "in_process"
    delete = "delete"
    done = "done"

task_type_enum = EnumType("TaskStatusEnum", TaskStatusEnum)
datetime_scalar = ScalarType("DateTime")

@datetime_scalar.serializer
def serialize_datetime(value):
    return value.isoformat()

TASK_QUEUES = []
