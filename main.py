import random
from tabulate import tabulate


def calculate_target_value(sample, matrix):
    target_value = sum(matrix[sample[j] - 1][sample[j + 1] - 1] for j in range(len(sample) - 1))
    target_value += matrix[sample[-1] - 1][sample[0] - 1]
    return target_value


def get_remaining_indices(sample, indices):
    remaining_indices = []
    for i in range(len(sample)):
        if i not in indices:
            remaining_indices.append(i)
    return remaining_indices


def mutate(child, child_number):
    mutation = 0.01
    if random.random() < mutation:
        print(f"Произошла мутация в ребенке {child_number}!")
        print("Был:", child)
        idx1, idx2 = random.sample(range(len(child)), 2)
        child[idx1], child[idx2] = child[idx2], child[idx1]
    return child


def main():
    matrix = [[0, 1, 1, 5, 3],
              [1, 0, 3, 1, 5],
              [1, 3, 0, 11, 1],
              [5, 1, 11, 0, 1],
              [3, 5, 1, 1, 0]]

    original_sample = []
    while len(original_sample) < 4:
        new_individual = random.sample([1, 2, 3, 4, 5], 5)
        if new_individual not in original_sample:
            original_sample.append(new_individual)

    parent_table = [["номер строки исходной выборки", "код", "значение целевой функции"]]
    for i, sample in enumerate(original_sample, 1):
        target_value = calculate_target_value(sample, matrix)
        parent_table.append([i, sample, target_value])

    print("Текущее поколение:")
    print(tabulate(parent_table, headers="firstrow", tablefmt="grid"))

    parents_indices = random.sample(range(len(original_sample)), 2)
    remaining_indices = get_remaining_indices(original_sample, parents_indices)

    print("Выбранные пары родителей:", [(i + 1) for i in sorted(parents_indices)],
          [(j + 1) for j in sorted(remaining_indices)])

    couple1_1 = original_sample[parents_indices[0]]
    couple1_2 = original_sample[parents_indices[1]]

    couple2_1 = original_sample[remaining_indices[0]]
    couple2_2 = original_sample[remaining_indices[1]]

    cut_points1 = sorted(random.sample(range(1, len(couple1_1)), 2))

    fragment1_1 = couple1_1[:cut_points1[0]]
    fragment1_2 = couple1_1[cut_points1[0]:cut_points1[1]]
    fragment1_3 = couple1_1[cut_points1[1]:]

    # print("couple1_1:", couple1_1)
    # print("Фрагменты couple1_1:", fragment1_1, fragment1_2, fragment1_3)

    fragment2_1 = couple1_2[:cut_points1[0]]
    fragment2_2 = couple1_2[cut_points1[0]:cut_points1[1]]
    fragment2_3 = couple1_2[cut_points1[1]:]

    # print("couple1_2:", couple1_2)
    # print("Фрагменты couple1_2:", fragment2_1, fragment2_2, fragment2_3)

    cut_points2 = sorted(random.sample(range(1, len(couple2_1)), 2))

    fragment3_1 = couple2_1[:cut_points2[0]]
    fragment3_2 = couple2_1[cut_points2[0]:cut_points2[1]]
    fragment3_3 = couple2_1[cut_points2[1]:]

    # print("couple2_1:", couple2_1)
    # print("Фрагменты couple2_1:", fragment3_1, fragment3_2, fragment3_3)

    fragment4_1 = couple2_2[:cut_points2[0]]
    fragment4_2 = couple2_2[cut_points2[0]:cut_points2[1]]
    fragment4_3 = couple2_2[cut_points2[1]:]

    # print("couple2_2:", couple2_2)
    # print("Фрагменты couple2_2:", fragment4_1, fragment4_2, fragment4_3)

    child1 = [[], fragment2_2, []]
    for gene in couple1_1[cut_points1[0] + 1:] + couple1_1[:cut_points1[0] + 1]:
        if gene not in (child1[0] + child1[1] + child1[2]):
            if len(child1[2]) < len(fragment1_3):
                child1[2].append(gene)
            else:
                child1[0].append(gene)
    child1 = mutate(child1[0] + child1[1] + child1[2], 1)
    # print("Child 1:", child1)

    child2 = [[], fragment1_2, []]
    for gene in couple1_2[cut_points1[0] + 1:] + couple1_2[:cut_points1[0] + 1]:
        if gene not in (child2[0] + child2[1] + child2[2]):
            if len(child2[2]) < len(fragment2_3):
                child2[2].append(gene)
            else:
                child2[0].append(gene)
    child2 = mutate(child2[0] + child2[1] + child2[2], 2)
    # print("Child 2:", child2)

    child3 = [[], fragment4_2, []]
    for gene in couple2_1[cut_points2[0] + 1:] + couple2_1[:cut_points2[0] + 1]:
        if gene not in (child3[0] + child3[1] + child3[2]):
            if len(child3[2]) < len(fragment3_3):
                child3[2].append(gene)
            else:
                child3[0].append(gene)
    child3 = mutate(child3[0] + child3[1] + child3[2], 3)
    # print("Child 3:", child3)

    child4 = [[], fragment3_2, []]
    for gene in couple2_2[cut_points2[0] + 1:] + couple2_2[:cut_points2[0] + 1]:
        if gene not in (child4[0] + child4[1] + child4[2]):
            if len(child4[2]) < len(fragment4_3):
                child4[2].append(gene)
            else:
                child4[0].append(gene)
    child4 = mutate(child4[0] + child4[1] + child4[2], 4)
    # print("Child 4:", child4)

    child1_target_value = calculate_target_value(child1, matrix)
    child2_target_value = calculate_target_value(child2, matrix)
    child3_target_value = calculate_target_value(child3, matrix)
    child4_target_value = calculate_target_value(child4, matrix)

    table_children = [["номер родителя", "родитель", "потомок", "значение функции для потомка"]]
    table_children.append(
        [parents_indices[0] + 1, [fragment1_1, fragment1_2, fragment1_3], child1, child1_target_value])
    table_children.append(
        [parents_indices[1] + 1, [fragment2_1, fragment2_2, fragment2_3], child2, child2_target_value])
    table_children.append(
        [remaining_indices[0] + 1, [fragment3_1, fragment3_2, fragment3_3], child3, child3_target_value])
    table_children.append(
        [remaining_indices[1] + 1, [fragment4_1, fragment4_2, fragment4_3], child4, child4_target_value])

    print(tabulate(table_children, headers="firstrow", tablefmt="grid"))

    all_individuals = parent_table[1:] + [
        ['N', child1, child1_target_value],
        ['N', child2, child2_target_value],
        ['N', child3, child3_target_value],
        ['N', child4, child4_target_value]
    ]

    sorted_individuals = sorted(all_individuals, key=lambda x: x[2])

    best_individuals = sorted_individuals[0:4]

    best_individuals_table = [["Номер строки", "Код", "Значение целевой функции",
                                                    "Вероятность участия в размножении"]]
    for ind in best_individuals:
        target_value = ind[2]
        reproduction_probability = (best_individuals[0][2] + best_individuals[3][2] - target_value) / sum(
            best_individuals[i][2] for i in range(4))

        row = [ind[0], ind[1], target_value, reproduction_probability]
        best_individuals_table.append(row)

    print("Популяция поколения после отсичения худших особей:\n", tabulate(best_individuals_table, headers="firstrow", tablefmt="grid"))

    number_of_repetitions = 10
    counter = 0
    while counter < number_of_repetitions:
        counter += 1
        original_sample = [best_individuals[i][1] for i in range(4)]
        parent_table = [["номер строки исходной выборки", "код", "значение целевой функции"]]
        for i, sample in enumerate(original_sample, 1):
            target_value = calculate_target_value(sample, matrix)
            parent_table.append([i, sample, target_value])

        print("Текущее поколение:")
        print(tabulate(parent_table, headers="firstrow", tablefmt="grid"))

        parents_indices = random.sample(range(len(original_sample)), 2)
        remaining_indices = get_remaining_indices(original_sample, parents_indices)

        print("Выбранные пары родителей:", [(i + 1) for i in sorted(parents_indices)],
              [(j + 1) for j in sorted(remaining_indices)])

        couple1_1 = original_sample[parents_indices[0]]
        couple1_2 = original_sample[parents_indices[1]]

        couple2_1 = original_sample[remaining_indices[0]]
        couple2_2 = original_sample[remaining_indices[1]]

        cut_points1 = sorted(random.sample(range(1, len(couple1_1)), 2))

        fragment1_1 = couple1_1[:cut_points1[0]]
        fragment1_2 = couple1_1[cut_points1[0]:cut_points1[1]]
        fragment1_3 = couple1_1[cut_points1[1]:]

        # print("couple1_1:", couple1_1)
        # print("Фрагменты couple1_1:", fragment1_1, fragment1_2, fragment1_3)

        fragment2_1 = couple1_2[:cut_points1[0]]
        fragment2_2 = couple1_2[cut_points1[0]:cut_points1[1]]
        fragment2_3 = couple1_2[cut_points1[1]:]

        # print("couple1_2:", couple1_2)
        # print("Фрагменты couple1_2:", fragment2_1, fragment2_2, fragment2_3)

        cut_points2 = sorted(random.sample(range(1, len(couple2_1)), 2))

        fragment3_1 = couple2_1[:cut_points2[0]]
        fragment3_2 = couple2_1[cut_points2[0]:cut_points2[1]]
        fragment3_3 = couple2_1[cut_points2[1]:]

        # print("couple2_1:", couple2_1)
        # print("Фрагменты couple2_1:", fragment3_1, fragment3_2, fragment3_3)

        fragment4_1 = couple2_2[:cut_points2[0]]
        fragment4_2 = couple2_2[cut_points2[0]:cut_points2[1]]
        fragment4_3 = couple2_2[cut_points2[1]:]

        # print("couple2_2:", couple2_2)
        # print("Фрагменты couple2_2:", fragment4_1, fragment4_2, fragment4_3)

        child1 = [[], fragment2_2, []]
        for gene in couple1_1[cut_points1[0] + 1:] + couple1_1[:cut_points1[0] + 1]:
            if gene not in (child1[0] + child1[1] + child1[2]):
                if len(child1[2]) < len(fragment1_3):
                    child1[2].append(gene)
                else:
                    child1[0].append(gene)
        child1 = mutate(child1[0] + child1[1] + child1[2], 1)
        # print("Child 1:", child1)

        child2 = [[], fragment1_2, []]
        for gene in couple1_2[cut_points1[0] + 1:] + couple1_2[:cut_points1[0] + 1]:
            if gene not in (child2[0] + child2[1] + child2[2]):
                if len(child2[2]) < len(fragment2_3):
                    child2[2].append(gene)
                else:
                    child2[0].append(gene)
        child2 = mutate(child2[0] + child2[1] + child2[2], 2)
        # print("Child 2:", child2)

        child3 = [[], fragment4_2, []]
        for gene in couple2_1[cut_points2[0] + 1:] + couple2_1[:cut_points2[0] + 1]:
            if gene not in (child3[0] + child3[1] + child3[2]):
                if len(child3[2]) < len(fragment3_3):
                    child3[2].append(gene)
                else:
                    child3[0].append(gene)
        child3 = mutate(child3[0] + child3[1] + child3[2], 3)
        # print("Child 3:", child3)

        child4 = [[], fragment3_2, []]
        for gene in couple2_2[cut_points2[0] + 1:] + couple2_2[:cut_points2[0] + 1]:
            if gene not in (child4[0] + child4[1] + child4[2]):
                if len(child4[2]) < len(fragment4_3):
                    child4[2].append(gene)
                else:
                    child4[0].append(gene)
        child4 = mutate(child4[0] + child4[1] + child4[2], 4)
        # print("Child 4:", child4)

        child1_target_value = calculate_target_value(child1, matrix)
        child2_target_value = calculate_target_value(child2, matrix)
        child3_target_value = calculate_target_value(child3, matrix)
        child4_target_value = calculate_target_value(child4, matrix)

        table_children = [["номер родителя", "родитель", "потомок", "значение функции для потомка"]]
        table_children.append(
            [parents_indices[0] + 1, [fragment1_1, fragment1_2, fragment1_3], child1, child1_target_value])
        table_children.append(
            [parents_indices[1] + 1, [fragment2_1, fragment2_2, fragment2_3], child2, child2_target_value])
        table_children.append(
            [remaining_indices[0] + 1, [fragment3_1, fragment3_2, fragment3_3], child3, child3_target_value])
        table_children.append(
            [remaining_indices[1] + 1, [fragment4_1, fragment4_2, fragment4_3], child4, child4_target_value])

        print(tabulate(table_children, headers="firstrow", tablefmt="grid"))

        all_individuals = parent_table[1:] + [
            ['N', child1, child1_target_value],
            ['N', child2, child2_target_value],
            ['N', child3, child3_target_value],
            ['N', child4, child4_target_value]
        ]

        sorted_individuals = sorted(all_individuals, key=lambda x: x[2])

        best_individuals = sorted_individuals[0:4]

        best_individuals_table = [["Номер строки", "Код", "Значение целевой функции",
                                   "Вероятность участия в размножении"]]
        for ind in best_individuals:
            target_value = ind[2]
            reproduction_probability = (best_individuals[0][2] + best_individuals[3][2] - target_value) / sum(
                best_individuals[i][2] for i in range(4))

            row = [ind[0], ind[1], target_value, reproduction_probability]
            best_individuals_table.append(row)

        print("Популяция поколения после отсичения худших особей:\n",
              tabulate(best_individuals_table, headers="firstrow", tablefmt="grid"))


if __name__ == "__main__":
    main()
