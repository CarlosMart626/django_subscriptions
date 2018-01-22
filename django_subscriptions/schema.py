import graphene
from rx import Observable


class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info, **kwargs):
        return 'world'

class Subscription(graphene.ObjectType):

    count_seconds = graphene.Int(up_to=graphene.Int())
    say_hello = graphene.String()

    def resolve_count_seconds(root, info, up_to=5):
        return Observable.interval(1000)\
                         .map(lambda i: "{0}".format(i))\
                         .take_while(lambda i: int(i) <= up_to)

    def resolve_say_hello(root, info):
        Observable.interval(1000)\
                  .map(lambda i: "{0}".format(i))\
                  .take_while(lambda i: int(i) <= up_to)
        return Observable.from_("Hello")



schema = graphene.Schema(query=Query, subscription=Subscription)
