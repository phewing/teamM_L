from __future__ import annotations

import json
import math
from uuid import uuid4
from typing import Optional, List, Dict, Tuple

import pandas
from numpy.core.multiarray import ndarray

from enums import *
from parsers import StepSequence, parse_relationship_text, StepDirection


def calculate_generation_from_path(path: StepSequence) -> int:
    generation = 0

    for step in path.items:
        if step.direction in (StepDirection.FATHER, StepDirection.MOTHER, ):
            generation += 1
        if step.direction == StepDirection.CHILD:
            generation -= 1

    return generation


class Person(object):
    file_number: int
    uuid: str
    is_root: bool
    relationship_to_self: str
    path: StepSequence
    sex: Gender
    is_living: bool
    label: str
    generation: int
    disease: Optional[Disease]
    disease_original: Optional[str]
    age_onset: Optional[int]
    age_death: Optional[int]
    mother: Optional[Person]
    father: Optional[Person]
    siblings: List[Person]
    children: List[Person]
    mate: Optional[Person]
    twin: Optional[Person]
    has_full_information: bool

    def __init__(self,
                 file_number: int,
                 uuid: str,
                 relationship_to_self: str,
                 sex: Gender,
                 is_living: bool,
                 disease: Optional[Disease],
                 disease_original: Optional[Disease],
                 age_onset: Optional[int],
                 age_death: Optional[int]
                 ):
        self.file_number = file_number
        self.uuid = uuid
        self.relationship_to_self = relationship_to_self
        self.path = parse_relationship_text(self.relationship_to_self)
        self.generation = calculate_generation_from_path(self.path)
        self.is_root = len(self.path.items) == 0
        self.sex = sex
        self.is_living = is_living
        self.disease = disease
        self.disease_original = disease_original
        self.label = self.relationship_to_self + ("\\n" + self.disease_original if self.disease_original else "")
        self.age_onset = age_onset
        self.age_death = age_death
        self.father = None
        self.mother = None
        self.mate = None
        self.children = []
        self.siblings = []
        self.twin = None
        self.has_full_information = False

    def set_father(self, father: Person):
        self.father = father

        if self.mother:
            self.mother.mate = father
            self.father.mate = self.mother
        if self not in father.children:
            father.children.append(self)

        for sibling in self.siblings:
            sibling.father = father
            if sibling not in father.children:
                father.children.append(sibling)

    def set_mother(self, mother: Person):
        self.mother = mother

        if self.father:
            self.father.mate = mother
            self.mother.mate = self.father
        if self not in mother.children:
            mother.children.append(self)

        for sibling in self.siblings:
            sibling.mother = mother
            if sibling not in mother.children:
                mother.children.append(sibling)

    def add_sibling(self, sibling: Person):
        self.siblings.append(sibling)
        if self not in sibling.siblings:
            sibling.siblings.append(self)

        if self.father:
            sibling.father = self.father
        if self.mother:
            sibling.mother = self.mother

        for otherSibling in self.siblings:
            if sibling != otherSibling and sibling not in otherSibling.siblings:
                otherSibling.add_sibling(sibling)

    def add_child(self, child: Person):
        self.children.append(child)
        if self.sex == Gender.MALE:
            child.father = self
        else:
            child.mother = self

        if self.sex == Gender.MALE:
            child.father = self

            if self.mate and child not in self.mate.children:
                self.mate.children.append(child)
                child.mother = self.mate
        else:
            child.mother = self
            if self.mate and child not in self.mate.children:
                self.mate.children.append(child)
                child.father = self.mate

    def set_mate(self, other: Person):
        self.mate = other
        other.mate = self
        for child in self.children:
            if child not in self.mate.children:
                self.mate.children.append(child)
        for child in self.mate.children:
            if child not in self.children:
                self.children.append(child)

    def fill_in_surrounding(self):
        # Basically, we know this node has all the information, so we want it to share it with surrounding nodes
        self.father.children.append(self)
        self.mother.children.append(self)
        self.father.mate = self.mother
        self.mother.mate = self.father
        for sibling in self.siblings:
            for otherSibling in self.siblings:
                if sibling != otherSibling and otherSibling not in sibling.siblings:
                    sibling.siblings.append(otherSibling)
            sibling.father = self.father
            if sibling not in self.father.children:
                self.father.children.append(sibling)
            sibling.mother = self.mother
            if sibling not in self.mother.children:
                self.mother.children.append(sibling)
        for child in self.children:
            for otherChild in self.children:
                if child != otherChild and otherChild not in child.siblings:
                    child.siblings.append(otherChild)
            if self.sex == Gender.MALE:
                child.father = self
                child.mother = self.mate
            else:
                child.mother = self
                child.father = self.mate

        # Mark surrounding nodes as being complete
        for child in self.children:
            child.has_full_information = True
        for sibling in self.siblings:
            sibling.has_full_information = True
        self.mother.has_full_information = True
        self.father.has_full_information = True
        self.mate.has_full_information = True

    def to_encodable_dict(self):
        return {
            "age_death": self.age_death,
            "age_onset": self.age_onset,
            "children": [child.uuid for child in self.children],
            "disease": self.disease,
            "father": self.father.uuid if self.father else None,
            "file_number": self.file_number,
            "generation": self.generation,
            "is_living": self.is_living,
            "is_root": self.is_root,
            "mate": self.mate.uuid if self.mate else None,
            "mother": self.mother.uuid if self.mother else None,
            # "path": str(self.path),
            "relationship_to_self": self.relationship_to_self,
            "sex": "M" if self.sex == Gender.MALE else "F",
            "siblings": [sibling.uuid for sibling in self.siblings],
            "twin": self.twin.uuid if self.twin else None,
            "uuid": self.uuid
        }


def ndarray_to_person(file_number: int, id_number: str, val: ndarray) -> Person:
    relation_original = val[0]  # self, mother, etc.
    sex_original = val[1]  # M, F
    is_living_original = val[2]  # Y, N
    disease_original = val[3]  # one of many diseases
    age_of_onset_original = val[4]
    age_of_death_original = val[5]

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
        id_number,
        relation_original,
        sex,
        is_living,
        disease,
        disease_original if type(disease_original) == str else None,
        age_of_onset,
        age_of_death
    )


def get_roots_and_people() -> Tuple[Dict[str, str], Dict[str, Person]]:
    people: Dict[str, Person] = {}

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

    roots: Dict[str, str] = {}

    # Load in our data
    for i, file_name in enumerate(file_names):
        df = pandas.read_csv('../All in the Family/All in the Family/' + file_name, sep="\t")

        people_needing_processed = []

        for j, value in enumerate(df.values):
            uuid = str(uuid4())
            person = ndarray_to_person(i + 1, uuid, value)

            if person.is_root:
                roots[str(i + 1)] = person.uuid

            people[uuid] = person
            people_needing_processed.append(people[uuid])

        root: Optional[Person] = None

        while len(people_needing_processed):
            did_pop_person = False

            for k, person in enumerate(people_needing_processed):
                if person.is_root:
                    root = person
                    people_needing_processed.pop(k)
                    did_pop_person = True
                    break

                if root is None:
                    continue

                current_node: Person = root
                did_connect_node = False
                for j, step in enumerate(person.path.items):
                    is_last_step = j == len(person.path.items) - 1

                    if is_last_step:
                        # If the attribute in the direction of our path is None and we are on the last step,
                        # then we have reached the edge of our tree and should add the leaf.
                        if step.direction == StepDirection.FATHER and current_node.father is None and is_last_step:
                            current_node.set_father(person)
                            did_connect_node = True
                        elif step.direction == StepDirection.MOTHER and current_node.mother is None and is_last_step:
                            current_node.set_mother(person)
                            did_connect_node = True
                        elif step.direction == StepDirection.SIBLING and person not in current_node.siblings and is_last_step:
                            current_node.add_sibling(person)
                            did_connect_node = True
                        elif step.direction == StepDirection.CHILD and person not in current_node.children and is_last_step:
                            current_node.add_child(person)
                            did_connect_node = True
                        elif step.direction == StepDirection.MATE and person.mate is None and is_last_step:
                            current_node.set_mate(person)
                            did_connect_node = True
                    else:
                        # Otherwise, we should traverse to the next step in our path
                        if step.direction == StepDirection.FATHER and current_node.father is not None:
                            current_node = current_node.father
                        elif step.direction == StepDirection.MOTHER and current_node.mother is not None:
                            current_node = current_node.mother
                        elif step.direction == StepDirection.MATE and current_node.mate is not None:
                            current_node = current_node.mate
                        elif step.direction == StepDirection.SIBLING and current_node.siblings[
                            step.index - 1] is not None:
                            current_node = current_node.siblings[step.index - 1]
                        elif step.direction == StepDirection.CHILD and current_node.children[
                            step.index - 1] is not None:
                            current_node = current_node.children[step.index - 1]

                if not did_connect_node:
                    continue
                else:
                    people_needing_processed.pop(k)
                    did_pop_person = True
                    break

            if not did_pop_person:
                raise Exception("Unable to processes any more people.")

    return roots, people


if __name__ == "__main__":
    roots, people = get_roots_and_people()

    encodings = {person.uuid: person.to_encodable_dict() for person in people.values()}

    output_data = {
        "roots": roots,
        "nodes": encodings
    }

    with open("output.json", "w") as f:
        f.write(json.dumps(output_data))
