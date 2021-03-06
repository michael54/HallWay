from django.conf.urls import patterns, include, url
from recipe.views import RecipeDetailView, RecipeCategoryListView, HotRecipeListView, DidRecipeDetailView
from food.views import FoodDetailView, FoodCategoryDetailView
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',   
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^comments/post/$', 'recipe.ajax_comment_post.post_comment', name='ajaxcommentpost'),
    url(r'^comments/', include('django.contrib.comments.urls')),

    url(r'^accounts/(?P<username>(?!signout|signup|signin)[\.\w]+)/$',
       'accounts.views.profile',
       name='userena_profile_detail'),
    url(r'^accounts/(?P<username>(?!signout|signup|signin)[\.\w]+)/message/$',
       'accounts.views.leave_message',
       name='leave_message'),
    url(r'^accounts/(?P<username>[\.\w]+)/edit/$',
       'accounts.views.profile_edit',
       name='userena_profile_edit'),

    url(r'^message_comet/$', 'accounts.views.message_comet', name='message_comet'),

    url(r'^accounts/', include('userena.urls')),

    url(r'^messages/', include('userena.contrib.umessages.urls')),

    url(r'^grappelli/', include('grappelli.urls')),
    #url(r'^$', 'recipe.views.nav', name='homepage'),
	url(r'^$', 'recipe.views.index', name='homepage'),

    # URL for recipe
    url(r'^recipe/add/$', 'recipe.views.recipe_create', name='recipe_create'),
    url(r'^recipe/(?P<pk>\d+)/$', RecipeDetailView.as_view(), name='recipe_detail'),
    url(r'^recipe/(?P<pk>\d+)/rate/$', 'recipe.views.rate', name='rate'),
    url(r'^recipe/(?P<pk>\d+)/like/$', 'recipe.views.like', name='like'),
    url(r'^recipe/(?P<pk>\d+)/unlike/$', 'recipe.views.unlike', name='unlike'),
    url(r'^recipe/(?P<pk>\d+)/edit/$', 'recipe.views.recipe_edit', name='recipe_edit'),
    url(r'^recipe/(?P<pk>\d+)/delete/$', 'recipe.views.recipe_delete', name='recipe_delete'),
    url(r'^recipe/(?P<pk>\d+)/did/$', 'recipe.views.did_recipe_upload', name='did_recipe_upload'),
    url(r'^didrecipe/(?P<pk>\d+)/$', DidRecipeDetailView.as_view(), name='did_recipe_detail'),

    url(r'^recipecategory/(\d+)/(hot|time|trend|rating)/$', RecipeCategoryListView.as_view(), name='recipe_category'),
    url(r'^hot/$', HotRecipeListView.as_view(), name='hot_recipes'),
    url(r'^recipe/cover_image_upload/$', 'recipe.views.cover_image_upload', name='recipe_image_upload'),
    url(r'^recipe/step_image_upload/$', 'recipe.views.step_image_upload', name='step_image_upload'),

    # URL for food
    url(r'^food/(?P<pk>\d+)/$', FoodDetailView.as_view(), name='food_detail'),
    url(r'^foodcategory/(?P<pk>\d+)/$', FoodCategoryDetailView.as_view(), name='food_list'),
    url(r'^categories/$', 'food.views.categories', name='categories'),


    # URL for activity
    url(r'^activity/$', 'accounts.views.activity', name='actstream'),
    url(r'^activity/', include('actstream.urls')),

    url(r'^ajax/image_delete/$', 'recipe.views.image_delete', name='image_delete'),

    # URL for search
    url(r'^search/autonav/$', 'recipe.search.autonav', name='autonav'),
    url(r'^search/$', 'recipe.search.normal_search', name='normal_search'),
    url(r'^search/advanced/$', 'recipe.search.advanced_search', name = 'advanced_search'),


    # URL for shopping
    url(r'shopping/add/$', 'shopping.views.add_item', name='add_to_shopping_list'),
    url(r'shopping/list/$', 'shopping.views.view_shopping_list', name='view_shopping_list')
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

