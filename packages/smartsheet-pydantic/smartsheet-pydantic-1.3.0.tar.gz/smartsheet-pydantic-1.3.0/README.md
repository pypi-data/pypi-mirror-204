# smartsheet-pydantic
## What is it?
Smartsheet Python SDK wrapper, incorporating Pydantic models for type validation to guarantee successful data read/updates into Smartsheet.

Smartsheet API requires the incoming data to comply with Smartsheet column types. When the types do not align then the write call can fail. In order streamline the data validation this package piggybacks off the Pydantic BaseModel structure and their data validation capabilities as a "SmartModel".

This package also provides frameworks to create a "DataSource" class which you can declaratively define your data source and attach it to the SmartModel, so you can have a standard method of querying your datasource and create/update into Smartsheet.

---

# Getting Started

## Install & Import The Module
__requires python greater than 3.10__
Standard installation using pip install, and package import.
```
pip install smartsheet-pydantic
```
```python
# The package name uses underscore "_" instead of hyphen
import smartsheet_pydantic
```

---


## Everything revolves around the __Controller__

__smartsheet_pydantic__ package's function revolves around the __Controller__. Once a Controller is setup, it can facilitate data extraction from the user designated data source (RESTful API or PostgreSQL) and refresh the designated Smartsheet using an additive approach (data is updated or added, but never deleted). The __Controller__ can also facilitate writing into the Smartsheet.

During both the write, read, or update of the Smartsheet the __smartsheet_pydantic__ as the name suggest uses __Pydantic__'s BaseModel to validate the data. This ensures the data has the write data type and will not fail to write to the given Smartsheet.



## Defining the Controller

In order to generate the Controller we will use the __SheetDetail__ class to collect the necessary details.

1. __sheet_id__: Every Smartsheet grid has a unique id, this is used to target the Smartsheet.
2. __description__: User defined description of the target Smartsheet to give some context. Can be anything.
3. __smart_model__: A __smartsheet-pydantic__ model we will create to aid in data validation (Extension of Pydantic BaseModel).
4. __source__: A __smartsheet-pydantic__ model we will create which contains the connection detail so data can be extracted from, and written into the target Smartsheet.

```python
from smartsheet_pydantic import SheetDetail, SmartModel, DataSource


sheet_detail = SheetDetail(
    sheet_id: int = 0123456789
    description: str = "Description of the target Smartsheet"
    smart_model: SmartModel = WeatherModel # we will create this in the subsequent steps
    source: DataSource = ExamplePostgres   # we will create this in the subsequent steps
)
```

---

## Defining a SmartModel
A __SmartModel__ class is an extension of Pydantic BaseModel. Therefore the definition of a __SmartModel__ is very similar. Define the data fields and their type as a class attribute.

You will also need to define 2 additional Configuration parameters.
1. __unique_key__: is a list of column names which the model will use to define uniqueness. When data in Smartsheet is updated these columns will be used to find and update the data if the data already exists.
2. __key_mapping__: if you have defined the data field names that differs from the source data, then this dictionary can be used to map and rename those columns. If the data field names are the same, the value must be set to None.

```python
from datetime import date


class WeatherModel(SmartModel):

    index: int
    date: date
    temperature: float
    humidity: float
    rain: bool

    class Configuration

        unique_key: list[int] = ['index']
        key_mapping: dict = None
```

---



## Defining a DataSource
There are options when creating a data source. One is a RESTful API endpoint, where the you can extend the __DataSourceAPI__ class, and provide a __url__ attribute. The other is a PostgreSQL database source using __DataSourcePostgres__, where you can provide the access details as well as the query to use, and the column name designations. We will use the latter in this example.

```python
# DataSource class to call a RESTful API endpoint.
class WeatherRestAPI(DataSourceAPI):
    url = 'http://127.0.0.1:8000/weather_data'


# DataSource class for PostgreSQL database
class ExamplePostgres(DataSourcePostgres):
    user: str          = "username"
    password: str      = "password"
    host: str          = "host name"
    database: str      = "database name"
    query: str         = 'SELECT * FROM weather_table WHERE location = "USA"'
    columns: list[str] = [ "index", "date", "temperature", "humidity", "rain" ]
```

---

## Generating the controller
Now that all of the components are ready we will now take the __SheetDetail__ instance, and provide it to the __SmartsheetControllerFactory__ class to generate a __ControllerFactory__. By calling on the __.get_controller()__ method we can generate the __SmarsheetController__ object.

```python
from smartsheet_pydantic import SmartsheetControllerFactory

controller_factory = SmartsheetControllerFactory(sheet_detail)
controller = controller_factory.get_controller()
```

---

## Using the controller

### Use the provided data source to refresh the target Smartsheet
```python
controller.refresh_smartsheet_from_source()
```

### Extracting data from Smartsheet
```python
data: list[WeatherData] = controller.extract_as_smartmodel()
```

### Manually write new data, or update existing data to Smartsheet
```python
data: list[WeatherData]
controller.update_rows(data)
```


### Delete all row data from Smartsheet
```python
controller.delete_all_rows()
```

---

# SmartModel
Not all data can be handled within the SmartModel. You may want to manipulate the data using Pandas or Numpy. Therefore SmartModel has methods to aid in the transforming of data into a SmartModel, as well as extracting data out into a dictionary.
## Extracting Data From SmartModel
```python
weather_data: list[WeatherData]
extracted_data: list[dict] = [smart_model.dict() for smart_model in weather_data]

print(extracted_data)
```
#### Results
```python
[
    {
        'index': 1
        'date': date(2023, 1, 1)
        'temperature': 65.2
        'humidity': 14.5
        'rain': False
    },
    {
        'index': 2
        'date': date(2023, 1, 2)
        'temperature': 67.2
        'humidity': 14.2
        'rain': False
    },
    {
        'index': 1
        'date': date(2023, 1, 3)
        'temperature': 62.3
        'humidity': 12.2
        'rain': False
    },
]

```

## Converting Data Into SmartModel
```python
extracted_data: list[dict]

weather_data: list[WeatherData] = \
    [WeatherData.from_source(data) for data in extracted_data]
```