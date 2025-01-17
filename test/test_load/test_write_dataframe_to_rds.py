import pandas as pd
from unittest.mock import patch, MagicMock
from sqlalchemy.engine.base import Engine
from load_utils import write_dataframe_to_rds

def test_write_dataframe_to_rds():

    data = {"col1": [1, 2, 3], "col2": ["A", "B", "C"]}
    df = pd.DataFrame(data)
    
    db_config = {
        "host": "test-host",
        "port": "5432",
        "user": "test-user",
        "password": "test-password",
        "dbname": "test-db"
    }
    table_name = "test_table"
    
    with patch("load_utils.create_engine") as mock_create_engine, \
         patch.object(pd.DataFrame, "to_sql") as mock_to_sql:
        
        mock_engine = MagicMock(spec=Engine)
        mock_connection = mock_engine.connect.return_value.__enter__.return_value
        mock_create_engine.return_value = mock_engine
        
        mock_result = MagicMock()
        mock_result.scalar.return_value = 1
        mock_connection.execute.return_value = mock_result
        
        write_dataframe_to_rds(df, table_name, db_config)
        
        host = db_config['host'].split(':')[0] if ':' in db_config['host'] else db_config['host']
        db_url = f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{host}:{db_config['port']}/{db_config['dbname']}"
        
        mock_create_engine.assert_called_once_with(db_url)
        mock_connection.execute.assert_called_once_with(f"SELECT COUNT(*) FROM {table_name}")
        mock_to_sql.assert_called_once_with(table_name, mock_engine, if_exists="append", index=False)



