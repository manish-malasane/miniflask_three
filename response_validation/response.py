from pydantic import BaseModel
from typing import Optional, Union


class ResponseValidation(BaseModel):
    Record_Count: Union[str, int]
    Name: str
    Message: Optional[str]

    # @validator("record_count")
    # def check_records_count(cls, record_count):
    #     if isinstance(record_count, int) or isinstance(record_count, str):
    #         return int(record_count)
