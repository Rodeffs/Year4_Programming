def result(doc_repo, pl_repo):
    final_output = []

    for pl in pl_repo.get_all():  # финальная оценка
        pl.final_rank = pl.tf_idf * doc_repo.get_by_id(pl.doc_id).weight
    
    for pl in pl_repo.get_all():
        if pl.final_rank > 0:  # сайты с нулевым рейтингом не берём во внимание
            final_output.append((doc_repo.get_by_id(pl.doc_id).url, pl.final_rank))

    return sorted(final_output, key=lambda x: x[1], reverse=True)  # сортируем в порядке убывания по рейтингу

