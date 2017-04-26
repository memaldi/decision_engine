from nltk.stem import snowball
from artifact_recommender import models
from decision_engine import settings
import Levenshtein


def stem_tags(lang, tags):
    if lang in snowball.SnowballStemmer.languages:
        stemmer = snowball.SnowballStemmer(lang)
        stemmed_tags = []
        for tag in tags:
            stemmed_tags.append(stemmer.stem(tag))
        return stemmed_tags
    return tags


def tags_similarity(source_tags, target_tags):
    try:
        similarity = len(
            source_tags & target_tags) * 1.0 / len(
                source_tags | target_tags) * 1.0
    except ZeroDivisionError:
        similarity = 0
    return similarity


def tag_similarity(source_artifact_id):
    source_artifact = models.Artifact.objects.get(pk=source_artifact_id)
    similar_artifacts = {}
    for target_artifact in models.Artifact.objects.all():
        modified_tags = set()
        if source_artifact.lang not in snowball.SnowballStemmer.languages:
            for target_tag in target_artifact.tags.all():
                add = False
                for source_tag in source_artifact.tags.all():
                    distance = Levenshtein.distance(target_tag.name,
                                                    source_tag.name)
                    if distance <= settings.MAX_LEVENSHTEIN:
                        modified_tags.add(source_tag.name)
                        add = True
                        break
                if not add:
                    modified_tags.add(target_tag.name)
        else:
            for target_tag in target_artifact.tags.all():
                modified_tags.add(target_tag.name)
        source_tag_names = set()
        for tag in source_artifact.tags.all():
            source_tag_names.add(tag.name)
        similarity = tags_similarity(source_tag_names, modified_tags)

        if similarity > 0:
            similar_artifacts[target_artifact] = similarity
    for artifact in similar_artifacts:
        if artifact.id != source_artifact.id:
            sim_value = similar_artifacts[artifact]
            similarity = models.Similarity(source_artifact=source_artifact,
                                           target_artifact=artifact,
                                           value=sim_value)
            similarity.save()
