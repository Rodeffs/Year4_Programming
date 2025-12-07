from math import log


def tf_idf(doc_repo, word_repo, pl_repo, approach):
    # tf = кол-во слова в документе / кол-во всех слов в документе; т.е. частота слова в документе
    # idf = log(кол-во документов / кол-во документов, где есть это слово); т.е. уникальность этого слова относительно других документов
    # tf-idf = tf*idf

    all_docs = list(doc_repo.get_all())
    all_words = list(word_repo.get_all())

    if approach == "taat":
        for word in all_words:
            for doc in all_docs:
                pl = pl_repo.get_both_id(word.word_id, doc.doc_id)

                if pl.count > 0:  # если слово есть в документе, то увеличиваем кол-во документов с ним
                    word.doc_count += 1

                pl.tf = pl.count / doc.length

            for pl in pl_repo.get_word_id(word.word_id):
                idf = log(len(all_docs) / word.doc_count)  # сразу считаем idf
                pl.tf_idf = pl.tf * idf


    elif approach == "daat":
        for doc in all_docs:
            for word in all_words:
                pl = pl_repo.get_both_id(word.word_id, doc.doc_id)

                if pl.count > 0:
                    word.doc_count += 1

                pl.tf = pl.count / doc.length

        for pl in pl_repo.get_all():
            idf = log(len(all_docs) / word_repo.get_by_id(pl.word_id).doc_count)   # сразу посчитать idf не можем
            pl.tf_idf = pl.tf * idf


