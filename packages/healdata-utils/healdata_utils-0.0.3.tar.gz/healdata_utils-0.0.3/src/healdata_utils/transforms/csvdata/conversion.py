""" 
 
CSV data to HEAL VLMD conversion


""" 
from healdata_utils.io import read_table 
from healdata_utils.transforms.jsontemplate.conversion import convert_templatejson
import pandas as pd

def convert_datacsv(file_path,data_dictionary_props={}):
    """ 
    Takes a CSV file containing data (not metadata) and 
    infers each of it's variables data types and names.
    These inferred properties are then outputted as partially-completed HEAL variable level metadata
    files. That is, it outputs the `name` and `type` property. 

    NOTE: this will be an invalid file as `description` is required
    for each variable. However, this serves as a great way to start
    the basis of a VLMD submission.
    """  
    #TODO: support possible values; use visions package 
    df = read_table(file_path,castdtype=None)#TODO: use visions package for inference (from pandas profile project)
    fields = pd.io.json.build_table_schema(df,index=False)['fields'] #converts to frictionless Table Schema

    for field in fields:
        field.pop('extDtype',None)
        fieldname = field['name']

    data_dictionary = data_dictionary_props.copy()
    data_dictionary['data_dictionary'] = fields 

    package = convert_templatejson(data_dictionary)
    return package
