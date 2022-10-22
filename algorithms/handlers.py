from algorithms.common import IAlgorithmScroll, Algorithm
from models.publication_model import PublicationModel


class Handler:
    def __init__(self, algorithms: list[IAlgorithmScroll]):
        self.algorithms = algorithms

    def check_terms_for_algorithm_1(self):
        if True:
            return Algorithm.ALGORITHM_1
        return None

    def handle(self, publication: PublicationModel):
        alg_check_list = list()

        alg_check_list.append(self.check_terms_for_algorithm_1())

        alg_check_entities = list()

        for i in self.algorithms:
            if i.get_name() in alg_check_list:
                alg_check_entities.append(i)

        if len(alg_check_entities) == 0:
            return False, None

        current_alg = alg_check_entities[0]
        for i in alg_check_entities:
            if i.get_priority() > current_alg.get_priority():
                current_alg = i

        return True, current_alg.start(publication)
