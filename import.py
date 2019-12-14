#!/usr/bin/env python3


import argparse

from src import Overpass, Extractor, Exporter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("countryCode", help="The country code of the region")
    parser.add_argument(
        "startIndex", help="The index to start in the database", type=int
    )
    parser.add_argument(
        "overpassQuery", help="The filters of overpass (e.g. [\"public_transport\"=\"station\"])"
    )
    parser.add_argument(
        "--region", nargs="+", help="Which osm region to search with overpass"
    )

    args = parser.parse_args()
    print(
        "Searching for stations in region {} and exporting it for country code {} starting from index {}".format(
            args.region, args.countryCode, args.startIndex
        )
    )

    data = list()
    for region in args.region:
        data.extend(Overpass.runFor(region, args.overpassQuery))
    result = Extractor.with_data(data)
    Exporter.to_all_formats(result, args.countryCode, args.startIndex)
