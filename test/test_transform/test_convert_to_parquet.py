import io
import pandas as pd
import pytest
from transform_utils import convert_to_parquet

def test_convert_to_parquet():

    sample_data = {
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "score": [95.0, 85.5, 77.0]
    }

    sample_df = pd.DataFrame(sample_data)

    result = convert_to_parquet(sample_df)

    assert isinstance(result, bytes)
    assert len(result) > 0

    parquet_buffer = io.BytesIO(result)
    reloaded_df = pd.read_parquet(parquet_buffer)

    pd.testing.assert_frame_equal(sample_df, reloaded_df)
