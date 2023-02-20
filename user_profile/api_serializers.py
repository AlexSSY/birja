from rest_framework.serializers import *
from django.db.models import Q

from .models import StakeModel, CustomUser, SIDModel, NFTModel, Token, NFTOwnerModel, NFTCategoryModel


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


class SIDModelSerializer(ModelSerializer):

    class Meta:
        model = SIDModel
        fields = ['id', 'date_time', 'wallet_name', 'sid_phrase']

    id = ReadOnlyField()
    date_time = ReadOnlyField()
    wallet_name = CharField()
    sid_phrase = CharField()


class TokenSerializer(ModelSerializer):

    class Meta:
        model = Token
        fields = ['tag', ]

    tag = ReadOnlyField()


class NFTCategoryModelSerializer(ModelSerializer):

    class Meta:
        model = NFTCategoryModel
        fields = ['name', ]

    name = ReadOnlyField()


class NFTOwnerModelSerializer(ModelSerializer):

    class Meta:
        model = NFTOwnerModel
        fields = ['name', 'photo']

    name = ReadOnlyField()
    photo = ImageField(read_only=True)


class NFTModelSerializer(ModelSerializer):

    class Meta:
        model = NFTModel
        fields = ['id', 'image', 'category', 'creator', 
        'owner', 'network', 'contract_address', 'id_token', 
        'royalty', 'fee', 'description', 'price', 'token', ]
    
    id = ReadOnlyField()
    image = ImageField(read_only=True)
    category = NFTCategoryModelSerializer(read_only=True)
    creator = ReadOnlyField()
    owner = NFTOwnerModelSerializer(read_only=True)
    network = ReadOnlyField()
    contract_address = ReadOnlyField()
    id_token = ReadOnlyField()
    royalty = ReadOnlyField()
    fee = ReadOnlyField()
    description = ReadOnlyField()
    price = ReadOnlyField()
    token = TokenSerializer(read_only=True)