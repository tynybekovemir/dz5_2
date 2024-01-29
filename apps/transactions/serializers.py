from rest_framework import serializers
from apps.transactions.models import Transactions
from apps.users import models as user_models

from rest_framework import serializers
from .models import Transactions

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ['from_user', 'to_user', 'amount', 'created_at', 'is_completed']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Replace 'from_user' and 'to_user' id with username
        from_user_id = representation.get('from_user')
        to_user_id = representation.get('to_user')

        if from_user_id:
            from_user = user_models.User.objects.get(id=from_user_id)
            representation['from_user'] = from_user.username

        if to_user_id:
            to_user = user_models.User.objects.get(id=to_user_id)
            representation['to_user'] = to_user.username

        return representation
    
    def create(self, validated_data):
        # Extract 'from_user' and 'to_user' from validated_data
        from_user_data = validated_data.pop('from_user', None)
        to_user_data = validated_data.pop('to_user', None)

        # Create the Transactions instance without the 'from_user' and 'to_user' fields
        transaction = Transactions.objects.create(**validated_data)

        # If 'from_user' and 'to_user' are provided, set them separately
        if from_user_data:
            from_user = user_models.User.objects.get(id=from_user_data['id'])
            transaction.from_user = from_user

        if to_user_data:
            to_user = user_models.User.objects.get(id=to_user_data['id'])
            transaction.to_user = to_user

        transaction.save()

        return transaction