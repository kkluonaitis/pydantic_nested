import types
from typing import (
    Any,
    Dict,
    List,
    Sequence,
    Set,
    Type,
    TypeAlias,
    Union,
    cast,
    get_origin,
)

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo
from typing_extensions import Annotated


def is_basic_type(obj) -> bool:
    if obj in (
        str,
        int,
        bool,
        float,
        complex,
        bytes,
        list,
        dict,
        tuple,
        Union,  # To allow nullables and stuff.
        TypeAlias,
        Dict,
        List,
        Set,
        set,
        None,
    ):
        return True
    if type(obj) in (types.UnionType,):
        return True
    return False


def handle_dict(
    schema: dict[str, Any],
    model_name: str,
    model_suffix: str,
    **kwargs,
):
    fields = {}
    for key, value in schema.items():
        # Recursively create a model for the nested dictionary
        gen_v = create_pydantic_model(
            value,
            model_name=key.capitalize(),
            model_suffix=model_suffix,
        )
        fields[key] = gen_v if isinstance(gen_v, Sequence) else (gen_v, ...)
    return create_model(model_name + model_suffix, **fields, **kwargs)  # type: ignore


def handle_sequence(
    schema: Sequence,
    model_name: str,
    model_suffix: str,
    **kwargs,
):
    if isinstance(schema, list):
        return list[  # type: ignore
            Union[
                *[
                    create_pydantic_model(
                        sc,
                        model_name=model_name,
                        model_suffix=model_suffix,
                        **kwargs,
                    )
                    for sc in schema
                ]
            ]
        ]
    if len(schema) == 2:
        if isinstance(schema[1], FieldInfo):
            # (<type>, Field(...))
            sub_model = create_pydantic_model(
                schema[0],
                model_name=model_name,
                model_suffix=model_suffix,
                **kwargs,
            )
            # Perhaps refactor to remove these tuples with ellipses.
            sub_model = sub_model[0] if isinstance(sub_model, Sequence) else sub_model
            return (sub_model, schema[1])
        if is_basic_type(schema[0]) or is_basic_type(get_origin(schema[0])):
            if schema[1] is None or isinstance(schema[1], schema[0]):
                # (<type>, <default value>)
                sub_model = create_pydantic_model(
                    schema[0],
                    model_name=model_name,
                    model_suffix=model_suffix,
                    **kwargs,
                )
                if isinstance(sub_model, Sequence) and len(sub_model) == 2:
                    return (
                        sub_model[0],
                        schema[1],
                    )
                else:
                    return (sub_model, schema[1])

    if len(schema) == 0:
        return type(schema)


def create_pydantic_model(
    schema: Any,
    model_name: str,
    model_suffix: str = "Model",
    **kwargs,
) -> Type[BaseModel] | tuple[Any, ...]:
    """Dynamically creates nested pydantic models."""

    if isinstance(schema, dict):
        # handle nested object
        return handle_dict(
            schema=schema,
            model_name=model_name,
            model_suffix=model_suffix,
            **kwargs,
        )
    elif isinstance(schema, Sequence):
        return handle_sequence(
            schema,
            model_name=model_name,
            model_suffix=model_suffix,
            **kwargs,
        )
    elif schema is Annotated or get_origin(schema) is Annotated:
        # typing.Annotated[<type>, Field(...)]
        return (schema, ...)
    elif schema in (
        str,
        int,
        float,
        bool,
        complex,
        bytes,
        list,
        dict,
        tuple,
        Union,
        TypeAlias,
        Dict,
        List,
        Set,
        set,
    ):
        # Could get the args and continue recursing.
        return (schema, ...)
    elif get_origin(schema) in (list, tuple, dict, set):
        return (schema, ...)
    elif type(schema) is types.UnionType:  # noqa: E721
        return (schema, ...)

    raise ValueError(f"{schema} of type {type(schema)} is not supported.")


def create_nested_model(
    schema: Any,
    root_model_name: str = "RootModel",
    model_suffix: str = "Model",
    **kwargs,
) -> Type[BaseModel]:
    model = create_pydantic_model(
        schema,
        model_name=root_model_name,
        model_suffix=model_suffix,
        **kwargs,
    )
    model = cast(Type[BaseModel], model)
    return model
