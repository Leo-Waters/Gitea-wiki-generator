from pathlib import Path
#base class for script parsers
class ScriptParser:
    def __init__(self,language):
        self.language=language
    
    #loads the contents of a file as a string
    @staticmethod
    def _load_from_file(filePath):
        return Path(filePath).read_text()

    def parse_file(self,filePath,namespaces):
        pass# should be inherited
