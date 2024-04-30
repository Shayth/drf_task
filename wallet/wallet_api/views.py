import random
import string
from decimal import Decimal

from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wallet, Transaction


def generate_key(length=18):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))


class ObtainAuthToken(APIView):
    @staticmethod
    def post(request):
        username = request.query_params.get('username')
        password = request.query_params.get('password')

        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CreateWalletView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        unique_key = generate_key()
        wallet = Wallet.objects.create(unique_key=unique_key)
        return Response({'unique_key': unique_key}, status=status.HTTP_201_CREATED)


class ViewWalletView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, key_wallet):
        try:
            wallet = Wallet.objects.get(unique_key=key_wallet)
            return Response({'balance': wallet.balance}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Wallet not found'}, status=status.HTTP_404_NOT_FOUND)


class DepositWalletView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, key_wallet):
        try:
            amount = request.query_params.get('amount')
            if amount is None:
                return Response({'error': 'Amount parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)
            amount = Decimal(amount)
            wallet = Wallet.objects.get(unique_key=key_wallet)
            wallet.balance += amount
            wallet.save()
            Transaction.objects.create(
                recipient=key_wallet,
                amount=amount,
                transaction_type='deposit'
            )
            return Response({'message': f'Баланс пополнен успешно'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Wallet not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)


class TransferWalletView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            sender_key = request.query_params.get('sender_key')
            recipient_key = request.query_params.get('recipient_key')
            amount_str = request.query_params.get('amount')

            if amount_str is None:
                return Response({'error': 'Amount parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)

            amount = Decimal(amount_str)

            sender_wallet = Wallet.objects.get(unique_key=sender_key)
            recipient_wallet = Wallet.objects.get(unique_key=recipient_key)

            if sender_wallet.balance < amount:
                return Response({'error': 'Недостаток средств'}, status=status.HTTP_400_BAD_REQUEST)

            sender_wallet.balance -= amount
            recipient_wallet.balance += amount

            sender_wallet.save()
            recipient_wallet.save()

            Transaction.objects.create(
                sender=sender_key,
                recipient=recipient_key,
                amount=amount,
                transaction_type='transfer'
            )

            return Response({'message': 'Успешно'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Wallet not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)