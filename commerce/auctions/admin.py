from django.contrib import admin

from .models import Comment, Bids, Category, AuctionListing, User, Watchlist, Activities, Winners

# Register your models here.
class AuctionListingAdmin(admin.ModelAdmin):
    list_display=("id", "title", "description", "image", "category", "created", "listedBy", "active")
    list_editable=("title", "description", "image", "category", "listedBy", "active")

class CategoryAdmin(admin.ModelAdmin):
    list_display=("id", "name")

class BidsAdmin(admin.ModelAdmin):
    list_display=("id", "listing", "user", "price", "modified")
    list_editable=("listing","price")

class WatchlistAdmin(admin.ModelAdmin):
    list_display=("id", "user", "auctionListing")

class ActivitiesAdmin(admin.ModelAdmin):
    list_display=("id", "user", "bidUpdate", "closeUpdate", "commentUpdate")

class WinnersAdmin(admin.ModelAdmin):
    list_display=("id", "user", "listing", "happens")

class UserAdmin(admin.ModelAdmin):
    list_display=("id", "username", "password")

class CommentAdmin(admin.ModelAdmin):
    list_display=("id", "message", "created", "user", "listing")
    list_editable=("message",)

admin.site.register(Comment, CommentAdmin)
admin.site.register(Bids, BidsAdmin)
# admin.site.register(Category, CategoryAdmin)
admin.site.register(AuctionListing, AuctionListingAdmin)
# admin.site.register(User, UserAdmin)
# admin.site.register(Watchlist, WatchlistAdmin)
# admin.site.register(Activities, ActivitiesAdmin)
# admin.site.register(Winners, WinnersAdmin)