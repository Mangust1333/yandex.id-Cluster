import enum
from sqlalchemy import (
    Column, Date, Enum, ForeignKey, CHAR, VARCHAR, SMALLINT, Float, Interval
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..db import Base

class Gender(enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

class TimeZone(Base):
    __tablename__ = 'time_zones'
    time_zone_id = Column(SMALLINT, primary_key=True)
    utc_offset = Column(Interval, nullable=False)
    city = Column(VARCHAR(100), nullable=False)
    
    personal_data = relationship("PersonalDataRecord", back_populates="time_zone")

class PersonalDataRecord(Base):
    __tablename__ = 'personal_data_records'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    time_zone_id = Column(SMALLINT, ForeignKey('time_zones.time_zone_id', ondelete='SET NULL'), nullable=False)
    name = Column(VARCHAR(39), nullable=False)
    surname = Column(VARCHAR(39), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    birth_date = Column(Date)
    locality = Column(VARCHAR(100))
    nickname = Column(VARCHAR(39), nullable=False)

    time_zone = relationship("TimeZone", back_populates="personal_data")

class DriverLicense(Base):
    __tablename__ = 'driver_licenses'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    number = Column(CHAR(10), nullable=False)
    surname = Column(VARCHAR(39))
    latin_surname = Column(VARCHAR(39))
    name = Column(VARCHAR(39))
    latin_name = Column(VARCHAR(39))
    patronymic = Column(VARCHAR(39))
    latin_patronymic = Column(VARCHAR(39))
    birth_date = Column(Date)
    birth_place = Column(VARCHAR(50))
    latin_birth_place = Column(VARCHAR(50))
    date_of_issue = Column(Date)
    expiration_date = Column(Date)
    issued_by_whom = Column(VARCHAR(100))
    issued_by_whom_latin = Column(VARCHAR(100))
    issue_place = Column(VARCHAR(100))
    issue_place_latin = Column(VARCHAR(100))
    categories = Column(VARCHAR(3), nullable=False)
    special_marks = Column(VARCHAR(255))

    categories_rel = relationship("DriverLicenseCategory", back_populates="license")

class DriverLicenseCategory(Base):
    __tablename__ = 'driver_license_categories'
    driver_license_user_id = Column(UUID(as_uuid=True), ForeignKey('driver_licenses.user_id', ondelete='CASCADE'), primary_key=True)
    category = Column(VARCHAR(5), primary_key=True)

    license = relationship("DriverLicense", back_populates="categories_rel")

class InternationalPassport(Base):
    __tablename__ = 'international_passports'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    number = Column(CHAR(9), nullable=False)
    surname = Column(VARCHAR(39))
    latin_surname = Column(VARCHAR(39))
    name = Column(VARCHAR(39))
    latin_name = Column(VARCHAR(39))
    patronymic = Column(VARCHAR(39))
    latin_patronymic = Column(VARCHAR(39))
    nationality = Column(VARCHAR(50))
    latin_nationality = Column(VARCHAR(50))
    birth_date = Column(Date)
    birth_place = Column(VARCHAR(50))
    latin_birth_place = Column(VARCHAR(50))
    gender = Column(Enum(Gender))
    date_of_issue = Column(Date)
    expiration_date = Column(Date)
    issued_by_whom = Column(VARCHAR(100))

class CompulsoryMedicalInsurance(Base):
    __tablename__ = 'compulsory_medical_insurances'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    number = Column(CHAR(16), nullable=False)
    surname = Column(VARCHAR(39))
    name = Column(VARCHAR(39))
    patronymic = Column(VARCHAR(39))
    birth_date = Column(Date)
    gender = Column(Enum(Gender))
    blank_number = Column(CHAR(4))
    blank_seria = Column(CHAR(7))

class BirthCertificate(Base):
    __tablename__ = 'birth_certificates'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    seria = Column(CHAR(2), nullable=False)
    number = Column(CHAR(6), nullable=False)
    name = Column(VARCHAR(39))
    surname = Column(VARCHAR(39))
    patronymic = Column(VARCHAR(39))
    birth_date = Column(Date)
    birth_place = Column(VARCHAR(50))
    birth_certificate_record_number = Column(CHAR(21))
    father_name = Column(VARCHAR(39))
    father_surname = Column(VARCHAR(39))
    father_patronymic = Column(VARCHAR(39))
    father_birth_date = Column(Date)
    father_nationality = Column(VARCHAR(50))
    mother_name = Column(VARCHAR(39))
    mother_surname = Column(VARCHAR(39))
    mother_patronymic = Column(VARCHAR(39))
    mother_birth_date = Column(Date)
    mother_nationality = Column(VARCHAR(50))
    state_registration_place = Column(VARCHAR(50))
    issue_certificate_place = Column(VARCHAR(50))
    date_of_issue = Column(Date)

class VoluntaryMedicalInsurance(Base):
    __tablename__ = 'voluntary_medical_insurances'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    number = Column(CHAR(16), nullable=False)
    surname = Column(VARCHAR(39))
    name = Column(VARCHAR(39))
    patronymic = Column(VARCHAR(39))
    birth_date = Column(Date)
    gender = Column(Enum(Gender))
    date_of_issue = Column(Date)
    expiration_date = Column(Date)
    insurer = Column(VARCHAR(100))

class VehicleRegistrationCertificate(Base):
    __tablename__ = 'vehicle_registration_certificates'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    seria = Column(CHAR(4), nullable=False)
    number = Column(CHAR(6), nullable=False)
    registration_number = Column(CHAR(8))
    vin = Column(CHAR(17))
    brand = Column(VARCHAR(50))
    brand_latin = Column(VARCHAR(50))
    model = Column(VARCHAR(50))
    model_latin = Column(VARCHAR(50))
    vehicle_type = Column(VARCHAR(50))
    vehicle_category = Column(VARCHAR(50))
    manufacture_year = Column(SMALLINT)
    chassis_number = Column(VARCHAR(17))
    body_number = Column(VARCHAR(17))
    color = Column(VARCHAR(20))
    engine_power_kw = Column(Float)
    engine_power_hp = Column(Float)
    ec_class = Column(VARCHAR(20))
    max_allowed_weight = Column(Float)
    curb_weight = Column(Float)
    registration_expiration_date = Column(Date)
    pts_number = Column(CHAR(15))
    surname = Column(VARCHAR(39))
    surname_latin = Column(VARCHAR(39))
    name = Column(VARCHAR(39))
    name_latin = Column(VARCHAR(39))
    patronymic = Column(VARCHAR(39))
    registration_address = Column(VARCHAR(100))
    subdivision_code = Column(CHAR(6))
    issue_date = Column(Date)
    special_marks = Column(VARCHAR(255))

class SocialInsuranceNumber(Base):
    __tablename__ = 'social_insurance_numbers'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    snils = Column(CHAR(11), nullable=False)
    surname = Column(VARCHAR(39))
    name = Column(VARCHAR(50))
    patronymic = Column(VARCHAR(50))
    birth_date = Column(Date)
    gender = Column(Enum(Gender))
    registration_date = Column(Date)

class TaxpayerIdentificationNumber(Base):
    __tablename__ = 'taxpayer_identification_numbers'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    inn = Column(CHAR(12), nullable=False)
    surname = Column(VARCHAR(39))
    name = Column(VARCHAR(39))
    patronymic = Column(VARCHAR(39))
    birth_date = Column(Date)
    place_of_birth = Column(VARCHAR(50))
    gender = Column(Enum(Gender))
    issuing_authority = Column(VARCHAR(100))
    date_of_issue = Column(Date)

class Passport(Base):
    __tablename__ = 'passports'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    seria = Column(CHAR(4), nullable=False)
    number = Column(CHAR(6), nullable=False)
    name = Column(VARCHAR(39))
    surname = Column(VARCHAR(39))
    patronymic = Column(VARCHAR(39))
    birth_date = Column(Date)
    locality = Column(VARCHAR(100))
    gender = Column(Enum(Gender))
    issued_by_whom = Column(VARCHAR(100))
    unit_code = Column(CHAR(6))
    date_of_issue = Column(Date)
    registration_address = Column(VARCHAR(100))
