import random
import string
alphabet = "{}{}{}".format(string.ascii_letters, string.digits, string.punctuation)
django_secret = "".join([random.SystemRandom().choice(alphabet) for i in range(50)])
print('DJANGO_SECRET_KEY={}'.format(django_secret))
print('# ALLOWED_HOSTS is a comma separated list of allowed hosts')
print('ALLOWED_HOSTS=localhost')
