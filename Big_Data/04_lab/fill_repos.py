import requests
import re
from bs4 import BeautifulSoup  # для парсинга HTML

from data import Doc, Word, PL


def fill_repos(doc_repo, word_repo, pl_repo, doc_link_repo, query, urls):  # заполнить все репозитории исходя из запросов
    for word in query:  # нас интересуют только те слова, которые были в запросе
        new_word = Word(word)
        word_repo.add(new_word)

    # Работа с парсингом HTML

    inital_weight = 1/len(urls)  # изначальный вес документов

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.7103.48 Safari/537.36"}  # чтобы сайты не отклоняли запросы

    site_links = []  # временно храним все ссылки на сайты, потом уберём те, которые не ссылаются на наши сайты

    for url in urls:
        new_doc = Doc(url, inital_weight)
        doc_repo.add(new_doc)

        try:
            print("Getting response from", url)
            response = requests.get(url, headers=headers)

        except Exception:
            raise(RuntimeError(f"Error, could not get response from {url}, reason: {Exception}"))

        content = response.text  # получаем файлы в формате HTML
        soup = BeautifulSoup(content, "lxml")  # lxml - библиотека в python, переводящая HTML в дерево элементов
        text = soup.get_text(separator=' ')  # сепаратор пробел обеспечит то, что слова не будут слипаться
        words = re.findall(r"\b\w+\b", text)  # регулярное выражение для вывода всех слов

        for word in words:
            word = word.lower()  # не обращаем внимание на регистр
            word_in_repo = word_repo.get_by_word(word)  # находим это слово в репозитории

            if word_in_repo is None:  # если этого слова не было в запросе, то тогда ничего не делаем
                continue
            
            already_in = False

            for pl in pl_repo.get_word_id(word_in_repo.word_id):  # смотрим, если уже есть такая связь слово-документ, и если да, то увеличиваем кол-во вхождений
                if pl.doc_id == new_doc.doc_id:
                    pl.count += 1
                    already_in = True
                    break

            if not already_in:
                new_pl = PL(word_in_repo.word_id, new_doc.doc_id)  # если же такой связи ещё не было, то добавляем её
                pl_repo.add(new_pl)

        links = [a["href"] for a in soup.find_all('a', href=True)]  # получаем все ссылки на этом сайте
        site_links.append([new_doc, links])

    for cur_doc, links in site_links:

        for link in links:
            if link == cur_doc.url:  # ссылки сами на себя не считаются
                continue

            doc_in_repo = doc_repo.get_by_url(link)

            if doc_in_repo is not None:
                already_in = False

                for from_id in doc_link_repo.get_id_to(doc_in_repo.doc_id):  # смотрим, если эта ссылка уже была учтена, и если это так, то не добавляем
                    if from_id == cur_doc.doc_id:
                        already_in = True
                        break

                if not already_in:
                    doc_link_repo.add(cur_doc.doc_id, doc_in_repo.doc_id)

