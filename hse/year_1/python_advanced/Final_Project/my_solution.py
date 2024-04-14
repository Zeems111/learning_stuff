import json
import argparse


class SetEncoder(json.JSONEncoder):
    """Creates an encoder for easier json dumps of sets."""
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def load_document(filepath: str):
    """Creates a dictionary {article_id: 'article name + its content'}.
    Ignores articles with inappropriate id."""
    articles = {}
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            first_tab_index = line.index('\t')
            try:
                article_id = int(line[:first_tab_index])
                if article_id < 0:
                    raise ValueError("article_id can't be less than 0")
            except Exception:
                continue
            first_space_index = line.index(' ')
            article_name = line[first_tab_index:first_space_index].strip()
            article_content = line[first_space_index:].strip()
            articles[article_id] = f'{article_name} {article_content}'
    return articles


def build_inverted_index(articles):
    """Creates a dictionary {word: set of article_id}."""
    inverted_index = {}
    for article_id, article in articles.items():
        article.replace('\t', ' ')
        article_content = set(x.strip() for x in article.split())
        for word in article_content:
            word_inverted_index = inverted_index.setdefault(word, set())
            word_inverted_index.add(article_id)
    return InvertedIndex(inverted_index)


class InvertedIndex:
    def __init__(self, inverted_index):
        self.inverted_index = inverted_index

    def query(self, words):
        """Returns a set of common articles for all words."""
        query_result = set()
        query_result.update(self.inverted_index.setdefault(words[0], set()))
        words = set(words)
        for word in words:
            query_result &= self.inverted_index.setdefault(word, set())
        return query_result

    def dump2(self, filepath):
        """Stores inverted index to a file."""
        with open(filepath, 'w', encoding='utf-8') as file:
            for word, articles in self.inverted_index.items():
                file.write(json.dumps((word, list(articles))))
                file.write('\n')

    def dump(self, filepath):
        """Stores inverted index to a file."""
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.inverted_index, cls=SetEncoder))

    @classmethod
    def load2(cls, filepath):
        """Loads inverted index from a file"""
        inverted_index = {}
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                word, articles = json.loads(line)
                inverted_index[word] = set(articles)
        return InvertedIndex(inverted_index)

    @classmethod
    def load(cls, filepath):
        """Loads inverted index from a file"""
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                inverted_index = json.loads(line)

            for word in inverted_index:
                inverted_index[word] = set(inverted_index[word])
        return InvertedIndex(inverted_index)


def build_command(args):
    inverted_index = build_inverted_index(load_document(args.dataset_path))
    inverted_index.dump(args.index_path)


def query_command(args):
    inverted_index = InvertedIndex.load(args.index_path)
    with open(args.query_path, 'r', encoding='utf-8') as file:
        for line in file:
            words = set()
            for word in line.split():
                words.add(word.strip())
            words = list(words)
            query_result = inverted_index.query(words)
            print(*sorted(query_result), sep=',')


def create_argparser():
    parser = argparse.ArgumentParser(description='Creates inverted index')
    subparsers = parser.add_subparsers(title='Available commands', help='description')
    build_parser = subparsers.add_parser('build')
    build_parser.add_argument('--dataset', dest='dataset_path',
                              default='./tests/wikipedia_sample.txt',
                              help='path to dataset to build Inverted Index')
    build_parser.add_argument('--index', dest='index_path',
                              default='./index.json',
                              help='path for Inverted Index dump')
    build_parser.set_defaults(func=build_command)

    query_parser = subparsers.add_parser('query')
    query_parser.add_argument('--query_file', dest='query_path',
                              help='query file with collection of queries to run against Inverted Index')
    query_parser.add_argument('--index', dest='index_path',
                              help='path to load Inverted Index from')
    query_parser.set_defaults(func=query_command)
    return parser

def main():
    parser = create_argparser()
    args = parser.parse_args()
    if not vars(args):
        parser.print_usage()
    else:
        args.func(args)

if __name__ == '__main__':
    main()