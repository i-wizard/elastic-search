from drf_yasg import openapi

CHARACTER_OBJECT = {
    "data": {
        "id": "7420c2ab42dc41cbaceb4faee5e8491d",
        "created_at": "2023-03-18T16:08:09.985044Z",
        "updated_at": "2023-03-18T16:08:09.985171Z",
        "deleted_at": None,
        "is_deleted": False,
        "first_name": "Hank",
        "last_name": "Schrader",
        "date_of_birth": "1982-02-23",
        "occupation": "Business",
        "is_suspect": False
    },
    "message": "Character added successfully",
    "status": "success"
}
CREATE_CHARACTER_BAD_INPUT = {
    "errors": {
        "first_name": [
            "This field is required."
        ],
        "last_name": [
            "This field is required."
        ],
        "date_of_birth": [
            "This field is required."
        ],
        "occupation": [
            "This field is required."
        ]
    },
    "message": "",
    "status": "error"
}
LOCATION_OBJECT = {
    "data": {
        "id": "fae5d95433654330ab9a4c763adf9501",
        "character": {
            "id": "7420c2ab42dc41cbaceb4faee5e8491d",
            "created_at": "2023-03-18T16:08:09.985044Z",
            "updated_at": "2023-03-18T16:08:09.985171Z",
            "deleted_at": None,
            "is_deleted": False,
            "first_name": "Walter",
            "last_name": "White",
            "date_of_birth": "1982-02-23",
            "occupation": "Business",
            "is_suspect": False
        },
        "created_at": "2023-03-18T18:44:48.175040Z",
        "updated_at": "2023-03-18T18:44:48.175080Z",
        "deleted_at": None,
        "is_deleted": False,
        "latitude": "40.7116670",
        "longitude": "-74.0136110"
    },
    "message": "Location added successfully",
    "status": "success"
}
CREATE_LOCATION_BAD_INPUT = {
    "errors": {
        "longitude": [
            "This field is required."
        ],
        "latitude": [
            "This field is required."
        ],
        "character_id": [
            "This field is required."
        ]
    },
    "message": "",
    "status": "error"
}
CREATE_CHARACTER_RESPONSE = {
    201: openapi.Response(description="Character added successfully", examples={"application/json": CHARACTER_OBJECT}),
    400: openapi.Response(
        description="Bad Input", examples={"application/json": CREATE_CHARACTER_BAD_INPUT}
    ),

}
START_DATE_FILTERS = openapi.Parameter(
    "start_date",
    in_=openapi.IN_QUERY,
    description="Start date  for date-range search using the date of creation. The results of the search will include this value",
    type=openapi.TYPE_STRING,
)

END_DATE_FILTERS = openapi.Parameter(
    "end_date",
    in_=openapi.IN_QUERY,
    description="End date for date-range search using the date of creation. The results of the search will include this value",
    type=openapi.TYPE_STRING,
)
NAME_FILTERS = openapi.Parameter(
    "name",
    in_=openapi.IN_QUERY,
    description="This could either be the firstname or the lastname. The results of this search will include characters whose first or last name partially or fully match the entered value (case insensitive)",
    type=openapi.TYPE_STRING,
)
OCCUPATION_FILTERS = openapi.Parameter(
    "occupation",
    in_=openapi.IN_QUERY,
    description="The results of this search will include characters whose occupation partially or fully match the entered value (case insensitive)",
    type=openapi.TYPE_STRING,
)
CHARACTER_FILTERS = openapi.Parameter(
    "character_id",
    in_=openapi.IN_QUERY,
    description="This will be the ID of the character. The results of this search will include only locations of the character whose ID was entered.",
    type=openapi.TYPE_STRING,
)
LONGITUDE_FILTERS = openapi.Parameter(
    "longitude",
    in_=openapi.IN_QUERY,
    description="This will be the longitude of a specific geographical point.",
    type=openapi.TYPE_STRING,
)
LATITUDE_FILTERS = openapi.Parameter(
    "latitude",
    in_=openapi.IN_QUERY,
    description="This will be the latitude of a specific geographical point.",
    type=openapi.TYPE_STRING,
)
MAX_DISTANCE_FILTERS = openapi.Parameter(
    "max_distance",
    in_=openapi.IN_QUERY,
    description="This will be the distance in METERS. The results of this filter will include only locations that are within the entered max distance.",
    type=openapi.TYPE_NUMBER,
)
IS_SUSPECT_FILTERS = openapi.Parameter(
    "is_suspect",
    in_=openapi.IN_QUERY,
    description="This could be true or false. This will filter based on the suspect status of the character.",
    type=openapi.TYPE_BOOLEAN,
)
ORDER_BY_FILTERS = openapi.Parameter(
    "orderBy",
    in_=openapi.IN_QUERY,
    enum=["first_name", "last_name", "date_of_birth"],
    description="This will order the returned result using this value.",
    type=openapi.TYPE_STRING,
)
ASCENDING_FILTERS = openapi.Parameter(
    "ascending",
    in_=openapi.IN_QUERY,
    enum=["1", '0'],
    description="This will decide the order the results wil return in. 1 means ascending order and 0 means descending order. Default value is 1",
    type=openapi.TYPE_STRING,
)

LIST_CHARACTER_RESPONSE = {
    200: openapi.Response(description="Data retrieved successfully", examples={"application/json": [{**CHARACTER_OBJECT, "message":"Data retrieved successfully"}]}),

}
CHARACTER_NOT_FOUND = {"application/json": {"message": "Character not found"}}
LOCATION_NOT_FOUND = {"application/json": {"message": "Location entry not found"}}
UPDATE_CHARACTER_RESPONSE = {
    200: openapi.Response(description="Character updated successfully", examples={"application/json": {**CHARACTER_OBJECT, "message":"Character updated successfully"}}),
    400: openapi.Response(
        description="Bad Input", examples={"application/json": CREATE_CHARACTER_BAD_INPUT}
    ),
    404: openapi.Response(
        description="Character does not exist", examples=CHARACTER_NOT_FOUND
    )

}

RETRIEVE_CHARACTER_RESPONSE = {
    200: openapi.Response(description="Character retrieved successfully", examples={"application/json": {**CHARACTER_OBJECT, "message":"Data retrieved successfully"}}),
    404: openapi.Response(
        description="Character does not exist", examples=CHARACTER_NOT_FOUND
    )
}
DELETE_CHARACTER_RESPONSE = {
    200: openapi.Response(description="Character deleted successfully", examples={"application/json": {"message":"Character deleted successfully"}}),
    404: openapi.Response(
        description="Character does not exist", examples=CHARACTER_NOT_FOUND
    )
}

CREATE_LOCATION_RESPONSE = {
    201: openapi.Response(description="Location added successfully", examples={"application/json": LOCATION_OBJECT}),
    400: openapi.Response(
        description="Bad Input", examples={"application/json": CREATE_LOCATION_BAD_INPUT}
    ),
    404: openapi.Response(
        description="Character does not exist", examples=CHARACTER_NOT_FOUND
    )

}
LIST_LOCATION_RESPONSE = {
    200: openapi.Response(description="Locations retrieved successfully", examples={"application/json": [{**LOCATION_OBJECT, "message":"Data retrieved successfully"}]}),
}
UPDATE_CHARACTER_RESPONSE = {
    200: openapi.Response(description="Location updated successfully", examples={"application/json": {**LOCATION_OBJECT, "message":"Location updated successfully"}}),
    400: openapi.Response(
        description="Bad Input", examples={"application/json": CREATE_LOCATION_BAD_INPUT}
    ),
    404: openapi.Response(
        description="Location does not exist", examples=LOCATION_NOT_FOUND
    )

}
RETRIEVE_LOCATION_RESPONSE = {
    200: openapi.Response(description="Location retrieved successfully", examples={"application/json": {**LOCATION_OBJECT, "message":"Data retrieved successfully"}}),
    404: openapi.Response(
        description="Location does not exist", examples=LOCATION_NOT_FOUND
    )
}
DELETE_LOCATION_RESPONSE = {
    200: openapi.Response(description="Location deleted successfully", examples={"application/json": {"message":"Location entry deleted successfully"}}),
    404: openapi.Response(
        description="Location does not exist", examples=LOCATION_NOT_FOUND
    )
}