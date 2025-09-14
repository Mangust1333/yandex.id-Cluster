import uuid
import random
from datetime import date, timedelta
from faker import Faker

from ..db import session
from ..truncate import truncate_table
from .V2_models import (
    TimeZone, PersonalDataRecord, Gender, DriverLicense,
    DriverLicenseCategory, InternationalPassport, CompulsoryMedicalInsurance,
    BirthCertificate, VoluntaryMedicalInsurance, VehicleRegistrationCertificate,
    SocialInsuranceNumber, TaxpayerIdentificationNumber, Passport
)
from .V1_seed import UUID_USERS

faker = Faker("ru_RU")

def seed_time_zones():
    time_zones = []
    for i in range(1, 6):
        tz = TimeZone(
            time_zone_id=i,
            utc_offset=timedelta(hours=i - 3),
            city=faker.city()
        )
        time_zones.append(tz)
    session.bulk_save_objects(time_zones)
    session.commit()
    print("→ Засеяны часовые пояса")

def seed_personal_data_records():
    records = []
    for user_id in UUID_USERS:
        record = PersonalDataRecord(
            user_id=user_id,
            time_zone_id=random.randint(1, 5),
            name=faker.first_name(),
            surname=faker.last_name(),
            gender=random.choice([Gender.MALE, Gender.FEMALE]),
            birth_date=faker.date_of_birth(minimum_age=18, maximum_age=70),
            locality=faker.city(),
            nickname=faker.user_name()
        )
        records.append(record)
    session.bulk_save_objects(records)
    session.commit()
    print("→ Засеяны персональные данные")

def seed_driver_licenses():
    licenses = []
    for user_id in UUID_USERS:
        birth_date = faker.date_of_birth(minimum_age=18, maximum_age=60)
        issue_date = birth_date + timedelta(days=365 * 18)
        expiration_date = issue_date + timedelta(days=365 * 10)
        license = DriverLicense(
            user_id=user_id,
            number=faker.bothify(text='##########'),
            surname=faker.last_name(),
            latin_surname=faker.last_name().upper(),
            name=faker.first_name(),
            latin_name=faker.first_name().upper(),
            patronymic=faker.first_name(),
            latin_patronymic=faker.first_name().upper(),
            birth_date=birth_date,
            birth_place=faker.city(),
            latin_birth_place=faker.city().upper(),
            date_of_issue=issue_date,
            expiration_date=expiration_date,
            issued_by_whom=faker.company(),
            issued_by_whom_latin=faker.company().upper(),
            issue_place=faker.city(),
            issue_place_latin=faker.city().upper(),
            categories='B',
            special_marks=faker.text(max_nb_chars=100)
        )
        licenses.append(license)
    session.bulk_save_objects(licenses)
    session.commit()
    print("→ Засеяны водительские удостоверения")

def seed_driver_license_categories():
    categories = ['A', 'B', 'C', 'D', 'E']
    records = []
    for user_id in UUID_USERS:
        chosen = random.sample(categories, k=random.randint(1, 3))
        for cat in chosen:
            record = DriverLicenseCategory(
                driver_license_user_id=user_id,
                category=cat
            )
            records.append(record)
    session.bulk_save_objects(records)
    session.commit()
    print("→ Засеяны категории водительских удостоверений")

def seed_passports():
    records = []
    for user_id in UUID_USERS:
        birth_date = faker.date_of_birth(minimum_age=18, maximum_age=70)
        issue_date = birth_date + timedelta(days=365 * 14)
        p = Passport(
            user_id=user_id,
            seria=faker.bothify(text="####"),
            number=faker.bothify(text="######"),
            name=faker.first_name(),
            surname=faker.last_name(),
            patronymic=faker.first_name(),
            birth_date=birth_date,
            locality=faker.city(),
            gender=random.choice([Gender.MALE, Gender.FEMALE]),
            issued_by_whom=faker.company(),
            unit_code=faker.bothify(text="######"),
            date_of_issue=issue_date,
            registration_address=faker.address()
        )
        records.append(p)
    session.bulk_save_objects(records)
    session.commit()
    print("→ Засеяны паспорта")

def seed_international_passports():
    records = []
    for user_id in UUID_USERS:
        birth_date = faker.date_of_birth(minimum_age=18, maximum_age=70)
        issue_date = birth_date + timedelta(days=365 * 18)
        expiration_date = issue_date + timedelta(days=365 * 10)
        p = InternationalPassport(
            user_id=user_id,
            number=faker.bothify(text='#########'),
            surname=faker.last_name(),
            latin_surname=faker.last_name().upper(),
            name=faker.first_name(),
            latin_name=faker.first_name().upper(),
            patronymic=faker.first_name(),
            latin_patronymic=faker.first_name().upper(),
            nationality="Россия",
            latin_nationality="RUSSIA",
            birth_date=birth_date,
            birth_place=faker.city(),
            latin_birth_place=faker.city().upper(),
            gender=random.choice([Gender.MALE, Gender.FEMALE]),
            date_of_issue=issue_date,
            expiration_date=expiration_date,
            issued_by_whom=faker.company()
        )
        records.append(p)
    session.bulk_save_objects(records)
    session.commit()
    print("→ Засеяны заграничные паспорта")

def seed_compulsory_medical_insurances():
    records = []
    for user_id in UUID_USERS:
        birth_date = faker.date_of_birth(minimum_age=18, maximum_age=70)
        record = CompulsoryMedicalInsurance(
            user_id=user_id,
            number=faker.bothify(text="################"),
            surname=faker.last_name(),
            name=faker.first_name(),
            patronymic=faker.first_name(),
            birth_date=birth_date,
            gender=random.choice([Gender.MALE, Gender.FEMALE]),
            blank_number=faker.bothify(text="####"),
            blank_seria=faker.bothify(text="#######")
        )
        records.append(record)
    session.bulk_save_objects(records)
    session.commit()
    print("→ Засеяны полисы ОМС")

def seed_birth_certificates():
    records = []
    for user_id in UUID_USERS:
        birth_date = faker.date_of_birth(minimum_age=0, maximum_age=40)
        date_of_issue = birth_date + timedelta(days=5)
        record = BirthCertificate(
            user_id=user_id,
            seria=faker.bothify("##"),
            number=faker.bothify("######"),
            name=faker.first_name(),
            surname=faker.last_name(),
            patronymic=faker.first_name(),
            birth_date=birth_date,
            birth_place=faker.city(),
            birth_certificate_record_number=faker.bothify("##-##-######-#"),
            father_name=faker.first_name_male(),
            father_surname=faker.last_name(),
            father_patronymic=faker.first_name(),
            father_birth_date=faker.date_of_birth(minimum_age=40, maximum_age=70),
            father_nationality="Россия",
            mother_name=faker.first_name_female(),
            mother_surname=faker.last_name(),
            mother_patronymic=faker.first_name(),
            mother_birth_date=faker.date_of_birth(minimum_age=35, maximum_age=65),
            mother_nationality="Россия",
            state_registration_place=faker.city(),
            issue_certificate_place=faker.city(),
            date_of_issue=date_of_issue
        )
        records.append(record)
    session.bulk_save_objects(records)
    session.commit()
    print("→ Засеяны свидетельства о рождении")

def seed_voluntary_medical_insurances():
    records = []
    for user_id in UUID_USERS:
        birth_date = faker.date_of_birth(minimum_age=18, maximum_age=70)
        issue_date = date.today() - timedelta(days=365)
        expiration_date = issue_date + timedelta(days=365)
        record = VoluntaryMedicalInsurance(
            user_id=user_id,
            number=faker.bothify("################"),
            surname=faker.last_name(),
            name=faker.first_name(),
            patronymic=faker.first_name(),
            birth_date=birth_date,
            gender=random.choice([Gender.MALE, Gender.FEMALE]),
            date_of_issue=issue_date,
            expiration_date=expiration_date,
            insurer=faker.company()
        )
        records.append(record)
    session.bulk_save_objects(records)
    session.commit()
    print("→ Засеяны полисы ДМС")

def seed_vehicle_registration_certificates():
    records = []
    for user_id in UUID_USERS:
        manufacture_year = random.randint(2000, 2022)
        issue_date = date.today() - timedelta(days=365)
        record = VehicleRegistrationCertificate(
            user_id=user_id,
            seria=faker.bothify("####"),
            number=faker.bothify("######"),
            registration_number=faker.bothify("A###AA##"),
            vin=faker.bothify("#################"),
            brand="LADA",
            brand_latin="LADA",
            model="Vesta",
            model_latin="VESTA",
            vehicle_type="Легковой",
            vehicle_category="B",
            manufacture_year=manufacture_year,
            chassis_number=faker.bothify("CH#######"),
            body_number=faker.bothify("BD#######"),
            color=faker.color_name(),
            engine_power_kw=random.uniform(50, 150),
            engine_power_hp=random.uniform(70, 200),
            ec_class="EURO 5",
            max_allowed_weight=random.uniform(1500, 3000),
            curb_weight=random.uniform(1000, 2000),
            registration_expiration_date=issue_date + timedelta(days=365 * 5),
            pts_number=faker.bothify("##AA###########"),
            surname=faker.last_name(),
            surname_latin=faker.last_name().upper(),
            name=faker.first_name(),
            name_latin=faker.first_name().upper(),
            patronymic=faker.first_name(),
            registration_address=faker.address(),
            subdivision_code=faker.bothify("######"),
            issue_date=issue_date,
            special_marks="Нет"
        )
        records.append(record)
    session.bulk_save_objects(records)
    session.commit()
    print("→ Засеяны СТС")

def seed_social_insurance_numbers():
    records = []
    for user_id in UUID_USERS:
        birth_date = faker.date_of_birth(minimum_age=18, maximum_age=70)
        registration_date = birth_date + timedelta(days=365 * 18)
        record = SocialInsuranceNumber(
            user_id=user_id,
            snils=faker.bothify("###########"),
            surname=faker.last_name(),
            name=faker.first_name(),
            patronymic=faker.first_name(),
            birth_date=birth_date,
            gender=random.choice([Gender.MALE, Gender.FEMALE]),
            registration_date=registration_date
        )
        records.append(record)
    session.bulk_save_objects(records)
    session.commit()
    print("→ Засеяны СНИЛС")

def seed_taxpayer_identification_numbers():
    records = []
    for user_id in UUID_USERS:
        birth_date = faker.date_of_birth(minimum_age=18, maximum_age=70)
        date_of_issue = birth_date + timedelta(days=365 * 18)
        record = TaxpayerIdentificationNumber(
            user_id=user_id,
            inn=faker.bothify("############"),
            surname=faker.last_name(),
            name=faker.first_name(),
            patronymic=faker.first_name(),
            birth_date=birth_date,
            place_of_birth=faker.city(),
            gender=random.choice([Gender.MALE, Gender.FEMALE]),
            issuing_authority=faker.company(),
            date_of_issue=date_of_issue
        )
        records.append(record)
    session.bulk_save_objects(records)
    session.commit()
    print("→ Засеяны ИНН")


def run_seed(SEED_COUNT):
    truncate_table(TimeZone.__tablename__)
    truncate_table(PersonalDataRecord.__tablename__)
    truncate_table(DriverLicense.__tablename__)
    truncate_table(DriverLicenseCategory.__tablename__)
    truncate_table(Passport.__tablename__)
    truncate_table(InternationalPassport.__tablename__)
    truncate_table(CompulsoryMedicalInsurance.__tablename__)
    truncate_table(BirthCertificate.__tablename__)
    truncate_table(VoluntaryMedicalInsurance.__tablename__)
    truncate_table(VehicleRegistrationCertificate.__tablename__)
    truncate_table(SocialInsuranceNumber.__tablename__)
    truncate_table(TaxpayerIdentificationNumber.__tablename__)

    seed_time_zones()
    seed_personal_data_records()
    seed_driver_licenses()
    seed_driver_license_categories()
    seed_passports()
    seed_international_passports()
    seed_compulsory_medical_insurances()
    seed_birth_certificates()
    seed_voluntary_medical_insurances()
    seed_vehicle_registration_certificates()
    seed_social_insurance_numbers()
    seed_taxpayer_identification_numbers()
    print("Сидирование для V2 завершено.")