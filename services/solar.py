def calculate_cell_power(voc, isc, fill_factor):
    return voc * isc * fill_factor / 100
