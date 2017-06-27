from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.index, name='index'), 
	url(r'^add$', views.add, name="add"),
	url(r'^add_trip$', views.add_trip, name="add_trip"),
	url(r'^join/(?P<join_id>[\d]+)$', views.join_plan, name="join"),
	url(r'^(?P<id>[\d]+)$', views.show_plan, name="show"),
] 