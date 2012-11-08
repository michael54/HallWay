from django.conf.urls import patterns, include, url
from recipe.views import RecipeCreate, RecipeDetailView
from food.views import FoodDetailView


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'chief.views.home', name='home'),
    # url(r'^chief/', include('chief.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('userena.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^test/','recipe.views.nav'),
    #url(r'^$', 'recipe.views.nav', name='homepage'),
	url(r'^$', 'recipe.views.index', name='homepage'),

    # URL for recipe
    url(r'^recipe/add/$', RecipeCreate.as_view(), name='recipe_create'),
    url(r'^recipe/(?P<pk>\d+)/$', RecipeDetailView.as_view()),

    # URL for food
    url(r'^food/(?P<pk>\d+)/$', FoodDetailView.as_view())


)

