import json
import re

from pydriosm import GeofabrikReader

from src.IgnoreFile import IgnoreFile
from src.ProblemDetector import detect_potential_problems, report_missing_name


def download_osm(region: str, ignore_file: IgnoreFile):
    print("Start reading pbf file")
    osm_region = GeofabrikReader().read_osm_pbf(region, download_confirmation_required=False, verbose=True)
    print("Finished reading pbf file")

    resulting_nodes = list()
    for type_collection in osm_region:
        print("Looking in {} for railway stations".format(type_collection))
        for index, type_instance_pd in osm_region[type_collection].iterrows():
            type_instance = json.loads(type_instance_pd[type_collection])["properties"]
            tags = get_tags(type_instance["other_tags"])
            osm_type = get_osm_type(type_collection)
            osm_id = get_osm_id(type_instance)
            name = type_instance["name"]
            if not ignore_file.should_be_ignored(osm_type, osm_id):
                if tags:
                    if is_train_station(osm_type, osm_id, name, tags):
                        railway = tags["railway"]
                        if railway == "halt" or railway == "station":
                            if not osm_id:
                                print("unable to determine osm id for:")
                                print(type_instance)
                            coordinates = extract_coordinates(
                                type_instance, type_collection
                            )
                            resulting_nodes.append(
                                station(osm_id, name, coordinates, tags, osm_type)
                            )
                    else:
                        detect_potential_problems(osm_type, osm_id, name, tags)
    return resulting_nodes


def get_tags(other_tags):
    result = {}
    if other_tags:
        split = re.findall(r"\"[^,]+\"=>\"[^,]+\"", other_tags)
        for entry in split:
            key_value = re.split(r'=>', entry)
            result[key_value[0].replace("\"", "")] = key_value[1].replace("\"", "")
    return result


def get_osm_id(type_instance):
    if "osm_id" in type_instance:
        return type_instance["osm_id"]
    else:
        return type_instance["osm_way_id"]


def is_train_station(osm_type, osm_id, name, tags):
    is_public_transport = "public_transport" in tags and (tags["public_transport"] == "station" or tags["public_transport"] == "stop_position")
    result = is_public_transport and "railway" in tags
    if result and (name is None or name == ""):
        report_missing_name(osm_type, osm_id)
        return False
    return result



def get_osm_type(type_collection):
    if type_collection == "points":
        return "node"
    if type_collection == "lines":
        return "way"
    if (
            type_collection == "multilinestrings"
            or type_collection == "multipolygons"
            or type_collection == "other_relations"
    ):
        return "relation"


def extract_coordinates(type_instance, collection_type):
    if collection_type == "multipolygons":
        return type_instance.coordinates.centroid
    else:
        return type_instance.coordinates


def station(osm_id, name, coordinates, tags, osm_type):
    tags["name"] = name
    return {
        "lat": str(coordinates.y),
        "lon": str(coordinates.x),
        "osm_id": osm_id,
        "tags": tags,
        "osm_type": osm_type,
    }
