from turtle import distance
from typing import Union

from django.db.models.functions import Cast, Sqrt, Radians, Power
from django.db.models import Q, QuerySet, F, FloatField
from django.contrib.postgres.search import SearchVector

from breaking_bad.models import Character, Location
from helpers.db_helpers import update_object
from helpers.exceptions import CustomAPIException
from helpers.utils import Validators


class CharacterService:
    @classmethod
    def get_character(cls, raise_404=True, **kwargs) -> Union[Character, None]:
        """
        This services tries to get a single character using the key word args
        passed
        if the object does not exist and the raise_404 flag
        is true it raises a 404  else it returns the object or None
        """
        character = Character.objects.filter(**kwargs).first()
        if not character and raise_404:
            raise CustomAPIException("Character not found", 404)
        return character

    @classmethod
    def list_characters(cls, filter_params) -> QuerySet:
        name: str = filter_params.get("name", "")
        is_suspect: str = filter_params.get("is_suspect", "")
        occupation: str = filter_params.get("occupation", "")
        orderBy: str = filter_params.get("orderBy", "")
        ascending: str = filter_params.get("ascending", '1')

        queryset = Character.objects.all()
        if name:
            queryset = queryset.annotate(combined_name=SearchVector("first_name", "last_name")).filter(
                Q(combined_name__icontains=name) | Q(combined_name=name))
        if is_suspect.lower() in ["true", "false"]:
            queryset = queryset.filter(
                is_suspect=True if is_suspect == "true" else False)
        if occupation:
            queryset = queryset.filter(occupation__icontains=occupation)
        if orderBy.lower() in ["first_name", "last_name", "date_of_birth"]:
            orderBy = f"-{orderBy}" if ascending == '0' else orderBy
            queryset = queryset.order_by(orderBy)
        return queryset

    @classmethod
    def delete_character(cls, pk) -> None:
        character: Character = CharacterService.get_character(id=pk)
        character.delete()
        return

    @classmethod
    def search_character(cls, keyword):
        from elasticsearch_dsl import Q, Search
        from .documents import CharacterIndex
        
        # Create a search object
        search = Search(index='character')

        # Define the search query
        # query = Q('match', first_name=keyword)
        query = Q('bool', should=[
            Q('match', first_name=keyword),
            Q('range', created_at={'gte': 'now-7d/d', 'lt': 'now/d'})
        ])

        # Add the query to the search object
        search = search.query(query)

        # Execute the search and get the results
        response = search.execute()

        # Extract the Product objects from the Elasticsearch documents
        characters = [hit.django for hit in response]

        return characters


class LocationService:

    @classmethod
    def get_location(cls, raise_404=True, **kwargs) -> Union[Location, None]:
        """
        This services tries to get a single location entry using the keyword args
        passed
        if the object does not exist and the raise_404 flag
        is true it raises a 404  else it returns the object or None
        """
        location = Location.objects.filter(**kwargs).first()
        if not location and raise_404:
            raise CustomAPIException("Location entry not found", 404)
        return location

    @classmethod
    def add_location(cls, data) -> Location:
        character = CharacterService.get_character(id=data.pop("character_id"))
        return Location.objects.create(**data, character=character)

    @classmethod
    def list_locations(cls, filter_params) -> QuerySet:
        longitude: str = filter_params.get("longitude", "")
        latitude: str = filter_params.get("latitude", "")
        start_date: str = filter_params.get("start_date")
        end_date: str = filter_params.get("end_date")
        character_id: str = filter_params.get("character_id")
        ascending: str = filter_params.get("ascending", '1')
        max_distance: str = filter_params.get("max_distance")

        queryset = Location.objects.all()
        if Validators.is_valid_date_format(start_date):
            queryset = queryset.filter(created_at__gte=start_date)
        if Validators.is_valid_date_format(end_date):
            queryset = queryset.filter(created_at__lte=end_date)
        if Validators.is_start_date_less_than_or_equals_end_date(start_date, end_date):
            queryset = queryset.filter(
                created_at__range=(start_date, end_date))
        if character_id:
            queryset = queryset.filter(character__id=character_id)
        if longitude and latitude:
            earth_radius = 6371 * 1000  # this will convert the unit to meters
            # using Haversine formula
            distance = Cast(Sqrt(
                Power(Radians(latitude - F('latitude')), 2) +
                Power(Radians(longitude - F('longitude')), 2)
            ) * earth_radius, FloatField())
            orderBy = "-distance" if ascending == "0" else "distance"
            queryset = queryset.annotate(distance=distance).order_by(orderBy)
            if max_distance:
                queryset = queryset.filter(distance__lte=max_distance)
        return queryset

    @classmethod
    def update_location(cls, pk, data) -> Location:
        location = cls.get_location(id=pk)
        if data.get("character_id"):
            character = CharacterService.get_character(
                id=data.pop("character_id"))
            data["character"] = character
        return update_object(location, data)

    @classmethod
    def delete_location(cls, pk) -> None:
        location = cls.get_location(id=pk)
        location.delete()
        return
