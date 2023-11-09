from django.contrib import admin
from .models import Report, SingleGamePlayer, ChessGame


class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "chess_com_username",
        "lichess_username",
        "time_class",
        "games_num",
        "analyzed_games",
        "engine_depth",
        "fail_reason",
        "professional",
    )
    search_fields = ("chess_com_username", "lichess_username")


class SingleGamePlayerAdmin(admin.ModelAdmin):
    list_display = ("elo",)


class ChessGameAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "host",
        "opening",
        "opening_short",
        "player_color",
        "result",
        "end_reason",
        "time_class",
        "time_control",
        "url",
        "username",
    )
    search_fields = ("host", "opening", "username")


admin.site.register(Report, ReportAdmin)
admin.site.register(SingleGamePlayer, SingleGamePlayerAdmin)
admin.site.register(ChessGame, ChessGameAdmin)
