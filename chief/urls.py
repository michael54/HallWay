from django.conf.urls import patterns, include, url
from recipe.views import RecipeCreate, RecipeDetailView, RecipeCategoryListView, HotRecipeListView
from food.views import FoodDetailView, FoodCategoryListView
from django.conf import settings
from django.conf.urls.static import static

import autocomplete_light
autocomplete_light.autodiscover()
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',   
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^autocomplete/', include('autocomplete_light.urls')),

    url(r'^accounts/(?P<username>(?!signout|signup|signin)[\.\w]+)/$',
       'accounts.views.profile',
       name='userena_profile_detail'),
    url(r'^accounts/', include('userena.urls')),
    
    url(r'^grappelli/', include('grappelli.urls')),
    #url(r'^$', 'recipe.views.nav', name='homepage'),
	url(r'^$', 'recipe.views.index', name='homepage'),

    # URL for recipe
    url(r'^recipe/add/$', RecipeCreate.as_view(), name='recipe_create'),
    url(r'^recipe/(?P<pk>\d+)/$', RecipeDetailView.as_view(), name='recipe_detail'),
    url(r'^recipe/(?P<pk>\d+)/rate/$', 'recipe.views.rate', name='rate'),
    url(r'^recipecategory/(\d+)/(hot|time|trend)/$', RecipeCategoryListView.as_view(), name='recipe_category'),
    url(r'^hot/$', HotRecipeListView.as_view(), name='hot_recipes'),

    # URL for food
    url(r'^food/(?P<pk>\d+)/$', FoodDetailView.as_view(), name='food_detail'),
    url(r'^foodcategory/(\d+)/$', FoodCategoryListView.as_view()),
    url(r'^foodcategory/(\d+)/(\w+)/$', FoodCategoryListView.as_view()),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

