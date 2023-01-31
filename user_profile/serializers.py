from rest_framework.serializers import *
from .models import StakeModel


class StakeModelSerializer(ModelSerializer):

    class Meta:
        model = StakeModel
        fields = ['id', 'stake_period', 'token_tag','amount', 'user']

    id = ReadOnlyField()
    user = PrimaryKeyRelatedField(read_only=True)
    stake_period = ChoiceField(choices=StakeModel.StakePeriod.choices)
    token_tag = CharField()
    amount = FloatField()

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)