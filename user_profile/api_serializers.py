from rest_framework.serializers import *
from django.db.models import Q

from .models import StakeModel, CustomUser


class StakeModelSerializer(ModelSerializer):

    class Meta:
        model = StakeModel
        fields = ['id', 'stake_period', 'token_tag', 'amount', 'user']

    id = ReadOnlyField()
    user = PrimaryKeyRelatedField(read_only=True)
    stake_period = ChoiceField(choices=StakeModel.StakePeriod.choices)
    token_tag = CharField()
    amount = FloatField()


class CustomUserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'email']

    id = ReadOnlyField()
    email = ReadOnlyField()