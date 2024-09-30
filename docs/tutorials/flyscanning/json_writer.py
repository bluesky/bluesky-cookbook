class JSONWriter:
    """Callback to write a Bluesky stream into a JSON file. Useful for debugging.

    Parameters
    ----------
        filepath : str
            A desired path to a .json file used to save the data.

    """

    def __init__(self, filepath: str):
        if not filepath.endswith(".json"):
            filepath = filepath + ".json"
        self.filepath = filepath

    def __call__(self, name, doc):
        import json

        if name == "start":
            self.file = open(self.filepath, "w")
            self.file.write("[\n")

        json.dump({"name": name, "doc": doc}, self.file)

        if name == "stop":
            self.file.write("\n]")
            self.file.close()
        else:
            self.file.write(",\n")
