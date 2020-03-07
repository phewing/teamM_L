from enum import Enum, IntEnum, IntFlag


class Gender(IntEnum):
    MALE = 1
    FEMALE = 2


class Disease(IntEnum):
    # Cardiovascular diseases
    HEART_ATTACK = 1000
    STROKE = 1001
    HYPERTENSION = 1100
    HYPERCHOLESTEROLEMIA = 1101
    HEART_DISEASE = 1102

    # Neurological diseases
    ALZHEIMERS = 2100
    PARKINSONS_DISEASE = 2101
    DEMENTIA = 2102
    EPILEPSY = 2103

    # Cancers
    CANCER = 3100
    LUNG_CANCER = 3101
    MELANOMA = 3102
    UTERINE_CANCER = 3103
    STOMACH_CANCER = 3104
    LEUKEMIA = 3105
    BREAST_CANCER = 3106
    OVARIAN_CANCER = 3107
    PROSTATE_CANCER = 3108
    LIVER_CANCER = 3109
    FEMALE_CANCER = 3110

    # Endocrine diseases
    DIABETES_TYPE_1 = 4100
    DIABETES_TYPE_2 = 4101
    CYSTIC_FIBROSIS = 4102
    TAY_SACHS_DISEASE = 4103

    # Congenital genetic abnormalities, not elsewhere classified
    DOWN_SYNDROME = 5100

    # Immune disorders
    LUPUS = 6100
    GRAVES_DISEASE = 6101

    # Respiratory diseases
    EMPHYSEMA = 7100
    ASTHMA = 7101

    # Musculoskeletal System
    ACHONDROPLASIA = 8100
    FIBROMYALGIA = 8101
    RHEUMATOID_ARTHRITIS = 8102
    GOUT = 8103

    # Traumatic accidents
    FIRE = 9000
    SUICIDE = 9001
    KILLED_IN_ACTION = 9002
    PLANE_ACCIDENT = 9003
    ACCIDENT = 9004
    CAR_ACCIDENT = 9005

    # Neurodevelopmental/behavioral diseases
    AUTISM = 10100

    # Other/unclassified
    BLOOD_INFECTION = 11000
    INFECTION = 11001
    SIDS = 11002
    MIGRANES = 11100

    # Digestive diseases
    CIRRHOSIS_LIVER = 12100
    CROHNS_DISEASE = 12101

    # Skin diseases
    PSORIASIS = 13100
