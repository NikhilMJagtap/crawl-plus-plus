class GenericParser:
    
    def __init__(self, group):
        self.is_parsing = False
        self.data = None
        self.group = group

    def parse(self, chunk):
        raise NotImplementedError("Parse method should be implemented and must return data")

    def start_parsing(self, chunk):
        if self.is_parsing:
            return None
        self.is_parsing = True
        self.data = data = self.parse(chunk)
        if self.data is None:
            raise NotImplementedError("Improper implementation of parse method. Must return data.")
        self.is_parsing = False
        self.data = None
        return data

    def save_data(self):
        # TODO: save self.data in db
