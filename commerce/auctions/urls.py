from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("categories<int:id>", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:auction_id>/listing", views.listingPage, name="listing"),
    path("<int:auction_id><str:sit>/whatchlist", views.whatchlisting, name="whatchlisting"),
    path("<int:user_lists>/user_lists", views.index, name="user_lists"),
    path("<int:auction_id>/close", views.close, name="close"),
    path("<int:auction_id>/comment", views.comment, name="comment"),
]
