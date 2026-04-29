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
    metadata['duplicated_values'] = int(df.duplicated().sum())
    
    df.drop_duplicates(inplace=True)
    
    split_data = df['service_description'].str.split(' ', n=1, expand=True)

    df['service_type'] = split_data[0]
    if split_data.shape[1] > 1:
        df['service_detail'] = split_data[1]
    else:
        df['service_detail'] = "unknown"

    is_identical = (df['maintenance_type'] == df['service_type']).all()
    print('Is maintenance_type identical to service_type?', is_identical)

    # get cols
    categorical_cols = ['maintenance_type', 'service_type', 'service_detail', 'facility_location']
    
    numerical_cols = [
        'odometer_reading', 'labor_hours', 'labor_cost', 'parts_cost',
        'total_cost', 'downtime_hours', 'days_since_last'
    ]

    for col in categorical_cols:
        if col not in df.columns:
            df[col] = "Unknown"
    for col in numerical_cols:
        if col not in df.columns:
            df[col] = 0.0

    if 'service_description' in df.columns:
        df.drop('service_description', axis=1, inplace=True)
    
    return df[categorical_cols + numerical_cols], metadata

