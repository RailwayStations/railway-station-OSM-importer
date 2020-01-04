def detect_potential_problems(osm_type, osm_id, name, tags):
    if "railway" in tags and "public_transport" not in tags:
        railway = tags["railway"]
        if railway == "halt" or railway == "station" or railway == "stop":
            print("Potential problem: missing public_transport for {}: {}".format(name, to_url(osm_type, osm_id)))


def report_missing_name(osm_type, osm_id):
    print("Potential problem: missing name for {}/{}: {}".format(osm_type, osm_id, to_url(osm_type, osm_id)))


def to_url(osm_type, osm_id):
    return "https://osm.org/{}/{}".format(osm_type, osm_id)
