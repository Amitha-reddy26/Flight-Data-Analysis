import csv
import io
from src.flight_analysis import FlightAnalysis

def test_mapper():
    row = ["0"] * 20
    row[1] = "2013"
    row[4] = "900"
    row[6] = "10"
    row[10] = "AA"

    buffer = io.StringIO()
    csv.writer(buffer).writerow(row)

    result = dict(FlightAnalysis().mapper(
        None, buffer.getvalue().strip()
    ))

    assert result[("AA", "total_flights")] == 1
    assert result[("AA", "departure_delay")] == 10
    assert result[("AA", "on_time")] == 1

def test_reducer():
    result = list(FlightAnalysis().reducer(
        ("AA", "total_flights"), [1, 1, 1]
    ))
    assert result[0][1] == 3
