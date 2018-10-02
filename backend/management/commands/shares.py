import requests
import twitter

from django.core.management.base import BaseCommand, CommandError
from backend.models.publication import Question
from django.urls import resolve


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        # graph = facebook.GraphAPI(access_token="##################################", version="3.0")
        # post = graph.get_object(id='https://argu.co/', fields='og_object{engagement}')

        # https://graph.facebook.com/?id=https://vraagdepolitiek.nl/q/1/

        #self.facebook(None)
        self.twitter(None)

    def facebook(self, url):
        urls = list()
        for question in Question.objects.all():
            urls.append(
                'https://vraagdepolitiek.nl{}'.format(question.get_absolute_url())
            )

        resp = requests.get('https://graph.facebook.com/?ids={}'.format(','.join(urls)))
        resp.raise_for_status()

        for url, data in resp.json().items():
            _, _, path = url.partition('.nl')
            _, args, kwargs = resolve(path)

            question = Question.objects.get(*args, **kwargs)
            question.fb_support_count = int(data['share']['share_count'])
            question.save()

    def twitter(self, url):
        api = twitter.Api(
            consumer_key='##################################',
            consumer_secret='##################################',
            access_token_key='##################################',
            access_token_secret='##################################'
        )
        print(api.GetSearch('@VraagDePolitiek'))