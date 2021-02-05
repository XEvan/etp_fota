from ctypes import Structure, c_uint8


class T_XL_ETH_CONFIG(Structure):
    XL_ETH_MODE_SPEED_AUTO_100 = 2
    XL_ETH_MODE_SPEED_AUTO_1000 = 4
    XL_ETH_MODE_SPEED_AUTO_100_1000 = 5
    XL_ETH_MODE_SPEED_FIXED_100 = 8
    XL_ETH_MODE_SPEED_FIXED_1000 = 9
    XL_ETH_MODE_DUPLEX_DONT_CARE = 0
    XL_ETH_MODE_DUPLEX_AUTO = 1
    XL_ETH_MODE_DUPLEX_FULL = 3
    XL_ETH_MODE_CONNECTOR_DONT_CARE = 0
    XL_ETH_MODE_CONNECTOR_RJ45 = 1
    XL_ETH_MODE_CONNECTOR_DSUB = 2
    XL_ETH_MODE_PHY_DONT_CARE = 0
    XL_ETH_MODE_PHY_IEEE_802_3 = 1
    XL_ETH_MODE_PHY_BROADR_REACH = 2
    XL_ETH_MODE_CLOCK_DONT_CARE = 0
    XL_ETH_MODE_CLOCK_AUTO = 1
    XL_ETH_MODE_CLOCK_MASTER = 2
    XL_ETH_MODE_CLOCK_SLAVE = 3
    XL_ETH_MODE_MDI_AUTO = 1
    XL_ETH_MODE_MDI_STRAIGHT = 2
    XL_ETH_MODE_MDI_CROSSOVER = 3
    XL_ETH_MODE_BR_PAIR_DONT_CARE = 0
    XL_ETH_MODE_BR_PAIR_1PAIR = 1
    _fields_ = [
        ("speed", c_uint8),
        ("duplex", c_uint8),
        ("phy", c_uint8),
        ("clockMode", c_uint8),
        ("mdiMode", c_uint8),
        ("brPairs", c_uint8)
    ]
