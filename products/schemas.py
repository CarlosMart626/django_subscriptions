from graphene import relay, String, List, resolve_only_args
from graphene_django import DjangoObjectType

from .models import Product


class ProductNode(DjangoObjectType):

    class Meta:
        model = Product
        interfaces = (relay.Node,)
