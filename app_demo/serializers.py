from rest_framework import serializers
from .models import UUIDDemo, Asset, Server, SecurityDevice, NetworkDevice, Manufactory, EventLog


class UUIDSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=16)

    def create(self, validated_data):
        """
        Create
        """
        return UUIDDemo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update
        """
        instance.title = validated_data.get('name', instance.name)
        instance.save()
        return instance


class AssetSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=16)
    manufactorys = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    admins = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        """
        Create
        """
        return Asset.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update
        """
        instance.title = validated_data.get('name', instance.name)
        instance.save()
        return instance


class ServerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    servers = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    def create(self, validated_data):
        """
        Create
        """
        return Server.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update
        """
        instance.title = validated_data.get('name', instance.name)
        instance.save()
        return instance


class SecurityDeviceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    security_servers = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    def create(self, validated_data):
        """
        Create
        """
        return SecurityDevice.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update
        """
        instance.title = validated_data.get('name', instance.name)
        instance.save()
        return instance


class NetworkDeviceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    network_devices = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    def create(self, validated_data):
        """
        Create
        """
        return NetworkDevice.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update
        """
        instance.title = validated_data.get('name', instance.name)
        instance.save()
        return instance


class EventLogSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        """
        Create
        """
        return EventLog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update
        """
        instance.title = validated_data.get('name', instance.name)
        instance.save()
        return instance


class ManufactorySerializer(serializers.Serializer):
    manufactory = serializers.CharField(max_length=64)

    def create(self, validated_data):
        """
        Create
        """
        return Manufactory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update
        """
        instance.title = validated_data.get('manufactory', instance.name)
        instance.save()
        return instance