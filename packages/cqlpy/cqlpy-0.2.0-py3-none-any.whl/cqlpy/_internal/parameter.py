from typing import Optional


class Parameter:
    def __init__(
        self,
        name: str,
        type_name: str,
        default_value: Optional[str] = None,
    ):
        self.name = name
        self.type_name = type_name
        self.default_value = default_value

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Parameter(name={self.name}, type_name={self.type_name}, default_value={self.default_value})"
