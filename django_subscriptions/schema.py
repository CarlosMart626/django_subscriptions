import graphene
from graphene import relay
from rx import Observable
from channels import Group
from products.schemas import ProductNode
from products.models import Product
from graphene_django.filter import DjangoFilterConnectionField


def make_sub(info, gid):
    inst = relay.Node.get_node_from_global_id(info, gid)
    print("Instancia", inst)
    try:
        gp_name = 'gqp.{0}-updated.{1}'.format(str.lower(inst.__class__.__name__), inst.pk)
        Group(gp_name).add(info.context.reply_channel)
        info.context.channel_session['Groups'] = ','.join(
            (gp_name, info.context.channel_session['Groups']))
    except:
        pass
    return iter([inst])

class Query(graphene.ObjectType):
    hello = graphene.String()
    product = relay.node.Field(ProductNode, id=graphene.Int())
    products = DjangoFilterConnectionField(ProductNode)

    def resolve_hello(self, info, **kwargs):
        return 'world'

class Subscription(graphene.ObjectType):

    count_seconds = graphene.Int(up_to=graphene.Int())
    sub_product = graphene.Field(
        ProductNode, description='subscribe to updated product', id=graphene.Int())

    def resolve_count_seconds(root, info, up_to=5):
        return Observable.interval(1000)\
                         .map(lambda i: "{0}".format(i))\
                         .take_while(lambda i: int(i) <= up_to)

    def resolve_sub_product(root, info, *args, **kwargs):
        id = kwargs.get('id')
        print("KW", kwargs)
        print("args", args)
        product_object = Product.objects.get(pk=id)
        gp_name = 'gqp.{0}-updated.{1}'.format(
            str.lower(product_object.__class__.__name__), product_object.pk)
        print("gp_name", gp_name)
        print("info", info.context.__dict__)
        print("session", info.context.channel_session.__dict__)
        # context = info.return_type
        print("channel_layer", info.context.reply_channel.channel_layer.__dict__)
        Group(gp_name).add(info.context.reply_channel)
        channel_session = info.context.channel_session
        
        all_channels = [
            channel for channel in info.context.channel_layer.group_channels(gp_name)]
        print("all_channels", all_channels)
        info.context.channel_session.update(
            {'Groups': ','.join((gp_name, info.context.channel_session.get('Groups', '')))})
        print("channel_session", channel_session.__dict__)
        return Observable.from_iterable(iter([product_object]))


schema = graphene.Schema(query=Query, subscription=Subscription)
