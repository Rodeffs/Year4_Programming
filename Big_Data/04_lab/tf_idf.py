from math import log


def tf_idf(doc_repo, word_repo, pl_repo, approach):
    all_docs = list(doc_repo.get_all())
    all_words = list(word_repo.get_all())

    if approach == "taat":
        for word in all_words:
            docs_with_word = list(pl_repo.get_word_id(word.word_id))  # все документы с этим словом

            for pl in docs_with_word:
                pl.tf = pl.count / doc_repo.get_by_id(pl.doc_id).length  # tf = кол-во слова в документе / кол-во всех слов в документе; т.е. частота слова в документе
                word.doc_count = len(docs_with_word)  # кол-во документов с этим словом
                idf = log(len(all_docs) / word.doc_count)  # idf = log(кол-во документов / кол-во документов, где есть это слово); т.е. уникальность этого слова относительно других документов
                pl.tf_idf = pl.tf * idf  # tf-idf = tf * idf 


    elif approach == "daat":
        for doc in all_docs:
            for pl in pl_repo.get_doc_id(doc.doc_id):  # все слова в этом документе
                pl.tf = pl.count / doc.length  # tf = кол-во слова в документе / кол-во всех слов в документе; т.е. частота слова в документе
                word_repo.get_by_id(pl.word_id).doc_count += 1  # увеличиваем кол-во документов, в котором это слово встретилось

        for pl in pl_repo.get_all():
            idf = log(len(all_docs) / word_repo.get_by_id(pl.word_id).doc_count)  # idf = log(кол-во документов / кол-во документов, где есть это слово); т.е. уникальность этого слова относительно других документов
            pl.tf_idf = pl.tf * idf  # tf-idf = tf * idf 



