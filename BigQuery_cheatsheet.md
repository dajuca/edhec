## Google Big Query
#### Cli help

```bash
bq help                                 # list all sub commands
bq ls --help                            # help for `ls` sub command
```
#### Datasets

DATASET=app_dataset
PROJECT=project-id
LOCATION=EU

# create dataset, `--sync` waits for the job to complete
bq mk \
    --sync \
    --project_id $PROJECT \
    --data_location $LOCATION \
    $DATASET

bq ls                                   # list datasets

bq ls $DATASET                          # list dataset tables

bq rm -r -f $DATASET      

#### Tables

DATASET=app_dataset
TABLE=data_table
REGION=europe-west1

# create dataset table
bq mk \
    --sync \
    --location=$REGION \
    $DATASET.$TABLE

bq show $DATASET.$TABLE                 # show table format

bq rm -f $DATASET.$TABLE                # remove dataset table

#### Queries

DATASET=app_dataset
TABLE=data_table

# show table first rows
bq query "SELECT * FROM $DATASET.$TABLE LIMIT 5"

# show table usage
bq query \
    --nouse_legacy_sql \
    "SELECT * FROM $DATASET.INFORMATION_SCHEMA.PARTITIONS"


#### Data import

DATASET=app_dataset
PROJECT=project-id
TABLE=data_table
SOURCE=data.csv

FORMAT=CSV
ENCODING=UTF-8
HEAD_COUNT=1
FIELD_DELIMITER=""
QUOTE="\""
MAX_ERROR=0


# load data into dataset table
bq load --autodetect $DATASET.$TABLE $SOURCE

# load data into dataset table with schema
bq load \
    --autodetect \
    --schema "key:timestamp,fare_amount:float,pickup_datetime:timestamp,pickup_longitude:float,pickup_latitude:float,dropoff_longitude:float,dropoff_latitude:float,passenger_count:integer" \
    --source_format $FORMAT \
    --encoding $ENCODING \
    --skip_leading_rows $HEAD_COUNT \
    --allow_jagged_rows \
    --allow_quoted_newlines \
    --ignore_unknown_values \
    --field_delimiter $FIELD_DELIMITER \
    --quote $QUOTE \
    --max_bad_records $MAX_ERROR \
    --project_id $PROJECT \
    $DATASET.$TABLE \
    $SOURCE
