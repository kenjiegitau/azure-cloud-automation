import pytest
from blob_storage import upload_report

def test_upload_report_not_found(tmp_path):
    # construct a path to a JSON file that doesn't exist inside the temporary directory
    nonexistent_file = tmp_path / "nonexistent_report.json"
    
    # confirm the file does not exist (optional, but good for clarity)
    assert not nonexistent_file.is_file()
    
    # use pytest.raises to assert that calling upload_report raises FileNotFoundError
    with pytest.raises(FileNotFoundError):
        upload_report(nonexistent_file)
