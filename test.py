from pydantic import Field, conint, conlist
from pydantic_nested.model import create_nested_model
from pprint import pprint

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

TestModel = create_nested_model(schema, "TestModel")

###
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
pprint(model_instance.dict())