from reports.reports import AveragePerformance


def test_average_rating_report():
    data = [
        {"position": "Backend Developer", "performance": 4.8},
        {"position": "Backend Developer", "performance": 4.83},
        {"position": "Mobile Developer", "performance": 4.62},
        {"position": "DevOps Engineer", "performance": 4.7},
    ]
    report = AveragePerformance()
    result = report.value(data)
    backend = next(r for r in result if r["position"] == "Backend Developer")
    mobile = next(r for r in result if r["position"] == "Mobile Developer")


    assert backend["performance"] == 4.80
    assert mobile["performance"] == 4.60