from pathlib import Path
import jsonschema
from frictionless import Resource,Schema
from frictionless import transform
import requests
import petl as etl
# currently using fields.json and hardcoding 
jsonschema_url = (
"https://raw.githubusercontent.com/norc-heal/"
"heal-metadata-schemas/mbkranz/variable-lvl-csvs/"
"variable-level-metadata-schema/schemas/jsonschema/fields.json"
)
healjsonschema = requests.get(jsonschema_url).json()

healfrictionless = Schema(
        "https://raw.githubusercontent.com/norc-heal/heal-metadata-schemas/"
        "mbkranz/variable-lvl-csvs/"
        "variable-level-metadata-schema/schemas/frictionless/csvtemplate/fields.json"
    )

schema = {
    'type':'object',
    'required':[
        'title',
        'data_dictionary'
    ],
    'properties':{
        'title':{'type':'string'},
        'description':{'type':'string'},
        'data_dictionary':{'type':'array','items':healjsonschema}
    }
}

def validate_json(data_dictionary,raise_valid_error=False,schema=schema):
    """
    Validates the `data_dictionary` fields property against the specified JSON schema.

    Parameters
    ----------
    data_dictionary : list[dict]
        The list of fields to validate.
    raise_valid_error : bool, optional
        If `True`, raises an exception if the validation fails.
        Default is `False`.
    schema : dict, optional
        The JSON schema to be validated against.
        Default is `schema`.

    Returns
    -------
    tuple
        A tuple containing the validated `data_dictionary` and the JSON schema
        validation error report in the form of a dictionary.

    Raises
    ------
    Exception
        If `raise_valid_error` is `True` and the validation fails.

    Notes
    -----
    This function uses the `jsonschema` package for validation.
    """
    try:
        print(f'Validating heal-specified json fields.....')
        jsonschema.validate(data_dictionary,schema=schema)
        report = {"valid":True}
        print(f"JSON array of data dictionary fields is VALID")
    except jsonschema.exceptions.ValidationError as e:
        report = e.__dict__
        report['valid'] = False
        if raise_valid_error:
            raise Exception(f"Data dictionary not valid: {e.message}")
            
        
    return data_dictionary,report


def validate_csv(data_or_path,schema=healfrictionless):
    """
    Validates tabular data by ordering columns according to a schema
    with frictionless Table Schema standards profile and adds missing
    columns before validating.

    Parameters
    ----------
    data_dict_or_path : str or Path or anything excepted by frictionless Resource data
        data parameter (eg array of fields in the correct specification for csv)
        Path to data with the data being a tabular HEAL-specified data dictionary
    schema : dict, optional
        The schema to compare data_or_path to (default: HEAL frictionless template)

    Returns
    -------
    List[dict]
        Tabular data in the form of an array of dictionaries for each field (ie keyed) and the validation report
    Report
        frictionless report object
    Notes
    -----
    Currently, in contrast to the `validate_json` function, this validates only
    at the field level.
    """
    schema = Schema(schema)
    if isinstance(data_or_path,(str,Path)):
        data_tbl = (
            pd.read_csv(data_or_path,dtypes="string")
            .fillna("")
            .to_dict(orient="records")
        )
    elif isinstance(data_or_path, list):
        if all(isinstance(item, dict) for item in data_or_path):
            #NOTE: need to add missing field-wise values. 
            # could also use potential dialect object. Might be worth looking
            # into if switching to fricitonless v5
            data_tbl = [
                {name:field.get(name,"") 
                for name in schema.field_names} 
                for field in data_or_path
            ]
   
    print("Validating csv data dictionary...")
    source = Resource(data=data_tbl,schema=schema)
    source.format = "inline"
    source.scheme = "buffer"
    report = source.validate()
    if report['valid']:
        print("Csv is VALID")
    else:
        print("Csv is invalid. Check the report")
    
    return data_tbl,report
