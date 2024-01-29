from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import serializers

from apps.transactions.models import Transactions
from apps.transactions.serializers import TransactionSerializer
from apps.users.models import User
from apps.transactions.permissions import UserPermissons

class TransactionsAPIViews(GenericViewSet, 
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin):
    queryset = Transactions.objects.all()
    serializer_class = TransactionSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return (UserPermissons(), )
        return (AllowAny(), )
    
    def perform_create(self, serializer):
        try:
            from_user = get_object_or_404(User, username=str(serializer.validated_data['from_user']))
            to_user = get_object_or_404(User, username=str(serializer.validated_data['to_user']))
            amount = float(serializer.validated_data['amount'])

            if amount > float(from_user.balance):
                raise serializers.ValidationError('Недостаточно средств для перевода')

            with transaction.atomic():
                if Transactions.objects.filter(from_user=from_user, to_user=to_user, is_completed=False).exists():
                    raise serializers.ValidationError('Транзакция уже завершена')

            #     # from_user.balance -= amount
            #     # to_user.wallet += amount

                from_user.save()
                to_user.save()

                transfer = Transactions(from_user=from_user, to_user=to_user, amount=amount)
                transfer.save()

        except (User.DoesNotExist, ValueError, serializers.ValidationError) as e:
            raise serializers.ValidationError({'detail': str(e)})