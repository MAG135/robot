from models.publication_model import PublicationModel


class Algorithm:
    ALGORITHM_1 = "algorithm_1"


"""
Тип алгоритма, описывает поведение скроллера после окончание работы
"""


class AlgorithmState:
    # Скроллер должен ачинать сначала
    AT_FIRST = 'AT_FIRST'

    # Скроллер должен продолжить работу с места где закончил
    CONTINUE = "continue"


"""
Алгоритмы, которые будут применяться по ходу скроллинга
"""


class IAlgorithmScroll:
    """
    Приоритет алгоритма
    Чем уникальнее условия алгоритма, тем выше приоритет
    """

    def get_priority(self):
        pass

    def start(self, publication: PublicationModel):
        pass

    def get_name(self):
        pass
