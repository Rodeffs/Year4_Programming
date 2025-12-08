def mapper(doc_repo, ref_ids):  # mapper получает на вход id документов, ссылающихся на этот документ и возвращает их вес / кол-во исходящих ссылок
    for doc_id in ref_ids:
        doc = doc_repo.get_by_id(doc_id)
        yield doc.weight / doc.links


def reducer(d, mapped):  # reducer складывает всё воедино, умножает на d и добавляет (1-d)
    result = 0

    for value in mapped:
        result += value

    return (1-d) + d*result


def page_rank(doc_repo, doc_link_repo, d, cycle_count):  # d = damping - фактор затухания
    for i in range(cycle_count):
        for doc in doc_repo.get_all():
            ref_ids = [entry.doc_from_id for entry in doc_link_repo.get_id_to(doc.doc_id)]
            mapped = mapper(doc_repo, ref_ids)
            doc.weight = reducer(d, mapped)
