def get_value_or_empty(obj, resulting_key, result):
    if resulting_key in obj:
        result[resulting_key] = obj[resulting_key]
    else:
        result[resulting_key] = ""


def with_data(data):
    result = []
    for station in data:
        tags = station["tags"]

        is_railway = "railway" in tags
        is_subway = "station" in tags and tags["station"] == "subway"
        if is_railway and not is_subway:
            resulting_station = dict()

            get_value_or_empty(tags, "name", resulting_station)
            get_value_or_empty(station, "lat", resulting_station)
            get_value_or_empty(station, "lon", resulting_station)
            get_value_or_empty(tags, "uic_ref", resulting_station)
            get_value_or_empty(station, "osm_id", resulting_station)
            get_value_or_empty(station, "osm_type", resulting_station)
            if resulting_station["uic_ref"] == "" and resulting_station["name"] == "":
                print(
                    "skipping as not enough data: https://osm.org/node/{}".format(
                        station["id"]
                    )
                )
            else:
                result.append(resulting_station)
    return result
