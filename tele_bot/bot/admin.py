from django.contrib import admin
from .models import FieldOfLaw,StatementsOfClaim,Regulations
from .forms import RegulationsForm, StatementsOfClaimForm


@admin.register(FieldOfLaw)
class FieldOfLawAdmin(admin.ModelAdmin):
    list_display = ('id', 'theses', 'legal_flag')


@admin.register(StatementsOfClaim)
class StatementsOfClaimAdmin(admin.ModelAdmin):
    list_display = ('id','title','document', 'action_algorithm')
    form = StatementsOfClaimForm


@admin.register(Regulations)
class RegulationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'legal_flag','main_question')
    form = RegulationsForm