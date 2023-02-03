from rest_framework.serializers import *
from django.db.models import Q

from .models import StakeModel, UserToken, Token


class StakeModelSerializer(ModelSerializer):

    class Meta:
        model = StakeModel
        fields = ['id', 'stake_period', 'token_tag', 'amount', 'user']

    id = ReadOnlyField()
    user = PrimaryKeyRelatedField(read_only=True)
    stake_period = ChoiceField(choices=StakeModel.StakePeriod.choices)
    token_tag = CharField()
    amount = FloatField()

    def validate_amount(self, value):
        return value

    def update(self, instance, validated_data):
        # user = instance.user
        # token = Token.objects.filter(tag=instance.token_tag).first()
        # if token:
        #     user_token = UserToken.objects.filter(Q(user=user) & Q(token=token)).first()
        #     if user_token:
        #         pass
        #     else:
        #         return None
        # else:
        #     return None
        return super().update(instance, validated_data)
