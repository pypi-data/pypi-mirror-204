import json

class Database:
    def __init__(self, path) -> None:
        self.path = path
        # create file if it does not exist
        with open(path, 'a'):
            pass
        
        # check if it is a database file
        isDB = False
        with open(path, 'r') as f:
            lines = f.readlines()
            if len(lines) >= 2 and lines[0].startswith("PYDB v"):
                self.data = json.loads(lines[1])
                isDB = True
        
        # if it is not a database, format it to be one
        if not isDB:
            with open(path, 'w') as f:
                self.data = {"tables": {}}
                f.write(f"PYDB v1 Beta\n{json.dumps(self.data)}")
    def __str__(self) -> str:
        return "<PYDB.Database.Class>"
    def __repr__(self) -> str:
        return "<PYDB.Database.Class>"

    # Append to data
    def addTable(self, name:str, cols:list) -> None:
        if self.data["tables"].get(name, None):
            raise RuntimeError("table already exist")
        else:
            self.data["tables"][name] = {}
            for c in cols:
                self.data["tables"][name][c] = []
    
    def addRow(self, table, **cols) -> None:
        keys = []
        for x in cols.keys():
            keys.append(x)
        vals = []
        for x in cols.values():
            vals.append(x)

        for i in range(len(keys)):
            self.data["tables"][table][keys[i]].append(vals[i])
    
    def addCol(self, table, colName) -> None:
        self.data["tables"][table][colName] = []

    # delete data
    def remTable(self, table) -> None:
        self.data["tables"].pop(table)

    def remRow(self, table, index) -> None:
        for c in self.data["tables"][table]:
            self.data["tables"][table][c].pop(index)

    def remCol(self, table, col) -> None:
        self.data["tables"][table].pop(col)

    # Get and set data
    def fetch(self, table, col, value):
        if value in self.data["tables"][table][col]:
            for i,v in enumerate(self.data["tables"][table][col]):
                if v == value:
                    return i
        return -1

    def getTables(self) -> list:
        names = []
        for t in self.data["tables"]:
            names.append(t)
        return names

    def set(self, table, col, index, value) -> bool:
        try:
            self.data["tables"][table][col][index] = value
            return True
        except:
            return False
    
    # store data (Major optimization from updating with every set)
    def commit(self):
        with open(self.path, 'w') as f:
            f.write(f"PYDB v1 Beta\n{json.dumps(self.data)}")

