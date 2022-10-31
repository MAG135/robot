import traceback

from algorithms.common import IAlgorithmScroll, Algorithm
from algorithms.scroll import algorithm_scr_2
from models.publication_model import PublicationModel


def check_terms_for_algorithm_1():
    return False


def check_terms_for_algorithm_2(publication: PublicationModel):
    if algorithm_scr_2.analysis_hashtags(publication.hashtags) \
            or algorithm_scr_2.analysis_decs(publication.desc) \
            or algorithm_scr_2.analysis_author(publication.author_unique_id):
        return Algorithm.ALGORITHM_2

    return False


class Handler:
    def __init__(self, algorithms: list[IAlgorithmScroll]):
        self.algorithms = algorithms

    def handle(self, publication: PublicationModel):
        try:
            alg_check_list = list()

            # alg_check_list.append(self.check_terms_for_algorithm_1())
            alg_check_list.append(check_terms_for_algorithm_2(publication))

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
        except Exception as ex:
            print(traceback.format_exc())

        return False, None

