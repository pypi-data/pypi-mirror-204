import math

def shale_horsrud_porosity(porosity):
    return 243.6 * (100 * porosity) ** (-0.96)


def limestone_faquhar_porosity(porosity):
    return 174.8 * math.exp( -0.093 * 100 * porosity)


def sandstone_edimann_porosity(porosity):
    return -3.225 * 100 * porosity + 129.54


def shale_horsrud_delta_tc(delta_tc):
    return 0.77 * (304.8 / delta_tc) ** 2.93


def limestone_golubev_delta_tc(delta_tc):
    return (10 ** (2.44 + 109.14 / delta_tc)) / 145


def sandstone_edimann_porosity(porosity):
    return -3.225 * 100 * porosity + 129.54


def sandstone_macnelly_delta_tc(delta_tc):
    return 1200 * math.exp( -0.036 * delta_tc)