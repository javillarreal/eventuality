import re
from datetime import datetime
from typing import Tuple, List

from ..graphql.exception import ExceptionType


def get_model_fields(model, include_fields: List[str] = [], **kwargs: dict) -> Tuple[dict, dict]:
    model_name = str(model.__name__)
    model_name = re.sub(r'(?<!^)(?=[A-Z])', '_', model_name).lower()
    
    model_fields = [
        str(field).replace(model_name + '.', '') 
        for field in model.__table__.columns
    ]
    
    model_fields_kwargs = dict()
    other_fields_kwargs = dict()
    for key, value in kwargs.items():
        if key in model_fields or key in include_fields:
            model_fields_kwargs[key] = value
        else:
            other_fields_kwargs[key] = value

    return model_fields_kwargs, other_fields_kwargs


def is_valid_id(model, id: int, input_name: str = 'id'):
    instance = model.query.get(id)
    
    if not instance:
        exception = ExceptionType(
            field=input_name,
            message=f"{model.__name__} with id {id} not found"
        )
        
        return exception


def is_value_unique(model, value, input_name: str = 'id'):
    existing_record = model.query.filter(getattr(model, input_name)==value).scalar()
    
    if existing_record:
        exception = ExceptionType(
            field=input_name,
            message=f"'{value}' {input_name} already exists"
        )

        return exception


def resource_exists(model, value, input_name: str = 'id'):
    instance = model.query.filter(getattr(model, input_name)==value).scalar()

    if not instance:
        exception = ExceptionType(
            field=input_name,
            message=f"{model.__name__} with {input_name} '{value}' not found"
        )
        
        return exception
    
    return instance


def validate_dates(datetime_from: datetime, datetime_to: datetime = None):

    current_date = datetime.now()
    if current_date > datetime_from:
        exception = ExceptionType(
            field='datetime_from',
            message=f"Check the datetime_from value. {datetime_from} is a date in the past"
        )
        return exception

    if datetime_to is not None:
        if current_date > datetime_from:
            exception = ExceptionType(
                message=f"Check the datetimes values. {datetime_to} is older than {datetime_from}"
            )
            return exception
