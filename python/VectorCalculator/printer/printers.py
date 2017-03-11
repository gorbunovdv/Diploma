def relationship_printer(model, result, output_file):
    for d, u, v in reversed(sorted(result)):
        output_file.write("%.3f\t%s\t%s\n" % (d, model.index2word[u].encode('utf-8'), model.index2word[v].encode('utf-8')))


def equivalence_class_printer(model, result, output_file):
    for eq_class in result:
        output_file.write("Equivalence class: %d\n" % eq_class)
        for word in result[eq_class]:
            output_file.write("%s\n" % model.index2word[word].encode('utf-8'))


def pairs_with_mincos_printer(model, result, output_file):
    for d, u, v in reversed(sorted(result)):
        output_file.write("%.3f\t%s\t%s\n" % (d, model.index2word[u].encode('utf-8'), model.index2word[v].encode('utf-8')))


def fours_with_not_fixed_relationship_printer(model, result, output_file):
    for d, u1, v1, u2, v2 in reversed(sorted(result)):
        output_file.write("%.3f\t%s\t%s\t%s\t%s\n" % (
        d, model.index2word[u1].encode('utf-8'), model.index2word[v1].encode('utf-8'), model.index2word[u2].encode('utf-8'), model.index2word[v2].encode('utf-8')))
