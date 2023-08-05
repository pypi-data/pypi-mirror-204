from django.conf import settings
from django.utils.translation import ugettext
from dotpath import getpath

from django_perm_trans import exceptions

DPT_OPERATOR = (getpath(settings, 'DJANGO_PERM_TRANS.separator', '|')).strip()
DPT_USE_DB = getpath(settings, 'DJANGO_PERM_TRANS.use_db', False)
DPT_CUSTOM_FUNC = getpath(settings, 'DJANGO_PERM_TRANS.custom_function', None)
DPT_CAPITALIZE_WORDS = getpath(settings, 'DJANGO_PERM_TRANS.capitalize_words', False)
DPT_REMOVE_APP = getpath(settings, 'DJANGO_PERM_TRANS.remove_app', False)
DPT_REMOVE_MODEL = getpath(settings, 'DJANGO_PERM_TRANS.remove_model', False)


def load_perm_model():
    """Load Permission model from django.contrib.auth.models"""
    from django.contrib.auth.models import Permission
    return Permission


def str_override(perm):
    """Override __str__ method of Permission model
    """
    perm_words = []

    if DPT_REMOVE_APP:
        perm_words.append(perm.content_type.app_label)

    if DPT_REMOVE_MODEL:
        perm_words.append(perm.content_type.name)

    perm_words.append(perm.name)

    if DPT_CAPITALIZE_WORDS:
        perm_words = [word.capitalize() for word in perm_words]

    if not DPT_USE_DB:
        perm_words = [ugettext(word) for word in perm_words]

    return f' {DPT_OPERATOR} '.join(perm_words)


def setup_translations(**kwargs):
    """Setup translations for Permission model"""
    perm_model = load_perm_model()

    if getpath(perm_model, '__str_func_override__', False):
        return
    perm_model.__str_func_override__ = True

    if not DPT_CUSTOM_FUNC:
        perm_model.__str__ = str_override
        perm_model.__unicode__ = str_override
        return

    if not isinstance(DPT_CUSTOM_FUNC, type(lambda: None)):
        raise exceptions.DjangoPermTransCustomFuncException()

    perm_model.__str__ = DPT_CUSTOM_FUNC
    perm_model.__unicode__ = DPT_CUSTOM_FUNC
