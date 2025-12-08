def mapper(doc_repo, doc_link_repo, d):  # mapper получает на вход документы и выводит ключ-значение, где ключ - документ, а значение - id ссылающегося на него документа
    for doc in doc_repo.get_all():
        is_dangling = True

        for link in doc_link_repo.get_id_to(doc.doc_id):
            is_dangling = False
            yield doc, link.doc_from_id

        if is_dangling:  # если на эту вершину никто не ссылается, то отметим сразу сосчитаем её ранк
            doc.weight = 1-d
            


def reducer(doc_repo, d, shuffled):  # reducer складывает всё воедино, умножает на d и добавляет (1-d)
    pending = []  # значения весов должны обновиться только после всех шагов
    result = 0
    prev_doc = None

    for doc, from_id in shuffled:
        doc_from = doc_repo.get_by_id(from_id)

        if prev_doc != doc and prev_doc is not None:
            pending.append((prev_doc, 1-d + d*result))
            result = 0

        prev_doc = doc
        result += doc_from.weight / doc_from.links

    pending.append((prev_doc, 1-d + d*result))

    for doc, new_value in pending:
        doc.weight = new_value


def page_rank(doc_repo, doc_link_repo, d, cycle_count):
    for i in range(cycle_count):
        result = list(mapper(doc_repo, doc_link_repo, d))
        result = sorted(result, key=lambda x: x[0].doc_id)  # shuffle
        reducer(doc_repo, d, result)

