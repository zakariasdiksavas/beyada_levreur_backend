from base.models import Batiment


def get_user_batiments(user):
    return Batiment.objects.filter(site__in=user.sites.all())