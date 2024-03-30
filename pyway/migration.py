from pyway.helpers import Utils
from typing import List, Any, Optional, Type


class Migration():
    def __init__(self, version: Any, extension: Any, name: Any,
                 checksum: Any, apply_timestamp: Optional[Any]) -> None:
        self.version: str = version
        self.extension: str = extension
        self.name: str = name
        self.checksum: str = checksum
        self.apply_timestamp: Optional[Any] = apply_timestamp

    @classmethod
    def from_name(cls: Type['Migration'], name: str, path: str, **kwargs: str) -> 'Migration':
        version = kwargs.get('version', Utils.get_version_from_name(name))
        extension = kwargs.get('extension', Utils.get_extension_from_name(name))
        checksum = kwargs.get('checksum', Utils.load_checksum_from_name(name, path))
        apply_timestamp = kwargs.get('apply_timestamp')
        return cls(version, extension, name, checksum, apply_timestamp)

    @classmethod
    def from_list(cls, list_: List['Migration']) -> List['Migration']:
        return [cls(m.version, m.extension, m.name, m.checksum, m.apply_timestamp) for m in list_]

    def __str__(self) -> str:
        return f"version={self.version}, extension={self.extension}, checksum={self.checksum}, " \
                "apply_timestamp={self.apply_timestamp}"
