from __future__ import annotations

import math
from typing import Optional, List

from numpy.core.multiarray import ndarray

from enums import *

import pandas


class Person(object):
    file_number: int
    is_root: bool
    sex: Gender
    is_living: bool
    disease: Optional[Disease]
    age_onset: Optional[int]
    age_death: Optional[int]
    mother: Optional[Person]
    father: Optional[Person]
    siblings: List[Person]
    children: List[Person]
    twin: Optional[Person]

    def __init__(self,
                 file_number: int,
                 is_root: bool,
                 sex: Gender,
                 is_living: bool,
                 disease: Optional[Disease],
                 age_onset: Optional[int],
                 age_death: Optional[int],
                 twin: Optional[Person]
                 ):
        self.file_number = file_number
        self.is_root = is_root
        self.sex = sex
        self.is_living = is_living
        self.disease = disease
        self.age_onset = age_onset
        self.age_death = age_death
        self.twin = twin

    def __sub__(self, other: Person) -> float:
        return self.compare(other)

    def compare(self, other: Person) -> float:
        sex_difference = other.sex - self.sex

        return float(sex_difference)

    def set_father(self, other: Person):
        self.father = other
        if self not in other.children:
            other.children.append(self)

    def set_mother(self, other: Person):
        self.mother = other
        if self not in other.children:
            other.children.append(self)

    def add_sibling(self, other: Person):
        self.siblings.append(self)
        if self not in other.siblings:
            other.siblings.append(self)

    def add_child(self, other: Person):
        self.children.append(other)
        if self.sex == Gender.MALE:
            other.father = self
        else:
            other.mother = self


def ndarray_to_person(file_number: int, val: ndarray) -> Person:
    relation_original = val[0]  # self, mother, etc.
    sex_original = val[1]  # M, F
    is_living_original = val[2]  # Y, N
    disease_original = val[3]  # one of many diseases
    age_of_onset_original = val[4]
    age_of_death_original = val[5]

    is_root = relation_original == "Self"

    if sex_original == "M":
        sex = Gender.MALE
    elif sex_original == "F":
        sex = Gender.FEMALE
    else:
        raise ValueError

    if is_living_original == "Y":
        is_living = True
    elif is_living_original == "N":
        is_living = False
    elif type(is_living_original) == float and math.isnan(is_living_original):
        is_living = True
    else:
        raise ValueError

    if math.isnan(age_of_onset_original):
        age_of_onset = None
    else:
        age_of_onset = int(age_of_onset_original)

    if math.isnan(age_of_death_original):
        age_of_death = None
    else:
        age_of_death = int(age_of_death_original)

    if type(disease_original) == float and math.isnan(disease_original):
        disease = None
    elif disease_original == "Heart Attack":
        disease = Disease.HEART_ATTACK
    elif disease_original == "Stroke":
        disease = Disease.STROKE
    elif disease_original == "Hypertension":
        disease = Disease.HYPERTENSION
    elif disease_original == "Alzheimer's Disease":
        disease = Disease.ALZHEIMERS
    elif disease_original == "Lung Cancer":
        disease = Disease.LUNG_CANCER
    elif disease_original == "Parkinson's Disease":
        disease = Disease.PARKINSONS_DISEASE
    elif disease_original == "Fire":
        disease = Disease.FIRE
    elif disease_original == "Melanoma":
        disease = Disease.MELANOMA
    elif disease_original == "Dementia":
        disease = Disease.DEMENTIA
    elif disease_original == "Uterine Cancer":
        disease = Disease.UTERINE_CANCER
    elif disease_original == "Cancer":
        disease = Disease.CANCER
    elif disease_original == "Type 1 Diabetes":
        disease = Disease.DIABETES_TYPE_1
    elif disease_original == "Suicide":
        disease = Disease.SUICIDE
    elif disease_original == "Type 2 Diabetes":
        disease = Disease.DIABETES_TYPE_2
    elif disease_original == "Killed in Action":
        disease = Disease.KILLED_IN_ACTION
    elif disease_original == "Plane Accident":
        disease = Disease.PLANE_ACCIDENT
    elif disease_original == "Stomach Cancer":
        disease = Disease.STOMACH_CANCER
    elif disease_original == "Achondroplasia":
        disease = Disease.ACHONDROPLASIA
    elif disease_original == "Hypercholesterolemia":
        disease = Disease.HYPERCHOLESTEROLEMIA
    elif disease_original == "SIDS":
        disease = Disease.SIDS
    elif disease_original == "Lupus":
        disease = Disease.LUPUS
    elif disease_original == "HTN":
        disease = Disease.HYPERTENSION
    elif disease_original == "Accident":
        disease = Disease.ACCIDENT
    elif disease_original == "Heart Disease":
        disease = Disease.HEART_DISEASE
    elif disease_original == "Leukemia":
        disease = Disease.LEUKEMIA
    elif disease_original == "Breast Cancer":
        disease = Disease.BREAST_CANCER
    elif disease_original == "Ovarian Cancer":
        disease = Disease.OVARIAN_CANCER
    elif disease_original == "Prostate Cancer":
        disease = Disease.PROSTATE_CANCER
    elif disease_original == "Cystic Fibrosis":
        disease = Disease.CYSTIC_FIBROSIS
    elif disease_original == "Emphysema":
        disease = Disease.EMPHYSEMA
    elif disease_original == "Grave's Disease":
        disease = Disease.GRAVES_DISEASE
    elif disease_original == "Rheumatoid Arthritis":
        disease = Disease.RHEUMATOID_ARTHRITIS
    elif disease_original == "Seizures":
        disease = Disease.EPILEPSY
    elif disease_original == "Fibromyalgia":
        disease = Disease.FIBROMYALGIA
    elif disease_original == "Gout":
        disease = Disease.GOUT
    elif disease_original == "Down Syndrome":
        disease = Disease.DOWN_SYNDROME
    elif disease_original == "High Cholesterol":
        disease = Disease.HYPERCHOLESTEROLEMIA
    elif disease_original == "Autism":
        disease = Disease.AUTISM
    elif disease_original == "Migranes":
        disease = Disease.MIGRANES
    elif disease_original == "Car Accident":
        disease = Disease.CAR_ACCIDENT
    elif disease_original == "Blood Infection":
        disease = Disease.BLOOD_INFECTION
    elif disease_original == "Cirrhosis of the Liver":
        disease = Disease.CIRRHOSIS_LIVER
    elif disease_original == "Asthma":
        disease = Disease.ASTHMA
    elif disease_original == "Infection":
        disease = Disease.INFECTION
    elif disease_original == "Crohn's Disease":
        disease = Disease.CROHNS_DISEASE
    elif disease_original == "Psoriasis":
        disease = Disease.PSORIASIS
    elif disease_original == "Liver Cancer":
        disease = Disease.LIVER_CANCER
    elif disease_original == "Epilepsy":
        disease = Disease.EPILEPSY
    elif disease_original == "Tay Sachs Disease":
        disease = Disease.TAY_SACHS_DISEASE
    elif disease_original == "Female Cancer":
        disease = Disease.FEMALE_CANCER
    else:
        raise ValueError(disease_original)

    return Person(
        file_number,
        is_root,
        sex,
        is_living,
        disease,
        age_of_onset,
        age_of_death
    )


people: List[Person] = []


file_names = [
    "F1.txt",
    "F2.txt",
    "F3.txt",
    "F4.txt",
    "F5.txt",
    "F6.txt",
    "F7.txt",
    "F8.txt",
    "F9.txt",
    "F10.txt",
    "F11.txt",
    "F12.txt",
    "F13.txt",
    "F14.txt",
    "F15.txt",
    "F16.txt",
    "F17.txt",
    "F18.txt",
    "F19.txt",
    "F20.txt"
]


for i, file_name in enumerate(file_names):
    df = pandas.read_csv('../All in the Family/All in the Family/' + file_name, sep="\t")

    for value in df.values:
        people.append(ndarray_to_person(i + 1, value))

pass
