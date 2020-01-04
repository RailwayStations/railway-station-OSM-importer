class IgnoreFile:
    def __init__(self, path_to_ignore_file: str):
        self.ignore = {"node": list(), "way": list(), "relation": list()}
        if path_to_ignore_file:
            with open(path_to_ignore_file) as file:
                for line in file:
                    if "/" in line:
                        split = line.rstrip("\n").split("/")
                        osm_type = split[0]
                        osm_id = split[1]
                        self.ignore[osm_type].append(osm_id)

    def should_be_ignored(self, osm_type: str, osm_id: str):
        return osm_id in self.ignore[osm_type]
