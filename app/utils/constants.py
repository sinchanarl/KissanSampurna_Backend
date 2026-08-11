from enum import Enum


class LandholdingEnum(Enum):
    SMALL = 'Small (<2 ha)'
    MEDIUM = 'Medium (2–5 ha)'
    LARGE = 'Large (>5 ha)'


class WaterSourceEnum(Enum):
    BOREWELL_CANAL = 'Borewell/Canal'
    BOREWELL_RAIN = 'Borewell + Rain'
    RAINFED_RIVER = 'Rainfed + River'
    RAINFED_POND = 'Rainfed + Pond'
    BOREWELL_CANAL_2 = 'Borewell + Canal'


class BudgetPerAcreEnum(Enum):
    BELOW_10000 = '<10,000'
    RANGE_10K_15K = '10,000–15,000'
    RANGE_12K_20K = '12,000–20,000'
    RANGE_15K_18K = '15,000–18,000'
    RANGE_20K_PLUS = '20,000+'
    BELOW_15K = '<15,000'


class RiskAppetiteEnum(Enum):
    LOW = 'Low'
    MEDIUM = 'Medium'
    MEDIUM_HIGH = 'Medium-High'
    MEDIUM_TO_HIGH = 'Medium to High'
    HIGH = 'High'


class CropCycleEnum(Enum):
    SHORT_MEDIUM = 'Short-Medium'
    MEDIUM = 'Medium'


class CropRotationEnum(Enum):
    YES = 'Yes'
    NO = 'No'


class IrrigationTypeEnum(Enum):
    NA = 'N/A'
    FLOOD = 'Flood'
    FLOOD_SPRINKLER = 'Flood / Sprinkler'
    FLOOD_DRIP = 'Flood / Drip'


class MarketAccessEnum(Enum):
    YES = 'Yes'
    LIMITED = 'Limited'


class OwnsLivestockEnum(Enum):
    YES = 'Yes'
    NO = 'No'


class SmartphoneUseEnum(Enum):
    YES = 'Yes'
    NO = 'No'


class MachineryUsedEnum(Enum):
    LIGHT = 'Light'
    HEAVY = 'Heavy'
    LIGHT_HEAVY = 'Light-Heavy'


class StorageFacilityEnum(Enum):
    YES = 'Yes'
    NO = 'No'
    PARTIAL = 'Partial'


class TransportAccessEnum(Enum):
    YES = 'Yes'
    PARTIAL = 'Partial'


class TemperatureRangeEnum(Enum):
    RANGE_25_35 = '25–35'


class AltitudeRangeEnum(Enum):
    RANGE_0_1000 = '0–1000'
    RANGE_0_800 = '0–800'


class FertilizerUsedEnum(Enum):
    ORGANIC = "organic"
    INORGANIC = "inorganic"
    BOTH = "both"
    NONE = "none"


class PestManagementEnum(Enum):
    CHEMICAL = "chemical"
    BIOLOGICAL = "biological"
    INTEGRATED = "integrated"
    NONE = "none"


__all__ = [
    "LandholdingEnum",
    "WaterSourceEnum",
    "BudgetPerAcreEnum",
    "RiskAppetiteEnum",
    "CropCycleEnum",
    "CropRotationEnum",
    "IrrigationTypeEnum",
    "MarketAccessEnum",
    "OwnsLivestockEnum",
    "SmartphoneUseEnum",
    "MachineryUsedEnum",
    "StorageFacilityEnum",
    "TransportAccessEnum",
    "TemperatureRangeEnum",
    "AltitudeRangeEnum",
    "FertilizerUsedEnum",
    "PestManagementEnum",
]
