"""Base pydantic models that our real models will inherit from.

This is an easy way of keeping consistent model configs across the project.
"""
import pydantic


class BaseModel(pydantic.BaseModel, allow_mutation=False, extra="forbid"):
    ...
