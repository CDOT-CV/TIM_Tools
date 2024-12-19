from enum import Enum


class ItisCodes(Enum):
    """
    Enum class representing various ITIS (International Traveler Information Systems) codes.
    """
    SPEED_LIMIT = '368'
    ACCIDENT = '513'
    INCIDENT = '531'
    HAZARDOUS_MATERIAL_SPILL = '550'
    CLOSED = '770'
    CLOSED_FOR_SEASON = '774'
    REDUCED_ONE_LANE = '777'
    AVALANCHE_CONTROL_ACTIVITIES = '1042'
    ROAD_CONSTRUCTION = '1025'
    HERD_OF_ANIMALS_ON_ROADWAY = '1292'
    ROCKFALL = '1309'
    LANDSLIDE = '1310'
    DELAYS = '1537'
    WIDE_LOAD = '2050'
    NO_TRAILERS = '2568'
    WIDTH_LIMIT = '2573'
    HEIGHT_LIMIT = '2574'
    WILD_FIRE = '3084'
    WEATHER_EMERGENCY = '3201'
    MAJOR_EVENT = '3841'
    NO_PARKING_SPACES_AVAILABLE = '4103'
    FEW_PARKING_SPACES_AVAILABLE = '4104'
    SPACES_AVAILABLE = '4105'
    NO_PARKING_INFO_AVAILABLE = '4223'
    SEVERE_WEATHER = '4865'
    SNOW = '4868'
    WINTER_STORM = '4871'
    RAIN = '4885'
    STRONG_WINDS = '5127'
    FOG = '5378'
    VISIBILITY_REDUCED = '5383'
    BLOWING_SNOW = '5985'
    BLACK_ICE = '5908'
    WET_PAVEMENT = '5895'
    ICE = '5906'
    ICY_PATCHES = '5907'
    SNOW_DRIFTS = '5927'
    GRAVEL_ROAD_SURFACE = '5933'
    DRY_PAVEMENT = '6011'
    DIRT_ROAD_SURFACE = '6016'
    MILLED_ROAD_SURFACE = '6017'
    SNOW_TIRES_OR_CHAINS_REQUIRED = '6156'
    LOOK_OUT_FOR_WORKERS = '6952'
    KEEP_TO_RIGHT = '7425'
    KEEP_TO_LEFT = '7426'
    REDUCE_YOUR_SPEED = '7443'
    DRIVE_CAREFUL = '7169'
    DRIVE_WITH_EXTREME_CAUTION = '7170'
    INCREASE_FOLLOWING_DISTANCE = '7173'
    PREPARE_TO_STOP = '7186'
    STOP_AT_NEXT_SAFE_PLACE = '7188'
    ONLY_TRAVEL_IF_NECESSARY = '7189'
    FALLING_ROCKS = '1203'

ItisCodeExtraKeywords = {
    "herd of animals on roadway": "herd of animals on the roadway",
    "rockfall": "rock fall",
    "wildfire": "wild fire",
    "keep to right": "keep right",
    "keep to left": "keep left",
    "reduce your speed": "reduce speed",
    "drive careful": "drive carefully",
    "stop at next safe place": "stop at the next safe place",
    "only travel if necessary": "only necessary travel",
    "falling rocks": "falling rock",
    "icy patches": "icy spots",
    "snow": "snow packed spots",
    "closed for season": "seasonal closure",
    "ice": "icy",
    "icy spots": "icy patches",
    "snow packed spots": "snow"
}