from mapper import mapper
from models.publication_model import PublicationModel
from repositories import video_repository, publication_repository


class Algorithm:
    ALGORITHM_1 = "algorithm_1"
    ALGORITHM_2 = "algorithm_2"


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


def save(publication: PublicationModel):
    video_entity = mapper.to_video_entity(publication.video)
    publication_entity = mapper.to_publication_entity(publication, video_entity)

    video_repository.save(video_entity)
    publication_repository.save(publication_entity)