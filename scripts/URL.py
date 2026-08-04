

class URL:
    def __init__(self, url, file):
        self.url = url
        self.file = file

    def remove_duplicates(self):
        with open(self.file, 'r') as f:
            file_read = f.read().splitlines()
        result = list(dict.fromkeys(file_read))
        return result