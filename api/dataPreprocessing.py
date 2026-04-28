import pandas as pd


def clean_record(record):
    metadata = {}

    if hasattr(record, "model_dump"):
        # Pydantic v2 model
        record = record.model_dump()
    elif not isinstance(record, dict):
        raise TypeError("record must be a dict or Pydantic model")

    df = pd.DataFrame([record])
    
    #stores missing values and duplicated values so it could be displayed in the frontend
    metadata['missing_values'] = int(df.isnull().sum().sum())
    
    # TODO: must acccess database, get all records with the same truck id, and check for duplicate
    #or just remove this functionality if it is too complex to implement
    metadata['duplicated_values'] = df.duplicated().sum() 
    
    df.drop_duplicates(inplace=True)
    
    # Split Service Desc
    df[['service_type', 'service_detail']] = df['service_description'].str.split(' ', expand=True)
    df.drop('service_description', axis=1, inplace=True)
    
    # check if maintenance_type is identical to service_type
    is_identical = df['maintenance_type'] == df['service_type']
    print('Is maintenance_type identical to service_type?', is_identical.all())
        
    if is_identical.all():
        drop_cols = ['service_type']
        df.drop(columns=drop_cols, inplace=True)
        
        
    
    # get cols
    categorical_cols = ['maintenance_type','service_type','facility_location']
    numerical_cols = [
    'odometer_reading', 'labor_hours', 'labor_cost', 'parts_cost',
    'total_cost', 'downtime_hours', 'days_since_last'
    ]
    
    return df[categorical_cols + numerical_cols], metadata

