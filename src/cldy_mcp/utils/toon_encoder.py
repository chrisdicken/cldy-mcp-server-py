"""TOON encoding with optional toon-python; falls back to compact JSON."""

import json
from typing import Any, Union

from .errors import CloudabilityError

try:
    import toon_python as toon

    _HAS_TOON = True
except ImportError:
    _HAS_TOON = False


class TOONEncodingError(CloudabilityError):
    pass


class TOONEncoder:
    @staticmethod
    def encode(data: Union[dict, list, str]) -> str:
        try:
            if isinstance(data, str):
                data = json.loads(data)
            if _HAS_TOON:
                return toon.encode(data)
            return json.dumps(data, separators=(",", ":"), default=str)
        except json.JSONDecodeError as e:
            raise TOONEncodingError(f"Failed to parse JSON: {e}") from e
        except Exception as e:
            raise TOONEncodingError(f"Failed to encode: {e}") from e

    @staticmethod
    def encode_response(response_dict: dict[str, Any]) -> str:
        if not isinstance(response_dict, dict):
            raise TOONEncodingError("Response must be a dictionary")
        return TOONEncoder.encode(response_dict)
