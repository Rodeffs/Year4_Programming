class Vertice:
    def __init__(self, doc, d):
        self.__incoming = []
        self.__doc = doc
        self.__d = d
        self.__neighbors = []

    def get_id(self) -> int:
        return self.__doc.doc_id

    def add_neighbor(self, vertice) -> None:
        self.__neighbors.append(vertice)

    def send(self) -> None:
        for neighbor in self.__neighbors:
            neighbor.receive(self.__doc.weight / self.__doc.links)

    def receive(self, message) -> None:
        self.__incoming.append(message)

    def update(self) -> None:
        self.__doc.weight = (1-self.__d) + self.__d*sum(self.__incoming)
        self.__incoming = []


def pregel(doc_repo, doc_link_repo, d, cycle_count):
    # Суть алгоритма - есть вершины, каждая вершина хранит свой рейтинг, полученные сообщения и список соседей.
    # В первый супершаг каждая вершина отправляет соседям сообщение, где содержится её рейтинг / кол-во ссылок.
    # Во второй супершаг каждая вершина обновляет свой рейтинг по формуле (1-d) + d*sum, где sum - сумма всех сообщений.
    # Повторяем эти шаги до сходимости

    vertices = []

    for doc in doc_repo.get_all():  # создаём вершины
        new_vertice = Vertice(doc, d)
        vertices.append(new_vertice)

    for vertice in vertices:  # устанавливаем связи
        for link in doc_link_repo.get_id_from(vertice.get_id()):  # получаем все документы, на которые ссылается данный
            for other in vertices:
                if other.get_id() == link.doc_to_id:
                    vertice.add_neighbor(other)
                    break

    for i in range(cycle_count):
        for vertice in vertices:  # супершаг 1 - все вершины отправляют соседям сообщения, которые содержат их ранг / кол-во всех ссылок
            vertice.send()

        for vertice in vertices:  # супершаг 2 - все вершины обновляют свой ранг в зависимости от полученных сообщений
            vertice.update()

