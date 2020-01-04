import pydriosm as dri

from src.IgnoreFile import IgnoreFile
from src.ProblemDetector import detect_potential_problems


def downloadOsm(region: str, ignore_file: IgnoreFile):
    osm_region = dri.read_osm_pbf(
        region,
        data_dir=None,
        parsed=True,
        file_size_limit=50,
        fmt_other_tags=True,
        fmt_single_geom=True,
        fmt_multi_geom=True,
        update=False,
        download_confirmation_required=False,
        pickle_it=True,
        rm_osm_pbf=False,
        verbose=True,
    )

    resulting_nodes = list()
    for type_collection in osm_region:
        print("Looking in {} for railway stations".format(type_collection))
        for index, type_instance in osm_region[type_collection].iterrows():
            tags = type_instance["other_tags"]
            osm_type = get_osm_type(type_collection)
            osm_id = get_osm_id(type_instance)
            name = type_instance["name"]
            if not ignore_file.should_be_ignored(osm_type, osm_id):
                if tags is not None:
                    if is_train_station(tags):
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


def get_osm_id(type_instance):
    if type_instance.osm_id:
        return type_instance.osm_id
    else:
        return type_instance.osm_way_id


def is_train_station(tags):
    return (
        "public_transport" in tags
        and tags["public_transport"] == "station"
        and "railway" in tags
    )


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
