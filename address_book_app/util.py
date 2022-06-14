import geopy.distance


def get_distance_in_km_from_coordinates(latitude_1, longitude_1, latitude_2, longitude_2):
    coords_1 = (latitude_1, longitude_1)
    coords_2 = (latitude_2, longitude_2)
    return geopy.distance.geodesic(coords_1, coords_2).km


def filter_address_by_distance(address_items, distance_limit, latitude_limit, longitude_limit):
    nearby_address = []
    for address in address_items:
        distance_between = get_distance_in_km_from_coordinates(
            address.latitude, address.longitude,
            latitude_limit, longitude_limit)

        if distance_between > distance_limit:
            continue
        else:
            nearby_address.append(address)
    return nearby_address
