import json
from pprint import pprint


def location_filter(location):
    try:
        return location['postcode'] == '6150'
    except KeyError:
        return False


if __name__ == '__main__':
    with open('locations.json', encoding='utf-8') as f:
        locations = json.load(f)
        print(len(locations))
    location = list(filter(location_filter, locations))
    pprint(location)
