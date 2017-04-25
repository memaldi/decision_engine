from nltk.stem.snowball import SnowballStemmer


def stem_tags(lang, tags):
    if lang in SnowballStemmer.languages:
        stemmer = SnowballStemmer(lang)
        stemmed_tags = []
        for tag in tags:
            stemmed_tags.append(stemmer.stem(tag))
        return stemmed_tags
    return tags
