# Конвертация чисел вида: 633.5K
def convert_str_to_number(x):
    num = 0
    num_map = {'K': 1000, 'M': 1000000, 'B': 1000000000}
    if x.isdigit():
        num = int(x)
    else:
        if len(x) > 1:
            num = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return int(num)


# Конвертация времени вида: 01:24
def convert_str_time_to_seconds(time_str: str):
    return sum(x * int(t) for x, t in zip([60, 1], time_str.split(":")))


def generate_publication_url(authorUniqueId, publication_id):
    return "https://www.tiktok.com/@%s/video/%s?is_copy_url=1&is_from_webapp=v1" % (authorUniqueId, publication_id)


def get_hashtags_from_file():
    with open('./hashtags.txt', 'r') as f:
        hashtags = f.readlines()
        hashtags = [tag.rstrip() for tag in hashtags]

    return hashtags


def format_hashtags(hashtags: list[str]):
    formatted_tags = list()

    for tag in hashtags:
        if tag.startswith("#"):
            formatted_tags.append(tag.replace('#', ''))
        elif tag != '':
            formatted_tags.append(tag.replace(" ", ""))

    return formatted_tags


def get_key_words():
    with open('./dictionary.txt', 'r') as f:
        worlds = f.readlines()
        worlds = [word.rstrip() for word in worlds]

    return worlds


def format_words(words: list[str]):
    formatted_words = list()

    for word in words:
        if word != '':
            formatted_words.append(word.replace(" ", ""))

    return formatted_words


def get_author():
    with open('./authors.txt', 'r') as f:
        authors = f.readlines()
        authors = [author.rstrip() for author in authors]

    return authors


def format_author(authors: list[str]):
    formatted_authors = list()

    for author in authors:
        if author != '':
            formatted_authors.append(author.replace(" ", ""))

    return formatted_authors


def get_publication_id_from_url(url: str):
    return url.split("/")[-1]
