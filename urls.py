# blockchain/urls.py

from django.contrib import admin
from django.urls import path, re_path as url
from blockchain.views import get_chain, mine_block, is_valid

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^get_chain$', get_chain, name="get_chain"),
    url('^mine_block$', mine_block, name="mine_block"),
    url('^is_valid$', is_valid, name="is_valid"),
]
