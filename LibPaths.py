class LibPaths:
    # for windows import path or static path
    static_path = None
    dynamic_path = None

    @property
    def import_path(self):
        return self.static_path

    @import_path.setter
    def import_path(self, import_path):
        self.static_path = import_path

    def set_path(self, path):
        if '.so' in path or 'dll' in path:
            self.dynamic_path = path
        if '.a' in path or '.lib' in path:
            self.static_path = self.import_path

    def get_path(self):
        return self.static_path or self.dynamic_path

    def only_static(self):
        return bool(self.static_path) and not bool(self.dynamic_path)

    def __bool__(self):
        return bool(self.get_path())
