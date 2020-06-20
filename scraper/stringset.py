class StringSet:
    def __init__(self):
        super().__init__()
        self.data = []

    def insert(self, some_string):
        if not self.contains(some_string):
            cnt = 0
            for x in self.data:
                if(some_string > x):
                    cnt += 1
                else:
                    break
            self.data.insert(cnt, some_string)

    def remove(self, some_string):
        if self.contains(some_string):
            self.data.remove(some_string)

    def contains(self, some_string):
        return some_string in self.data

    def clear_data(self):
        self.data = []

    def to_string(self):
        ret = ""
        for x in self.data:
            ret = ret + x + ","
        ret = ret[:-1]
        return ret

    def from_string_list(self, str_lst):
        self.data = str_lst
        self.data.sort()

    def from_string(self, some_string):
        self.clear_data()
        if(some_string == None):
            self.data = []
        else:
            self.data = some_string.split(',')
            self.data.sort()
