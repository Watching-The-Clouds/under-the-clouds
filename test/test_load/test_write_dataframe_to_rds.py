# from unittest.mock import patch, MagicMock
# import pandas as pd
# from sqlalchemy.engine import Engine
# from load_utils import write_dataframe_to_rds

# def test_write_dataframe_to_rds():
#     mock_df = pd.DataFrame({
#         "id": [1, 2, 3],
#         "name": ["Alice", "Bob", "Charlie"],
#         "value": [100, 200, 300]
#     })

#     mock_db_config = {
#         "user": "test_user",
#         "password": "test_password",
#         "host": "localhost",
#         "port": 5432,
#         "dbname": "test_db"
#     }

#     table_name = "test_table"

#     with patch("load_utils.create_engine") as mock_create_engine, \
#          patch.object(mock_df, "to_sql") as mock_to_sql:

#         mock_engine = MagicMock(spec=Engine)
#         mock_create_engine.return_value = mock_engine

#         write_dataframe_to_rds(mock_df, table_name, mock_db_config)

#         expected_db_url = (
#             f"postgresql+psycopg2://{mock_db_config['user']}:{mock_db_config['password']}"
#             f"@{mock_db_config['host']}:{mock_db_config['port']}/{mock_db_config['dbname']}"
#         )
#         mock_create_engine.assert_called_once_with(expected_db_url)

#         mock_to_sql.assert_called_once_with(table_name, mock_engine, if_exists="append", index=False)

from unittest.mock import patch, MagicMock
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from load_utils import write_dataframe_to_rds

def test_write_dataframe_to_rds():
    # Create a mock DataFrame
    mock_df = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "value": [100, 200, 300]
    })

    # Mock database configuration
    mock_db_config = {
        "user": "test_user",
        "password": "test_password",
        "host": "localhost",
        "port": 5432,
        "dbname": "test_db"
    }

    table_name = "test_table"

    # Mock the database engine creation
    with patch("load_utils.create_engine") as mock_create_engine:
        # Use a real in-memory SQLite engine for testing
        real_engine = create_engine("sqlite:///:memory:")
        mock_create_engine.return_value = real_engine

        # Call the function being tested
        write_dataframe_to_rds(mock_df, table_name, mock_db_config)

        # Verify that the engine was created with the expected URL
        expected_db_url = (
            f"postgresql+psycopg2://{mock_db_config['user']}:{mock_db_config['password']}"
            f"@{mock_db_config['host']}:{mock_db_config['port']}/{mock_db_config['dbname']}"
        )
        mock_create_engine.assert_called_once_with(expected_db_url)

        # Verify that the data was written to the table
        with real_engine.connect() as conn:
            result = conn.execute(f"SELECT * FROM {table_name}").fetchall()
            expected_result = [
                (1, "Alice", 100),
                (2, "Bob", 200),
                (3, "Charlie", 300)
            ]
            assert result == expected_result
