import codecs
import csv
import json
import os


def to_all_formats(data, country_code, start_index, base_output_dir):
    if not os.path.isdir(base_output_dir):
        os.mkdir(base_output_dir)
    json_file_name = "{}/result.json".format(base_output_dir)
    with codecs.open(json_file_name, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)
        print("Created file {}".format(json_file_name))

    csv_file_name = "{}/result.csv".format(base_output_dir)
    with open(csv_file_name, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
        writer.writeheader()
        for single_line in data:
            writer.writerow(single_line)
        print("Created file {}".format(csv_file_name))

    sql_file_name = "{}/result.sql".format(base_output_dir)
    with open(sql_file_name, "w") as sql_file:

        index = start_index

        for single_line in data:

            if single_line["uic_ref"] != "":
                uicibnr = single_line["uic_ref"]
            else:
                uicibnr = "NULL"
            sql_file.write(
                "INSERT INTO stations (countryCode, id, uicibnr, title, lat, lon) VALUES ('{}', "
                "'{}', {}, {}, {}, {});\n".format(
                    country_code,
                    index,
                    uicibnr,
                    single_line["name"].replace("'", "\\'"),
                    single_line["lat"],
                    single_line["lon"],
                )
            )
            index = index + 1
        print("Created file {}".format(sql_file_name))
