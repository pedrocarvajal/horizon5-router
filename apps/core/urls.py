from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.core.controllers.backtest import BacktestController
from apps.core.controllers.orders import OrderController

router = DefaultRouter()

urlpatterns = [
    path("backtests/", BacktestController.as_view(), name="backtest.get"),
    path("orders/", OrderController.as_view(), name="order.get"),
    *router.urls,
]
