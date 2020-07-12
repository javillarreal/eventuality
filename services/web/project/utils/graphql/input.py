from datetime import datetime
from typing import Tuple

from ..graphql.exception import ExceptionType


def get_model_fields(model, **kwargs: dict) -> Tuple[dict, dict]:
    model_name = str(model.__name__).lower()
    model_fields = [
        str(field).replace(model_name + '.', '') 
        for field in model.__table__.columns
    ]
    
    model_fields_kwargs = dict()
    other_fields_kwargs = dict()
    for key, value in kwargs.items():
        if key in model_fields:
            model_fields_kwargs[key] = value
        else:
            other_fields_kwargs[key] = value

    return model_fields_kwargs, other_fields_kwargs


def is_valid_id(model, id: int, input_name: str = 'id'):
    ok, exception = True, None

    instance = model.query.get(id)
    if not instance:
        ok = False
        exception = ExceptionType(
            field=input_name,
            message=f"{model.__name__} with id {id} not found"
        )
    
    return ok, exception


def is_value_unique(model, value, input_name: str = 'id'):
    ok, exception = True, None

    if not model.query.filter(model.username==value):
        ok = False
        exception = ExceptionType(
            field=input_name,
            message=f"{input_name} {value} is taken"
        )

    return ok, exception


def validate_dates(datetime_from: datetime, datetime_to: datetime = None):
    ok, exception = True, None
    
    current_date = datetime.now()
    if current_date > datetime_from:
        ok = False
        exception = ExceptionType(
            field='datetime_from',
            message=f"Check the datetime_from value. {datetime_from} is a date in the past"
        )

    if datetime_to is not None:
        if current_date > datetime_from:
            ok = False
            exception = ExceptionType(
                message=f"Check the datetimes values. {datetime_to} is older than {datetime_from}"
            )
    
    return ok, exception
