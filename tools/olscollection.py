from dataclasses import dataclass
from dataclasses_json import dataclass_json
from tools.olsmap import OlsMap


@dataclass
@dataclass_json
class OlsCollection:
    maps: list[OlsMap]
