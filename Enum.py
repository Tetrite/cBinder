from enum import Enum
from CType import CType, get_c_type_for_type

class EnumDeclaration:
    def __init__(self, enum):
        if 'name' in enum:
            self.name = enum['name']
        else:
            self.name = None
        self.values = enum['values']
        self.declaration_string = self._build_declaration_string(enum)

    def _build_declaration_string(self, enum):
        if self.name:
            parts = [f'typedef enum {{']
            for elem in enum['values']:
                name = elem['name']
                value = elem['value']
                parts.append(f'{name}={value},')
            parts[-1] = parts[-1][:-1]
            parts.append(f'}}{self.name};\n')
            return ' '.join(parts)
        else:
            parts = [f'enum {{']
            for elem in enum['values']:
                name = elem['name']
                value = elem['value']
                parts.append(f'{name}={value},')
            parts[-1] = parts[-1][:-1]
            parts.append(f'}};\n')
            return ' '.join(parts)

