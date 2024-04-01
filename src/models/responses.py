from pydantic import BaseModel


def to_lower_camel(string: str):
    return string.partition("_")[0] + "".join(
        word.capitalize() for word in string.split("_")[1:]
    )


class LowerCamelAlias(BaseModel):
    class Config:
        alias_generator = to_lower_camel
        populate_by_name = True


class AliveResponse(LowerCamelAlias):
    alive: bool
