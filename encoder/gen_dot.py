
import json
from typing import Dict, List

from encoder import get_roots_and_people, Person
from enums import Gender


def safe_uuid(uuid: str) -> str:
    return uuid.replace('-', '').replace(' ', '').lower()


def declare_male_node(id):
    return '{0} [shape=box, regular=1, color="blue"];'.format(id)


def generate_shape_text_from_person(person: Person) -> str:
    return f""""{person.relationship_to_self}" [shape={"oval" if person.sex == Gender.FEMALE else "box"}, regular=1, color="{"pink" if person.sex == Gender.FEMALE else "blue"}"];"""


def generate_points_text_from_male(person: Person) -> str:
    return f""""{safe_uuid(person.relationship_to_self)}+{safe_uuid(person.mate.relationship_to_self)}" [shape=point];"""


def generate_horizontal_lines_text_from_male(person: Person) -> str:
    return f""""{person.relationship_to_self}" -- "{safe_uuid(person.relationship_to_self)}+{safe_uuid(person.mate.relationship_to_self)}" -- "{person.mate.relationship_to_self}";"""


def generate_line_from_parent_to_child(father: Person, child: Person) -> str:
    return f""""{safe_uuid(father.relationship_to_self)}+{safe_uuid(father.mate.relationship_to_self)}" -- "{child.relationship_to_self}";"""


def generate_lines_from_parents_to_children(father: Person) -> str:
    return "\n".join([generate_line_from_parent_to_child(father, child) for child in father.children])


def write_dot(roots, people, tree_number: int, output_path: str):
    # Generate shapes
    people_in_tree = list(filter(lambda person: person.file_number == tree_number, people.values()))

    shapes_output = "\n".join([generate_shape_text_from_person(person) for person in people_in_tree])

    # Generate points
    males_in_tree_with_mate = list(filter(lambda person: person.sex == Gender.MALE and person.mate is not None,
                                     people_in_tree))
    points_output = "\n".join([generate_points_text_from_male(male) for male in males_in_tree_with_mate])

    # Generate lines from parents to children
    children_with_parents = list(filter(lambda person: person.father is not None or person.mother is not None, people_in_tree))
    parent_to_child_lines_output = "\n".join([generate_line_from_parent_to_child(child.father, child)
                                              for child in children_with_parents])

    # Generate lines between partners
    partner_line_output = "\n".join([generate_horizontal_lines_text_from_male(male) for male in males_in_tree_with_mate])

    # Generate ranks
    minimum_generation = min(map(lambda person: person.generation, people_in_tree))
    maximum_generation = max(map(lambda person: person.generation, people_in_tree))

    people_by_generation: Dict[str, List[Person]] = {}
    for generation in range(minimum_generation, maximum_generation + 1):
        people_in_generation: List[Person] = list(filter(lambda person: person.generation == generation, people_in_tree))
        people_by_generation[str(generation)] = people_in_generation

    for generation, people_in_generation in people_by_generation.items():
        ...

    output = f"""
graph f{tree_number} {{
{shapes_output}

{points_output}

{partner_line_output}

{parent_to_child_lines_output}
}}
    """

    with open(output_path, 'w') as f:
        f.write(output)

    return output

    dot_generations = {0: set()}
    dot_generations[0].add(roots[str(tree_number)])

    for ID in people:

        # Find the generations for each person in the target history...
        if (people[ID].file_number == tree_number) and (ID != roots[str(tree_number)]):
            this_generation = dot_generations.setdefault(people[ID].generation, set())
            this_generation.add(ID)

            # If the node has a spouse, add a union node between dist

            if people[ID].mate != None:
                this_generation.add("{0}_AND_{1}".format(*sorted([ID, people[ID].mate.uuid])))

        # Going generation-by-generation, declare the relations, as well as their connections

    for gen in reversed(sorted(dot_generations.keys())):
        pass

    # temporary result for debugging
    return dot_generations


if __name__ == "__main__":

    roots, people = get_roots_and_people()

    result = write_dot(roots, people, 16, 'out.gv')

    print(result)
