def mapper(doc_repo, doc_link_repo):  # mapper получает на вход документы и выводит ключ-значение, где ключ - документ, а значение - ранк / кол-во ссылок ссылающегося на него документа
    for doc in doc_repo.get_all():
        is_dangling = True

        for link in doc_link_repo.get_id_to(doc.doc_id):
            doc_from = doc_repo.get_by_id(link.doc_from_id)
            is_dangling = False
            yield doc, doc_from.weight / doc_from.links

        if is_dangling:  # если на эту вершину никто не ссылается
            yield doc, 0
            

def reducer(d, mapped):  # reducer складывает всё воедино, умножает на d и добавляет (1-d)
    prev_doc = None
    result = 0

    for doc, value in mapped:
        if prev_doc != doc and prev_doc is not None:
            prev_doc.weight = 1-d + d*result
            result = 0

        prev_doc = doc
        result += value

    if prev_doc is not None:
        prev_doc.weight = 1-d + d*result


def page_rank(doc_repo, doc_link_repo, d, cycle_count):
    for i in range(cycle_count):
        result = list(mapper(doc_repo, doc_link_repo))  # shuffle не нужен из-за специфики mapped
        reducer(d, result)

