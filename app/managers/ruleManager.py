import sqlalchemy as db
from sqlalchemy.orm import relationship, declared_attr

from SharedBackend.managers import BaseSchema, GenericManager
from utils.constants import (
    LandholdingEnum,
    WaterSourceEnum,
    IrrigationTypeEnum,
    BudgetPerAcreEnum,
    MarketAccessEnum,
    RiskAppetiteEnum,
    CropCycleEnum,
    CropRotationEnum,
    OwnsLivestockEnum,
    SmartphoneUseEnum,
    MachineryUsedEnum,
    StorageFacilityEnum,
    TransportAccessEnum,
    TemperatureRangeEnum,
    AltitudeRangeEnum,
    FertilizerUsedEnum,
    PestManagementEnum,
)


class CropSchema(BaseSchema):
    __tablename__ = 'crops'

    # Basic crop information
    name = db.Column(db.String, nullable=False, unique=True)
    scientific_name = db.Column(db.String, nullable=True)
    crop_type = db.Column(db.String, nullable=False)  # e.g., Cereal, Pulse, Vegetable, etc.
    season = db.Column(db.JSON, nullable=False)  # Multiple seasons possible

    # Growing conditions
    min_temperature = db.Column(db.Float, nullable=False)
    max_temperature = db.Column(db.Float, nullable=False)
    min_rainfall = db.Column(db.Float, nullable=False)  # in mm
    max_rainfall = db.Column(db.Float, nullable=False)  # in mm
    soil_type = db.Column(db.JSON, nullable=False)
    ph_min = db.Column(db.Float, nullable=False)
    ph_max = db.Column(db.Float, nullable=False)

    # Cultivation metadata
    growing_duration = db.Column(db.Integer, nullable=False)  # days
    water_requirement = db.Column(db.String, nullable=False)  # Low, Medium, High
    fertilizer_requirement = db.Column(db.String, nullable=False)  # Low, Medium, High
    pest_susceptibility = db.Column(db.String, nullable=False)  # Low, Medium, High
    disease_susceptibility = db.Column(db.String, nullable=False)  # Low, Medium, High

    # Economic metadata
    average_yield = db.Column(db.Float, nullable=False)  # tons per hectare
    market_price_min = db.Column(db.Float, nullable=False)  # price per kg
    market_price_max = db.Column(db.Float, nullable=False)  # price per kg
    storage_life = db.Column(db.Integer, nullable=True)  # days


class RuleSchema(BaseSchema):
    __tablename__ = "rules"

    # Farm characteristics
    total_farmland_area = db.Column(db.Enum(LandholdingEnum), nullable=False)
    primary_water_source = db.Column(db.Enum(WaterSourceEnum), nullable=False)
    irrigation_available = db.Column(db.Boolean, nullable=False)
    irrigation_type = db.Column(db.Enum(IrrigationTypeEnum), nullable=False)

    # Economic factors
    budget_per_acre = db.Column(db.Enum(BudgetPerAcreEnum), nullable=False)
    market_access = db.Column(db.Enum(MarketAccessEnum), nullable=False)
    preferred_crop_type = db.Column(db.String, nullable=True)

    # Risk and management
    risk_appetite = db.Column(db.Enum(RiskAppetiteEnum), nullable=False)
    fertilizer_used = db.Column(db.Enum(FertilizerUsedEnum), nullable=False)
    pest_management = db.Column(db.Enum(PestManagementEnum), nullable=False)

    # Farming practices
    crop_cycle = db.Column(db.Enum(CropCycleEnum), nullable=False)
    rotation_intercropping = db.Column(db.Enum(CropRotationEnum), nullable=False)

    # Additional resources
    owns_livestock = db.Column(db.Enum(OwnsLivestockEnum), nullable=False)
    livestock_type = db.Column(db.String, nullable=True)
    smartphone_use = db.Column(db.Enum(SmartphoneUseEnum), nullable=False)
    machinery_used = db.Column(db.Enum(MachineryUsedEnum), nullable=False)
    storage_facility = db.Column(db.Enum(StorageFacilityEnum), nullable=False)
    transport_access = db.Column(db.Enum(TransportAccessEnum), nullable=False)

    # Environmental conditions
    temperature_range = db.Column(db.Enum(TemperatureRangeEnum), nullable=False)
    altitude_range = db.Column(db.Enum(AltitudeRangeEnum), nullable=False)

    # Recommendation
    recommended_rabi_crops_rel = relationship(
        lambda: CropSchema,
        secondary=lambda: rabi_crop_rules,
        uselist=True,
    )
    recommended_summer_crops_rel = relationship(
        lambda: CropSchema,
        secondary=lambda: summer_crop_rules,
        uselist=True,
    )

    # Relationships
    primary_crop_uid = db.Column(db.String, db.ForeignKey(CropSchema.uid), nullable=True)

    @classmethod
    @declared_attr
    def primary_crop_rel(cls):
        return relationship(
            CropSchema,
            foreign_keys=[cls.primary_crop_uid],
            uselist=False,
        )


# Association tables for many-to-many relationships
rabi_crop_rules = db.Table(
    'rabi_crop_rules',
    BaseSchema.metadata,
    db.Column('rule_id', db.String, db.ForeignKey(RuleSchema.uid), primary_key=True),
    db.Column('crop_id', db.String, db.ForeignKey(CropSchema.uid), primary_key=True),
)

summer_crop_rules = db.Table(
    'summer_crop_rules',
    BaseSchema.metadata,
    db.Column('rule_id', db.String, db.ForeignKey(RuleSchema.uid), primary_key=True),
    db.Column('crop_id', db.String, db.ForeignKey(CropSchema.uid), primary_key=True),
)


class RuleManager(GenericManager[RuleSchema]):
    pass


class CropManager(GenericManager[CropSchema]):
    pass


__all__ = [
    "RuleSchema", "RuleManager",
    "CropSchema", "CropManager",
]
