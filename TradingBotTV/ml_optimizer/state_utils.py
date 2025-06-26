from dataclasses import asdict, is_dataclass
from pathlib import Path
import json
from typing import Type, TypeVar

T = TypeVar('T')


def load_state(path: Path, cls: Type[T]) -> T:
    """Load dataclass instance of type ``cls`` from ``path``."""
    try:
        data = json.loads(path.read_text())
    except FileNotFoundError:
        return cls()  # type: ignore[arg-type]
    return cls(**data)  # type: ignore[arg-type]


def save_state(path: Path, state: T) -> None:
    """Save dataclass ``state`` to ``path``."""
    if not is_dataclass(state):
        raise TypeError('state must be a dataclass instance')
    path.write_text(json.dumps(asdict(state)))
