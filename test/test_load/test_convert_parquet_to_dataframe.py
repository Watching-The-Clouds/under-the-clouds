from load_utils import convert_parquet_to_dataframe
from io import BytesIO
import pandas as pd
import pytest

def test_convert_parquet_to_dataframe():

    expected_df = pd.DataFrame({
        "column1": [1, 2, 3],
        "column2": ["A", "B", "C"]
    })

    parquet_buffer = BytesIO()
    expected_df.to_parquet(parquet_buffer, index=False)
    parquet_buffer.seek(0)

    result_df = convert_parquet_to_dataframe(parquet_buffer)

    assert isinstance(result_df, pd.DataFrame)
    pd.testing.assert_frame_equal(result_df, expected_df)