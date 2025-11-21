import os

import pytest

from main import get_data, get_valid_files, print_result, validate_report
from reports import REPORTS


def test_get_valid_files(tmp_path):
    # Создаем временный файл
    file1 = tmp_path / "file1.csv"
    file1.write_text("name,position,completed_tasks,skills,team,experience_years\n")
    valid_files = get_valid_files([str(file1)])
    assert len(valid_files) == 1
    assert os.path.basename(valid_files[0]) == "file1.csv"

def test_get_valid_files_missing(tmp_path):
    with pytest.raises(SystemExit):
        get_valid_files([str(tmp_path / "missing.csv")])


def test_validate_report_exists():
    report_name = list(REPORTS.keys())[0]
    assert validate_report(report_name) == report_name

def test_validate_report_missing():
    with pytest.raises(SystemExit):
        validate_report("bad-report")


def test_get_data(tmp_path):
    file = tmp_path / "test.csv"
    file.write_text(
        "name,position,completed_tasks,performance,skills,team,"
        "experience_years\nDavid Chen,Mobile Developer,36,4.6,"
        "Swift,React Native,Mobile Team,3\n")
    data = get_data([str(file)])
    assert len(data) == 1
    assert data[0]["position"] == "Mobile Developer"
    assert data[0]["performance"] == "4.6"


def test_print_result(capsys):
    result = [
        {"position": "Backend Developer", "performance": 4.83},
        {"position": "Mobile Developer", "performance": 4.62},
    ]
    print_result(result)
    captured = capsys.readouterr()
    assert "Backend Developer" in captured.out
    assert "Mobile Developer" in captured.out
