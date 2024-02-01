from rest_framework import serializers
from Myofficehour.models import Officehour,Location,Status,Participant

class OfficehourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Officehour
        fields = ["id","when","created_at","updated_at"]

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id","officehour","location","mapURL","created_at","updated_at"]

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ["id","status","created_at","updated_at"]

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ["id","officehour","name","email","ip","ua","created_at","updated_at"]

class ListviewSerializer(serializers.ModelSerializer):

    latest_location = serializers.SerializerMethodField()
    latest_status = serializers.SerializerMethodField()
    participants_count = serializers.SerializerMethodField()


    class Meta:
        model = Officehour
        fields = ["id","when","latest_location","latest_status","participants_count"]

    def get_latest_location(self, instance):
        latest_location = instance.location_set.order_by('-created_at').first()
        if latest_location:
            return {
                'location': latest_location.location
            }
        return None

    def get_latest_status(self, instance):
        latest_status = instance.status_set.order_by('-created_at').first()
        if latest_status:
            return {
                'status': latest_status.status
            }
        return None

    def get_participants_count(self, instance):
        return instance.participant_set.count()



