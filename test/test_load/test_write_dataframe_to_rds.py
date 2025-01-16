from unittest.mock import patch, MagicMock
import pandas as pd
from sqlalchemy.engine import Engine
from load_utils import write_dataframe_to_rds

def test_write_dataframe_to_rds():
    mock_df = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "value": [100, 200, 300]
    })

    mock_db_config = {
        "user": "test_user",
        "password": "test_password",
        "host": "localhost",
        "port": 5432,
        "dbname": "test_db"
    }

    table_name = "test_table"

    with patch("load_utils.create_engine") as mock_create_engine, \
         patch.object(mock_df, "to_sql") as mock_to_sql:

        mock_engine = MagicMock(spec=Engine)
        mock_create_engine.return_value = mock_engine

        write_dataframe_to_rds(mock_df, table_name, mock_db_config)

        expected_db_url = (
            f"postgresql+psycopg2://{mock_db_config['user']}:{mock_db_config['password']}"
            f"@{mock_db_config['host']}:{mock_db_config['port']}/{mock_db_config['dbname']}"
        )
        mock_create_engine.assert_called_once_with(expected_db_url)

        mock_to_sql.assert_called_once_with(table_name, mock_engine, if_exists="append", index=False)
