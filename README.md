# OSM Importer for railway-stations.org

This pythons scripts helps to export railway stations from osm to import them to the database of https://railway-stations.org

## How to run it
This project requires Python3
```bash
pip install -r requirements.txt
./import.py -h # will show all possible parameters
```
An example for Luxembourg
```bash
./import.py lu 0 --region Luxembourg
```
The script exports 3 formats (json, csv, sql) in the `output`-directory


