from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from breaking_bad.doc import schema_examples
from breaking_bad.serializers import CharacterSerializer, LocationSerializer, CreateLocationSerializer
from breaking_bad.service import CharacterService, LocationService
from helpers.utils import ResponseManager, paginate_response


class CharacterViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    
    @swagger_auto_schema(
        request_body=CharacterSerializer,
        operation_description="Create Character",
        operation_summary="This endpoint is to add a new character",
        tags=["Character"],
        responses=schema_examples.CREATE_CHARACTER_RESPONSE,
    )
    def create(self, request):
        serialized_data = CharacterSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(errors=serialized_data.errors, status=400)
        
        serialized_data.save()
        return ResponseManager.handle_response(data=serialized_data.data, message="Character added successfully", status=201)
    
    
    @swagger_auto_schema(
        operation_description="This endpoint is to list the characters",
        operation_summary="This endpoint is to list the characters, it also accepts some query parameters",
        tags=["Character"],
        manual_parameters=[
            schema_examples.NAME_FILTERS,
            schema_examples.IS_SUSPECT_FILTERS,
            schema_examples.OCCUPATION_FILTERS,
            schema_examples.ORDER_BY_FILTERS,
            schema_examples.ASCENDING_FILTERS
        ],
        responses=schema_examples.LIST_CHARACTER_RESPONSE,
    )

    def list(self, request):
        filter_params = request.GET
        queryset = CharacterService.list_characters(filter_params)
        return paginate_response(queryset=queryset, serializer_=CharacterSerializer, request=request)
    
    @swagger_auto_schema(
        request_body=CharacterSerializer,
        operation_description="Update an exsiting Character",
        operation_summary="This endpoint is to update an existing character",
        tags=["Character"],
        responses=schema_examples.UPDATE_CHARACTER_RESPONSE,
    )
    def partial_update(self, request, pk=None):
        character = CharacterService.get_character(id=pk)
        serialized_data = CharacterSerializer(character, data=request.data, partial=True)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(errors=serialized_data.errors, status=400)
        serialized_data.save()
        return ResponseManager.handle_response(data=serialized_data.data, message="Character updated successfully", status=200)
    
    @swagger_auto_schema(
        operation_description="This endpoint is to retrieve a single  characters",
        operation_summary="This endpoint is to retrieve a single characters, it raises a 404 exception if the character does not exist.",
        tags=["Character"],
        responses=schema_examples.RETRIEVE_CHARACTER_RESPONSE,
    )  
    def retrieve(self, request, pk=None):
        character = CharacterService.get_character(id=pk)
        return ResponseManager.handle_response(data=CharacterSerializer(character).data, message="Character retrieved successfully", status=200)
    
    @swagger_auto_schema(
        operation_description="This endpoint is to delete a single  character",
        operation_summary="This endpoint is to delete a single characters, it raises a 404 exception if the character does not exist.",
        tags=["Character"],
        responses=schema_examples.DELETE_CHARACTER_RESPONSE,
    ) 
    def destroy(self, request, pk=None):
        CharacterService.delete_character(pk)
        return ResponseManager.handle_response(data={}, message="Character deleted successfully", status=200)
        

class LocationViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    
    @swagger_auto_schema(
        request_body=CreateLocationSerializer,
        operation_description="Add location for a character",
        operation_summary="This endpoint is to add a new location for a character",
        tags=["Location"],
        responses=schema_examples.CREATE_LOCATION_RESPONSE,
    )
    def create(self, request):
        serialized_data = CreateLocationSerializer(data=request.data)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(errors=serialized_data.errors, status=400)
        location_instance = LocationService.add_location(serialized_data.validated_data)
        return ResponseManager.handle_response(data=LocationSerializer(location_instance).data, message="Location added successfully", status=201)
    
    @swagger_auto_schema(
        operation_description="This endpoint is to list the locations available",
        operation_summary="This endpoint is to list the locations, it also accepts some query parameters",
        tags=["Location"],
        manual_parameters=[
            schema_examples.START_DATE_FILTERS,
            schema_examples.END_DATE_FILTERS,
            schema_examples.CHARACTER_FILTERS,
            schema_examples.LONGITUDE_FILTERS,
            schema_examples.LATITUDE_FILTERS,
            schema_examples.MAX_DISTANCE_FILTERS,
            schema_examples.ASCENDING_FILTERS
        ],
        responses=schema_examples.LIST_LOCATION_RESPONSE,
    )
    def list(self, request):
        queryset = LocationService.list_locations(request.GET)
        return paginate_response(queryset, LocationSerializer, request)
    
    @swagger_auto_schema(
        request_body=CreateLocationSerializer,
        operation_description="Update exisiting location",
        operation_summary="This endpoint is to update an existing location.",
        tags=["Location"],
        responses=schema_examples.UPDATE_CHARACTER_RESPONSE,
    )
    def partial_update(self, request, pk=None):
        serialized_data = CreateLocationSerializer(data=request.data, partial=True)
        if not serialized_data.is_valid():
            return ResponseManager.handle_response(errors=serialized_data.errors, status=400)
        location_instance = LocationService.update_location(pk, serialized_data.validated_data)
        return ResponseManager.handle_response(data=LocationSerializer(location_instance).data, message="Location update successfully", status=200)
    
    @swagger_auto_schema(
        operation_description="This endpoint is to retrieve a single location",
        operation_summary="This endpoint is to retrieve a single location, it raises a 404 exception if the location does not exist.",
        tags=["Location"],
        responses=schema_examples.RETRIEVE_LOCATION_RESPONSE,
    ) 
    def retrieve(self, request, pk=None):
        location_instance = LocationService.get_location(id=pk)
        return ResponseManager.handle_response(data=LocationSerializer(location_instance).data, message="Location entry retrieved successfully", status=200)
    
    @swagger_auto_schema(
        operation_description="This endpoint is to delete a single location",
        operation_summary="This endpoint is to delete a single location, it raises a 404 exception if the location does not exist.",
        tags=["Location"],
        responses=schema_examples.DELETE_LOCATION_RESPONSE,
    ) 
    def destroy(self, request, pk=None):
        LocationService.delete_location(pk)
        return ResponseManager.handle_response(data={}, message="Location entry deleted successfully", status=200)
