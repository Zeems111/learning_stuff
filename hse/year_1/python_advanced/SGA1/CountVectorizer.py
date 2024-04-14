class CountVectorizer:
    def __init__(self, ngram_size):
        """Initialises CountVectorizer objects"""
        # Checks that ngram_size is integer greater than 0.
        # Otherwise, raises corresponding exceptions.
        if type(ngram_size) is not int:
            raise TypeError('ngram size must be an integer')
        if ngram_size < 1:
            raise ValueError('ngram size must be greater than 0')

        self.ngram_size = ngram_size
        self.token_to_index = dict()

    def fit(self, corpus):
        """Creates a token_to_index dictionary based on
        a given corpus"""
        # Generates a set of tokens from a corpus.
        ngrams = set()
        for line in corpus:
            line = line.upper()
            line_length = len(line)

            if line_length >= self.ngram_size:
                number_of_ngrams = line_length - self.ngram_size + 1
                for i in range(number_of_ngrams):
                    token = line[i: i + self.ngram_size]
                    ngrams.add(token)

        # If the set is empty after processing the whole corpus
        # raises an exception.
        if not ngrams:
            msg = (f'There is no token of length {self.ngram_size} '
                   f'in given corpus')
            raise ValueError(msg)

        # Otherwise sorts the set and creates a token_to_index dictionary.
        self.token_to_index = dict((ngram, index)
                                   for (index, ngram)
                                   in enumerate(sorted(ngrams)))

    def transform(self, corpus):
        """Transforms given corpus to a list of tokens'
        counts according to existing token_to_index dictionary"""
        # If token_to_index dictionary is empty,
        # then raises exception.
        if not self.token_to_index:
            msg = ("Corpus can't be transformed: "
                   "token_to_index dictionary is empty.")
            raise ValueError(msg)

        transformed_corpus = []
        # Transforms corpus according to token_to_index dict.
        for line in corpus:
            number_of_ngrams = len(line) - self.ngram_size + 1
            token_count = [0] * len(self.token_to_index)

            # If corpus line is shorter than token's length
            # sets corresponding line with 0s and continues to the next line.
            if len(line) < self.ngram_size:
                transformed_corpus.append(token_count)
                continue

            # Gets token index if it is in the token_to_index dict
            # and increases its count by 1.
            # Otherwise, ignores token.
            for i in range(number_of_ngrams):
                token = line[i: i + self.ngram_size]
                token_ind = self.token_to_index.get(token, None)
                if token_ind is not None:
                    token_count[token_ind] += 1
            transformed_corpus.append(token_count)
        return transformed_corpus

    def fit_transform(self, corpus):
        """Creates a token_to_index dictionary based on a given corpus
        and transforms it to a list of tokens' counts"""
        self.fit(corpus)
        return self.transform(corpus)
