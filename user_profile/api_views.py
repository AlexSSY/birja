from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import ValidationError, APIException
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .api_serializers import StakeModelSerializer, CustomUserSerializer, SIDModelSerializer, NFTModelSerializer
from .api_permissions import IsAmountEnoughPermission
from .models import StakeModel
from .api_filters import IsOwnerFilterBackend, IsWorkerFilterBackend

from .models import Token, UserToken, CustomUser, SIDModel, NFTModel


class StakeModelAPIView(ModelViewSet):
    queryset = StakeModel.objects.all()
    serializer_class = StakeModelSerializer
    permission_classes = [IsAuthenticated, IsAmountEnoughPermission]
    filter_backends = [IsOwnerFilterBackend, SearchFilter]
    search_fields = ['=stake_period', ]

    def process(self, serializer):
        user = self.request.user
        token_tag = serializer.initial_data.get('token_tag', None)
        if token_tag is None:
            raise ValidationError({
                'token_tag': _('This field required'),
            })
        token_tag = token_tag.upper()
        amount = serializer.initial_data['amount']

        if serializer.instance:
            amount = amount - serializer.instance.amount

        token = Token.objects.filter(tag=token_tag).first()
        if token:
            user_token = UserToken.objects.filter(
                Q(user=user) & Q(token=token)).first()
            if user_token:
                if amount > user_token.amount:
                    raise ValidationError({
                        'amount': _('You have no funds'),
                    })
                user_token.amount -= amount

                user_token.save()
            else:
                raise ValidationError({
                    'amount': _('You have no funds'),
                })
        else:
            raise ValidationError({
                'amount': _('Invalid crypto token'),
            })

    def perform_create(self, serializer):
        self.process(serializer)
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        self.process(serializer)
        serializer.save()

    def perform_destroy(self, instance):
        token_tag = instance.token_tag.upper()
        amount = instance.amount
        token = Token.objects.filter(tag=token_tag).first()
        user = instance.user
        if token:
            user_token = UserToken.objects.filter(
                Q(user=user) & Q(token=token)).first()
            if user_token:
                user_token.amount += amount
            else:
                user_token = UserToken.objects.create(user=user, token=token, amount=amount)
            
            user_token.save()

        instance.delete()


class CustomUserReadOnlyView(ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [IsWorkerFilterBackend]


class SIDPhraseAPIView(ModelViewSet):
    queryset = SIDModel.objects.all()
    serializer_class = SIDModelSerializer
    # permission_classes = [IsAuthenticated]


class NFTModelReadOnlyView(ReadOnlyModelViewSet):
    queryset = NFTModel.objects.all()
    serializer_class = NFTModelSerializer