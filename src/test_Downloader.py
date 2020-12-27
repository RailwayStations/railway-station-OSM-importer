from unittest import TestCase

from src.Downloader import get_tags


class Test(TestCase):
    def test_get_tags(self):
        result = get_tags('"crossing"=>"uncontrolled"')
        expected = {
            "crossing": "uncontrolled"
        }
        self.assertDictEqual(result, expected)

    def test_get_tags_2(self):
        result = get_tags(
            '"name:ca"=>"Pica d\'Estats","name:fr"=>"Pic d\'Estats","natural"=>"peak","wikidata"=>"Q1537733","wikipedia"=>"ca:Pica d\'Estats","prominence"=>"1290","url:source"=>"ftp://geofons.icc.cat/fitxes/100CIMS/271064006.pdf","source:date"=>"2010","source:prominence"=>"https://en.wikipedia.org/wiki/List_of_Pyrenean_three-thousanders"')
        expected = {
            "name:ca": "Pica d'Estats",
            "name:fr": "Pic d'Estats",
            "natural": "peak",
            "prominence": "1290",
            "source:date": "2010",
            "source:prominence": "https://en.wikipedia.org/wiki/List_of_Pyrenean_three-thousanders",
            "url:source": "ftp://geofons.icc.cat/fitxes/100CIMS/271064006.pdf",
            "wikidata": "Q1537733",
            "wikipedia": "ca:Pica d'Estats",
        }
        self.assertDictEqual(result, expected)
