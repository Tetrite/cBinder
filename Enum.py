from enum import Enum
from CType import CType, get_c_type_for_type

class EnumDeclaration:
    def __init__(self, enum):
        self.name = enum['name']
        self.values = enum['values']
        self.declaration_string = self._build_declaration_string(enum)

    def _build_declaration_string(self, enum):
        parts = [f'enum {self.name}{{']
        for name, value in enum['values']:
            parts.append(f'{name}={value},')
        parts.append(');\n')
