from random import choice

def spd(spells, dists):
    x = choice(globals()[f'spells_{dists}'])
    if x not in spells:
        return x
    else:
        return spd(spells, dists)

def spells_distribution(round, spells):
    try:
        dist_round = dist[round-1]
    except:
        return spells

    dist_round = dist_round.split('х')
    for dists in dist_round:
        spells.append(spd(spells, dists))

    return spells

spells_1 = ["11", "112", "119", "124"]

spells_1A = [
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "19",
    "110",
    "114",
    "115",
    "120",
    "121",
    "122",
    "123",
    "125",
    "126",
    "128",
    "133",
    "136",
    "137",
    "148",
    "149",
    "150",
    "151",
    "154",
    "155",
    "156",
    "158",
    "161",
    "162",
    "163",
    "169",
    "170",
]

spells_2A = [
    "21",
    "22",
    "24",
    "25",
    "26",
    "27",
    "210",
    "212",
    "215",
    "216",
    "217",
    "218",
    "219",
    "220",
    "226",
    "228",
    "229",
    "230",
    "231",
    "232",
    "236",
    "237",
    "238",
    "239",
    "240",
    "241",
    "244",
    "246",
    "251",
    "252",
    "257",
    "260",
    "261",
    "262",
    "265",
    "266",
    "268",
    "269",
]

spells_1D = [
    "18",
    "111",
    "112",
    "113",
    "116",
    "117",
    "118",
    "119",
    "124",
    "127",
    "129",
    "130",
    "131",
    "132",
    "134",
    "135",
    "138",
    "139",
    "140",
    "141",
    "142",
    "143",
    "144",
    "145",
    "146",
    "147",
    "152",
    "153",
    "157",
    "159",
    "160",
    "164",
    "165",
    "166",
    "167",
    "168",
]

spells_2D = [
    "23",
    "28",
    "29",
    "211",
    "213",
    "214",
    "221",
    "222",
    "223",
    "224",
    "225",
    "227",
    "233",
    "234",
    "235",
    "242",
    "243",
    "245",
    "247",
    "248",
    "249",
    "250",
    "253",
    "254",
    "255",
    "256",
    "258",
    "259",
    "263",
    "264",
    "267",
    "270",
]

spells_3 = [
    "31",
    "32",
    "33",
    "35",
    "36",
    "37",
    "38",
    "39",
    "310",
    "311",
    "312",
    "313",
    "316",
    "317",
    "320",
    "323",
    "324",
    "325",
    "327",
    "329",
    "330",
    "332",
    "34",
    "314",
    "315",
    "318",
    "319",
    "321",
    "322",
    "326",
    "328",
    "331",
    "333",
    "334",
    "335",
]

dist = [
    "1х1х1х1",
    "1Aх1D",
    "1Dх1A",
    "1Aх1D",
    "1Dх1A",
    "1Dх2A",
    "1Aх1D",
    "1Aх2D",
    "1Dх1A",
    "1Dх2A",
    "1Aх3",
    "1Aх2D",
    "1Dх2A",
    "1Aх2D",
    "2Dх2A",
    "1Dх3",
    "1Aх2D",
    "2Dх2A",
    "1Dх2D",
    "2Dх2A",
    "2Aх3",
    "2Aх2D",
    "1Aх2A",
    "2Aх2D",
    "2Dх2A",
    "2Dх3",
    "2Aх2D",
    "2Dх3",
    "2Dх2A",
    "3х3",
]
