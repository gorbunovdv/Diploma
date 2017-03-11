def relationship_evaluator(result_strict, result_not_strict):
    correct, incorrect = 0, 0
    strict_pairs = {tuple(sorted((pair[1], pair[2]))) for pair in result_strict}
    nonstrict_pairs = {tuple(sorted((pair[1], pair[2]))) for pair in result_not_strict}
    for pair in nonstrict_pairs:
        if pair in strict_pairs:
            correct += 1
        else:
            incorrect += 1
    print "Correctly found %d/%d pairs (%f percents), %d/%d are incorrect (%f percents)" % (
        correct, len(strict_pairs), 100.0 * correct / len(strict_pairs),
        incorrect, len(nonstrict_pairs), 100.0 * incorrect / len(nonstrict_pairs)
    )


def equivalence_class_evaluator(result_strict, result_not_strict):
    result_strict = sorted([result_strict[index] for index in result_strict])
    result_not_strict = sorted([result_not_strict[index] for index in result_not_strict])
    result, total = 0, 0
    for index in range(min(len(result_not_strict), len(result_strict))):
        for index2 in range(min(len(result_strict[index]), len(result_not_strict[index]))):
            result += 1 if result_strict[index][index2] == result_not_strict[index][index2] else 0
        total += max(len(result_strict[index]), len(result_not_strict[index]))
    print "Correctly found %d/%d indices (%f percents)" % (
        result, total, 100.0 * result / total
    )


def closest_pairs_evaluator(result_strict, result_not_strict):
    correct, incorrect = 0, 0
    strict_closest_pairs = {tuple(sorted((pair[1], pair[2]))) for pair in result_strict}
    nonstrict_closest_pairs = {tuple(sorted((pair[1], pair[2]))) for pair in result_not_strict}
    for pair in nonstrict_closest_pairs:
        if pair in strict_closest_pairs:
            correct += 1
        else:
            incorrect += 1
    print "Correctly found %d/%d pairs (%f percents), %d/%d are incorrect (%f percents)" % (
        correct, len(strict_closest_pairs), 100.0 * correct / len(strict_closest_pairs),
        incorrect, len(nonstrict_closest_pairs), 100.0 * incorrect / len(nonstrict_closest_pairs)
    )
