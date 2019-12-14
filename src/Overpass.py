import overpy


def runFor(region, overpassQuery):
    api = overpy.Overpass()
    query = """
    area[name="{}"]->.searchArea;
    (
      node{}(area.searchArea);
      way{}(area.searchArea);
      relation{}(area.searchArea);
    );
    out body;
    """.format(
        region,
        overpassQuery,
        overpassQuery,
        overpassQuery
    )
    result = api.query(query)
    print("Found {} nodes {} ways and {} relations for {}".format(len(result.nodes), len(result.ways), len(result.relations), region))
    resulting_nodes = list()
    for node in result.nodes:
        resulting_nodes.append(
            {
                "lat": str(node.lat),
                "lon": str(node.lon),
                "id": node.id,
                "tags": node.tags,
            }
        )
    for way in result.ways:
        resulting_nodes.append(
            {
                "lat": str(way.center_lat),
                "lon": str(way.center_lon),
                "id": way.id,
                "tags": way.tags,
            }
        )
    for relation in result.relations:
        resulting_nodes.append(
            {
                "lat": str(relation.center_lat),
                "lon": str(relation.center_lon),
                "id": relation.id,
                "tags": relation.tags,
            }
        )
    return resulting_nodes
