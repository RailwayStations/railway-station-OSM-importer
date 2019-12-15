#!/usr/bin/env python3


import argparse

from src import Overpass, Extractor, Exporter, CurrentStations

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("countryCode", help="The country code of the region")
    parser.add_argument(
        "overpassQuery",
        help='The filters of overpass (e.g. ["public_transport"="station"])',
    )
    parser.add_argument(
        "--outputDir", help="Where to output the files", default="./output"
    )
    parser.add_argument(
        "--startIndex",
        help="Override the index to start in the database. Otherwise the script will lookup the latest id",
        type=int,
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
    if args.startIndex is None:
        lastDatabaseId = CurrentStations.getCurrentLastDatabaseIds(args.countryCode)
        startIndex = lastDatabaseId + 1
        print(
            "The latest station id found for {} is {}, so the stating id will be {}".format(
                args.countryCode, lastDatabaseId, startIndex
            )
        )
    else:
        startIndex = args.startIndex
    Exporter.to_all_formats(result, args.countryCode, startIndex, args.outputDir)
