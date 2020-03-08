
import json
from encoder import get_roots_and_people

def declare_male_node(id):
    return '{0} [shape=box, regular=1, color="blue"];'.format(id)


def write_dot(roots, people, hist_num: int, output_path: str):

    dot_generations = {0: set()}
    dot_generations[0].add(roots[str(hist_num)])

    for ID in people:

        # Find the generations for each person in the target history...
        if (people[ID].file_number == hist_num) and (ID != roots[str(hist_num)]):
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

    result = write_dot(roots, people, 4, 'out.gv')

    print(result)
