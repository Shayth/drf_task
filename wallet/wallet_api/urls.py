from django.urls import path, include
from .views import CreateWalletView, ViewWalletView, DepositWalletView, TransferWalletView, ObtainAuthToken

urlpatterns = [
    path('create/wallet/', CreateWalletView.as_view(), name='create_wallet'),
    path('view/wallet/<str:key_wallet>/', ViewWalletView.as_view(), name='view_wallet'),
    path('deposit/wallet/<str:key_wallet>/', DepositWalletView.as_view(), name='deposit_wallet'),
    path('transfer/wallet/', TransferWalletView.as_view(), name='transfer_wallet'),
    path('token/', ObtainAuthToken.as_view(), name='obtain_auth_token'),
    path('watchman/', include('watchman.urls')),
]
