# smartsheet-pydantic
Smartsheet Python SDK wrapper, incorporating Pydantic models for type validation to guarantee successful data read/updates into Smartsheet.

Smartsheet API requires the incoming data to comply with Smartsheet column types. When the types do not align then the write call can fail. In order streamline the data validation this package piggybacks off the Pydantic BaseModel structure and their data validation capabilities as a "SmartModel".

This package also provides frameworks to create a "DataSource" class which you can declaratively define your data source and attach it to the SmartModel, so you can have a standard method of querying your datasource and create/update into Smartsheet.

# Installation
__requires python greater than 3.10__

Standard installation using pip install, and package import.
```
pip install smartsheet-pydantic
```

```python
# The package name uses underscore "_" instead of hyphen
import smartsheet_pydantic
```

# Example
## Defining a DataSource
```python
# DataSource class to call a RESTful API endpoint.
class ExampleRestAPI(DataSourceAPI):
    url = 'http://127.0.0.1:8000/weather_data'


# DataSource class for PostgreSQL database
class ExamplePostgres(DataSourcePostgres):
    user: str          = "username"
    password: str      = "password"
    host: str          = "host name"
    database: str      = "database name"
    query: str         = "query string"
    columns: list[str] = [ "index", "date", "value" ]
```

## Defining a SmartModel
```python
from datetime import date


class PostgresData(SmartModel):

    index: str
    date: date
    value: int | None

    class Configuration
        """
        unique_key: this key is used to match existing data in Smartsheet when
                    data is being updated. add multiple columns to make the
                    data unique.

        key_mapping: this dictionary is used to force match the source column
                     with the SmartModel attribute names if they do not match.
                     enter none if the names are exactly the same.
        """
        unique_key: list[str] = ['index']
        key_mapping: dict = None
```

## Generating the controller
The __controller__ is what utilizes the __DataSource__ and __SmartModels__ to read/write/update to and from Smartsheet. We can enter all necessary data into the __SheetDetail__ typed dictionary to more conveniently to generate a new controller.

```python
from smartsheet_pydantic import \
    SheetDetail, SmartsheetControllerFactory, SmartModel, DataSource

sheet_detail = SheetDetail(
    sheet_id: int = 0123456789
    description: str = "Description of the target Smartsheet"
    smart_model: SmartModel = PostgresData # created in the previous example
    source: DataSource = ExamplePostgres # created in the previous example
)

controller_factory = SmartsheetControllerFactory(sheet_detail)

controller = controller_factory.get_controller()
```

## Using the controller
```python
# Extract all data from the target Smartsheet with pre-defined data validation.
data: list[PostgresData] = controller.extract_as_smartmodel()

# Write new or update existing data into Smartsheet
data: list[PostgresData]
controller.update_rows(data)

# Using the pre-defined data source, refresh the Smartsheet. This process is
# additive, so based on the unique_key it will either update the values, or add
# new values. But it will not delete any unreferenced rows.
controller.create_or_update()

# Delete the entire content of the Smartsheet (maintains existing columns).
# Use this when there is no repercussion for deleting existing data, and you
# want to populate the sheet with fresh new data.
controller.delete_all_rows()
```