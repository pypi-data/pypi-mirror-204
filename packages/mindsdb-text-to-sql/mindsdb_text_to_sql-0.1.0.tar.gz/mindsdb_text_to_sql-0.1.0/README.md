# MindsDB Text to SQL

MindsDB Text to SQL is a Python package that allows you to convert natural language queries into SQL code that can be run on MindsDB. With this package, you can easily build models using MindsDB's in-database machine learning capabilities by simply describing what you want to predict in natural language.

This package uses the OpenAI API to convert natural language queries into SQL code that can be run on MindsDB.

## Installation
### With pip
```
pip install mindsdb_text_to_sql
```

## Usage
The library will first need to be configured with an API key from OpenAI.
```
from mindsdb_text_to_sql import GPTTextToSQL

text_to_sql = GPTTextToSQL('sk-...')
query = text_to_sql.convert_text_to_sql(
    "Get all rows from the iris table of the sqlite_datasource where the sepal_length is greater than 5"
)
```