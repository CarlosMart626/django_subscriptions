"""django_subscriptions URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import json
from django.conf.urls import url, include
from django.contrib import admin
from .template import render_graphiql
from django.http import HttpResponse
from django.conf import settings

from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from django_subscriptions.schema import schema
from channels.sessions import channel_session

def graphiql(request):
    response = HttpResponse(content=render_graphiql())
    return response

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^graphiql/', graphiql),
    url(r'^graphql', csrf_exempt(GraphQLView.as_view(graphiql=True)))
]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ]

from channels.routing import route_class, route
from graphql_ws.django_channels import GraphQLSubscriptionConsumer


def ws_GQL_connect(message):
    message.reply_channel.send({"accept": True})


@channel_session
def ws_GQLData(message):
    print("message", message.__dict__)
    clean = json.loads(message.content['text'])
    query = clean.get('payload').get('query')
    foovar = clean.get('variables')                                                                                                                                                                                                                                                                                                                                                                                                   
    kwargs = {'context_value': message}
    print("query", query)
    result = schema.execute(query, variable_values=foovar,
                            allow_subscriptions=True, **kwargs)
    print("result", result.data)
    message.reply_channel.send(
        {
            'text': str({'data': json.loads(json.dumps(result.data))})
        })


channel_routing = [
    # route('websocket.connect', ws_GQL_connect, path=r"^/subscriptions"),
    # route('websocket.receive', ws_GQLData, path=r"^/subscriptions"),
    route_class(GraphQLSubscriptionConsumer, path=r"^/subscriptions"),
]
