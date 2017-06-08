from nltk.stem import snowball
from artifact_recommender import models
from artifact_recommender import cdv
from decision_engine import settings
from geopy import geocoders
from geopy.distance import vincenty
from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from collections import Counter
from silk.profiling.profiler import silk_profile
from django.core.cache import cache
import Levenshtein
import operator
import logging

logger = logging.getLogger(__name__)


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
                for source_tag in source_artifact.tags.all():
                    distance = Levenshtein.distance(target_tag.name,
                                                    source_tag.name)
                    if distance <= settings.MAX_LEVENSHTEIN:
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


def recommend_app(user_id, lat, lon, radius):
    user_age, user_location, user_apps, user_tags = cdv.get_user_data(user_id)

    geolocator = geocoders.Nominatim()
    if -1000 in [lat, lon]:
        with silk_profile(name='Geocode for {}'.format(user_location)):
            try:
                user_loc = cache.get_or_set(
                    'geocode:{}'.format(user_location),
                    geolocator.geocode(user_location))
            except (GeocoderServiceError, GeocoderTimedOut):
                user_loc = None
                logger.warning('Can not connect to Geocode URL for location '
                               '{}'.format(user_location))
        with silk_profile(name='Geocode for {}'.format('europe')):
            if not user_loc:
                try:
                    user_loc = cache.get_or_set('geocode:europe',
                                                geolocator.geocode('europe'))
                except (GeocoderServiceError, GeocoderTimedOut):
                    logger.warning('Can not connect to Geocode URL for '
                                   'location europe')
                    return []
        lat = user_loc.latitude
        lon = user_loc.longitude
    user_point = (lat, lon)

    used_apps_tags = []
    for app_id in user_apps:
        try:
            app = models.Application.objects.get(pk=app_id)
            for tag in app.tags.all():
                used_apps_tags.append(tag.name)
        except models.Application.DoesNotExist:
            logger.error('Can not retrieve app {}'.format(app_id))

    ordered_used_tags = Counter(used_apps_tags)
    for tag in ordered_used_tags.most_common(5):
        user_tags.append(tag[0])

    filtered_apps = []
    for app in models.Application.objects.filter(min_age__lte=user_age):
        try:
            with silk_profile(name='Geocode for {}'.format(app.scope)):
                app_loc = geolocator.geocode(app.scope)
            app_point = (app_loc.latitude, app_loc.longitude)
            if vincenty(user_point, app_point).km <= radius:
                filtered_apps.append(app)
        except (GeocoderServiceError, GeocoderTimedOut):
            logger.warning('Can not connect to Geocode URL for location '
                           '{}'.format(app.scope))

    similar_apps = {}
    for app in filtered_apps:
        if len(user_tags) <= 0:
            similar_apps[app.id] = 1
        else:
            app_tags = set()
            for tag in app.tags.all():
                app_tags.add(tag.name)
            user_stemmed_tags = stem_tags(app.lang, user_tags)
            similarity = tags_similarity(set(user_stemmed_tags), app_tags)
            if similarity > settings.RECOMENDATION_THRESHOLD:
                similar_apps[app.id] = similarity

    sorted_similarity = sorted(similar_apps.items(),
                               key=operator.itemgetter(0))
    sorted_similarity.reverse()
    app_list = []
    for item in sorted_similarity:
        app_list.append(item[0])

    return app_list
