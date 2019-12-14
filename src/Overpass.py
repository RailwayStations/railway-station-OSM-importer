import overpy


def runFor(region):
    api = overpy.Overpass()
    query = """
    area[name="{}"]->.searchArea;
    (
      node["public_transport"="station"](area.searchArea);
    );
    out body;
    """.format(
        region
    )
    result = api.query(query)
    print("Found {} nodes for {}".format(len(result.nodes), region))
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
    return resulting_nodes
