import json

# noinspection PyPackageRequirements
import geograpy  # from geograpy3
import nltk
import requests

from ..disaggregation_module import DisaggregationModule, DisaggregationModuleLabels


class ContinentLabels(DisaggregationModuleLabels):
    AFRICA = "africa"
    AMERICAS = "americas"
    ASIA = "asia"
    EUROPE = "europe"
    OCEANIA = "oceania"


class Continent(DisaggregationModule):
    labels = ContinentLabels
    continents = [
        ContinentLabels.AFRICA,
        ContinentLabels.AMERICAS,
        ContinentLabels.ASIA,
        ContinentLabels.EUROPE,
        ContinentLabels.OCEANIA,
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(module_id="continent", *args, **kwargs)

        countries_url = "https://raw.githubusercontent.com/bigscience-workshop/data_sourcing/master/"\
                        "sourcing_sprint/resources/country_regions.json"

        response = json.loads(requests.get(countries_url).text)

        self.continents = response[0]
        countries = response[1]
        region_countries = response[2]

        def get_countries_and_regions(continent_or_region):
            return_countries_and_regions = {"countries": [], "regions": []}

            for region in region_countries.get(continent_or_region):
                if region in countries:
                    return_countries_and_regions["countries"] = return_countries_and_regions["countries"] + [region]
                else:
                    countries_and_regions = get_countries_and_regions(region)
                    return_countries_and_regions["regions"] = return_countries_and_regions["regions"] + [region]
                    return_countries_and_regions["countries"] = (
                        return_countries_and_regions["countries"] + countries_and_regions["countries"]
                    )

            return return_countries_and_regions

        continent_maps = {c: get_countries_and_regions(c) for c in self.continents}

        self.continent_lists = [
            [c, *continent_maps[c]["regions"], *continent_maps[c]["countries"]] for c in continent_maps
        ]

        nltk.download("punkt")
        nltk.download("averaged_perceptron_tagger")
        nltk.download("maxent_ne_chunker")
        nltk.download("words")

    def __call__(self, row, *args, **kwargs):
        return_continent = {continent: False for continent in list(ContinentLabels)}

        places = geograpy.get_place_context(text=row[self.column]).countries

        if not len(places) > 0:
            return return_continent

        continent_search = [cl[0] for cl in self.continent_lists if places[0] in cl]

        if len(continent_search) > 0:
            continent = continent_search[0]
            label = getattr(ContinentLabels, continent.upper())
            return_continent.update({label: True})

        return return_continent
