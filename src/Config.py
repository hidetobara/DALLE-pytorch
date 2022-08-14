import os, json, yaml


class Config:
    def __init__(self, path=None, table=None):
        self.table = {}
        if path is not None and os.path.exists(path):
            with open(path, 'r') as f:
                self.load_map(yaml.safe_load(f))
        if table is not None:
            self.load_map(table)

    def load_env(self):
        for key, value in os.environ.itmes():
            self.table[key] = value

    def load_map(self, table):
        for key, value in table.items():
            self.table[key] = value
    
    def __getattr__(self, key):
        if key in self.table:
            return self.table[key]
        return None

    #def __setattr__(self, key, value):
    #    self.table[key] = value

    def put(self, key, value):
        self.table[key] = value
    
    def get(self, key, default=None):
        if key not in self.table:
            return default
        return self.table[key]

    def __str__(self) -> str:
        cells = []
        for key, value in self.table.items():
            cells.append(str(key) + ": " + str(value))
        return "{" + ", ".join(cells) + "}"