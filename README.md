# OpenPlantbook-client
This is repository for Open Plantbook API release notes, documentation and sample clients

## Requirements
In order to use this API you need to login to Open Plantbook web UI at https://open.plantbook.io and generate API credentials. The credentials are client_id and client_secret. API authentication implements OAuth2 standard Client Credentials Grant flow.

## Documentation
- [API documentation](https://documenter.getpostman.com/view/12627470/TVsxBRjD)
- [Web UI documentation](https://github.com/slaxor505/OpenPlantbook-client/wiki)

## WebUI and API Release notes:

### release 2209 (19 September 2022)
UI updates:
- Added validation when saving a modified Public Plant. User cannot save modified public plant if its no attributes have been modified.
- Added stylised notifications to reflect results of operations
- Added "Category" when creating and modifying plants
- Other minor UI fixes and improvements

API updates and changes (see [API documentation](https://documenter.getpostman.com/view/12627470/TVsxBRjD) for details):
- Plant Search endpoint now returns combined user + public plants result with deduplication.
- Plant Search results now include plant's Category.
- Introduced search selector "userplant" to Plant Search endpoint. Now it is possible to search public and user plants, and get separate (user/public) and combined results.
- Plant Details endpoint returns extra field "'user_plant': True" if resulting plant is user-plant.
- Added "Category" field when creating and modifying plants

Maintenance:
- Updated web framework and libraries to the secure and vulnerabilities free versions.

### release 2205 (25 May 2022):
Now all plant image requests are proxied/cached using CloudFlare servers across the globe so images are fast to download independently on your location on the planet.

### version 1.04 (20 July 2021)
Major UI update. Now Users can:
- Modify existing Public-Plants using "Modify" button in Browse DB.
- Add new Plants using "Add Plant" button in side Menu. Plant is cloned into User-Plant and visible in "My Plants" side menu.
- Modify own User-Plants via "My Plants" side menu.
- The only way to delete User-Plant at the moment is via API DELETE call. UI-based deletion will be available in next release.

The detailed documentation about UI Add/Modify operations is available in [Wiki](https://github.com/slaxor505/OpenPlantbook-client/wiki). 

### version 1.03 (26 December 2020)
Major update:
- Ability to add new and edit existing plants via API calls. (not UI yet)

Now user can update existing plant or create new one. 
There are 2 databases: user specific database (user's context) and main database (public).
- All modifications of plants (new, existing) are only visible for the user who have modified them. Later, moderator can merge these modifications into main public database.
- A modification of an existing plant creates a "shadow" or clone of the plant in the user context. 
- Once a plant has been updated, the user can only see this updated (shadow) version of the plant but not public version of it.
- Newly created plants are only available to the user who created them until a moderator merges them into a main database.
- It is not possible to create plant which already exists in a main DB. It can only be updated with API update call.
- New or updated plants can be deleted from user context.
- Once updated existing plant is deleted from user context (user's version of existing plant), the user can again retrieve a public version of the plant from main database.
  
### version 1.02
- Introduction of Plant images feature. api/v1/plant/detail/ endpoint returns Plant's image URL as image_url JSON string field.
- Web UI is generally available for guests. Guests can search Plant DB but to get API key and plants details Signing in is required.

### version 1.01
- Browse-DB feature in WebUI so it is possible to search plants available in DB.
- Small UI clean-ups

### version 1.0
Breaking changes in comparison with 1.0-RC:
- Removed api/v1/plant/detail/{id}/ endpoint
- Removed "id" from responses
- Now to get plant details use api/v1/plant/detail/{pid} endpoint.

## Client Release notes:

### version 1.0
- Updated Postman collection:
    - built-in variables for easier use (See variables specific to the Collection)
    - "Get token" call now extracts and updates {{access_token}} value automatically (no need to copy/paste)
- Added Python client by @Olen (https://github.com/Olen). Thanks and Kudos! The client is a step for Home-assistant.io integration and this is why it is a bit overcomplicated.  

## Integrations
- [home-assistant](https://www.home-assistant.io/) integration. [Plant Monitor component](https://github.com/Olen/homeassistant-plant) and [PlantCard](https://github.com/Olen/lovelace-flower-card) which leverage the component. Discussion of HASS forum [here](https://community.home-assistant.io/t/cloud-plant-db-with-api-for-plantcard/).

## Usage
The easiest way to get familiar with API is to use Browsable API within Web UI. The link can be found within Docs section.
Alternatively, you can use [API examples](https://documenter.getpostman.com/view/12627470/TVsxBRjD) in Postman. You need to install free Postman API tool: https://www.postman.com/ or use Postman online.

### Examples

**For up to date examples see [API documentation](https://documenter.getpostman.com/view/12627470/TVsxBRjD) Below example may be outdated**

#### Retrieve plant:

1. Get API credentials from Web UI.

2. Get access token using API credentials.
```
curl --request POST 'https://open.plantbook.io/api/v1/token/' \
--form 'grant_type=client_credentials' \
--form 'client_id=string_client_id_from_UI' \
--form 'client_secret=string_client_secret_from_UI'
```
Response will be:
```
{
    "access_token": "token_string",
    "expires_in": 2629800,
    "token_type": "Bearer",
    "scope": "read"
}
```
This is token to access API. It will expire in 2629800 seconds = 1 month. It is ok to get a new token everytime.
We will need "token_string" at next step.

3. Make a Plant Search API call with 'Bearer Token' HTTP header:
Query parameter ?alias=<search string> is required.
```
curl --request GET 'https://open.plantbook.io/api/v1/plant/search?alias=acanthus%20ilicifolius' \
--header 'Authorization: Bearer token_string'
```
From the response, you can to get Plant Id (pid) in order to get the plant details.
```
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "pid": "acanthus ilicifolius",
            "display_pid": "Acanthus ilicifolius",
            "alias": "acanthus ilicifolius"
        },
        {
            "pid": "acanthus spinosus",
            "display_pid": "Acanthus spinosus",
            "alias": "acanthus ilicifolius"
        }
    ]
}
```
4.  From previous step, take "pid" value of the desired plant and get the plant details with Bearer Token. 

```
curl --request GET 'https://open.plantbook.io/api/v1/plant/detail/acanthus ilicifolius/' \
--header 'Authorization: Bearer token_string'
```
```
{
    "pid": "acanthus ilicifolius",
    "display_pid": "Acanthus ilicifolius",
    "alias": "acanthus ilicifolius",
    "max_light_mmol": 2500,
    "min_light_mmol": 1200,
    "max_light_lux": 6000,
    "min_light_lux": 1500,
    "max_temp": 32,
    "min_temp": 10,
    "max_env_humid": 80,
    "min_env_humid": 30,
    "max_soil_moist": 60,
    "min_soil_moist": 15,
    "max_soil_ec": 2000,
    "min_soil_ec": 350,
    "image_url": "https://example.com/n/sdpo/b/plant-img/o/acanthus%20ilicifolius.jpg"
}
```

#### Plant modifications example:

1. Create new plant:

```Shell
curl --request POST 'http://open.plantbook.io/api/v1/plant/create' \
--header 'Authorization: Bearer token_string' \
--header 'Content-Type: application/json' \
--data-raw '{
    "display_pid": "Solanum lycopersicum",
    "alias": "Tomato",
    "max_light_mmol": 7600,
    "min_light_mmol": 3200,
    "max_light_lux": 55000,
    "min_light_lux": 3000,
    "max_temp": 33,
    "min_temp": 12,
    "max_env_humid": 80,
    "min_env_humid": 15,
    "max_soil_moist": 60,
    "min_soil_moist": 20,
    "max_soil_ec": 2000,
    "min_soil_ec": 350
}'
```

Response:

```JSON
{
    "pid": "solanum lycopersicum",
    "display_pid": "Solanum lycopersicum",
    "alias": "Tomato",
    "max_light_mmol": 7600,
    "min_light_mmol": 3200,
    "max_light_lux": 55000,
    "min_light_lux": 3000,
    "max_temp": 33,
    "min_temp": 12,
    "max_env_humid": 80,
    "min_env_humid": 15,
    "max_soil_moist": 60,
    "min_soil_moist": 20,
    "max_soil_ec": 2000,
    "min_soil_ec": 350,
    "image_url": "https://objectstorage.ap-sydney-1.oraclecloud.com/n/sdyd5yr3jypo/b/plant-img/o/solanum%20lycopersicum.jpg"
}
```

Take pid value (not display_name)

2. Update this plant:

```shell
curl --request PATCH 'http://open.plantbook.io/api/v1/plant/update' \
--header 'Authorization: Bearer token_string' \
--header 'Content-Type: application/json' \
--data-raw '{
    "pid": "solanum lycopersicum",
    "max_light_mmol": 1111,
    "min_light_mmol": 2222,
    "max_light_lux": 4444,
    "min_light_lux": 3333,
    "max_temp": 66,
    "min_temp": 55
}'
```

Response:

```json
{
    "pid": "solanum lycopersicum",
    "display_pid": "Solanum lycopersicum",
    "alias": "Tomato",
    "max_light_mmol": 1111,
    "min_light_mmol": 2222,
    "max_light_lux": 4444,
    "min_light_lux": 3333,
    "max_temp": 66,
    "min_temp": 55,
    "max_env_humid": 80,
    "min_env_humid": 15,
    "max_soil_moist": 60,
    "min_soil_moist": 20,
    "max_soil_ec": 2000,
    "min_soil_ec": 350,
    "image_url": "https://objectstorage.ap-sydney-1.oraclecloud.com/n/sdyd5yr3jypo/b/plant-img/o/solanum%20lycopersicum.jpg"
}
```

3. Delete the plant:

```shell
curl --request DELETE 'http://open.plantbook.io/api/v1/plant/delete' \
--header 'Authorization: Bearer token_string' \
--header 'Content-Type: application/json' \
--data-raw '{
    "pid": "solanum lycopersicum"
}'
```
Response:

Status: 204 No content
