from pydantic import BaseModel, ConfigDict, Field


class BaseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )


class BaseResponse(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    