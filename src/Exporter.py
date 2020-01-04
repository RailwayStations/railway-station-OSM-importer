import codecs
import csv
import json
import os

from src import HtmlRenderer


def to_all_formats(data, country_code, start_index, base_output_dir):
    if not os.path.isdir(base_output_dir):
        os.mkdir(base_output_dir)
    toJson(base_output_dir, data)
    to_csv(base_output_dir, data)
    to_sql(base_output_dir, data, country_code, start_index)
    to_html_map(base_output_dir, data)


def to_html_map(base_output_dir, data):
    html_file_name = "{}/result.html".format(base_output_dir)
    HtmlRenderer.render_html("map.html", {"stations": data}, html_file_name)
    print_created_file(html_file_name)


def to_sql(base_output_dir, data, country_code, start_index):
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
                    "" if single_line["name"] is None else single_line["name"].replace("'", "\\'"),
                    single_line["lat"],
                    single_line["lon"],
                )
            )
            index = index + 1
        print_created_file(sql_file_name)


def to_csv(base_output_dir, data):
    csv_file_name = "{}/result.csv".format(base_output_dir)
    with open(csv_file_name, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
        writer.writeheader()
        for single_line in data:
            writer.writerow(single_line)
        print_created_file(csv_file_name)


def toJson(base_output_dir, data):
    json_file_name = "{}/result.json".format(base_output_dir)
    with codecs.open(json_file_name, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)
        print_created_file(json_file_name)


def print_created_file(file_name):
    os.path.abspath(file_name)
    print("Created file://{}".format(os.path.abspath(file_name)))
