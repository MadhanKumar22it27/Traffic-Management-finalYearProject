dictionary = {
    5: {"car": 3, "bike": 2, "bus": 4, "truck": 5},
    10: {"car": 4, "bike": 3, "bus": 6, "truck": 7},
    15: {"car": 6, "bike": 4, "bus": 8, "truck": 10}
}

def green_time(vehicle_dict):

    total = 0

    for dist in [5, 10, 15]:
        for vehicle, count in vehicle_dict.get(dist, {}).items():
            total += dictionary[dist][vehicle] * count

    # Cap maximum green time
    return min(total, 60)