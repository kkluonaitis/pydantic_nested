# Pydantic Nested


This Python library allows you to create **Pydantic models** with support for nested dictionaries, lists, default values, and field constraints. The schema is defined using standard Python types and Pydantic's features.

## Features
- Supports simple fields (e.g., `str`, `int`, `float`)
- Nested dictionaries and lists
- Default values for fields
- Pydantic field constraints (e.g., `conint`, `conlist`)
- Full validation with dynamically created models


## Usage

Where could this be useful?
Sometimes data models can be very nested. Also, API queries exposing search engines such as elasticsearch can get convoluted and required validation.
Models defined in dictionary format instead of classes could be easier to read.

### Define the model

```python
from pydantic import Field, conint, conlist
from pydantic_nested.model import create_nested_model

schema = {
    "str1": str,
    "str2": (str, "default_string"),
    "str3": (str | None, None),
    "str4": (str, Field("str4 default value", description="str4 description")),
    "list1": list,
    "list2": list | tuple,
    "list3": list[int | str],
    "list4": (list, None),
    "list5": (list[float], Field(default_factory=list)),
    "dict1": {
        "str1": (str | None, None),
        "str2": (str, "default_string"),
    },
    "dict2": {"product_ids": conlist(int, min_length=1, max_length=20)},
    "dict3": {"include": {"product_ids": list[conint(ge=1)]}},
    "dict_list_nullable": (
        {
            "str1": (str | None, None),
            "str2": (str, "default_string"),
        },
        None,
    ),
    "list_of_objects1": [{"str1": str}],
    "list_of_objects2": [{"str1": str}, {"bool1": bool}],
    "list_of_objects3": ([{"str1": str}, {"bool1": bool}], None),
    "list_of_objects4": ([{"str1": str}, {"bool1": bool}], Field(default_factory=list, max_length=5)),
}
```

### Create the model

###
```python
TestModel = create_nested_model(schema, "TestModel")

sample_data = {
    "str1": "example string",
    "list1": [1, 2, 3],
    "list2": (1, 2),
    "list3": ["1", 2],
    "dict1": {},
    "dict2": {"product_ids": [1, 2, 3]},
    "dict3": {"include": {"product_ids": [1, 2, 3]}},
    "list_of_objects1": [{"str1": "object1"}],
    "list_of_objects2": [{"bool1": True}],
}

# Instantiate the model and validate the data
model_instance = TestModel(**sample_data)
print(model_instance.dict())
```
