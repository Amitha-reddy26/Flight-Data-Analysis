import csv
from mrjob.job import MRJob

class FlightAnalysis(MRJob):

    def mapper(self, _, line):
        row = next(csv.reader([line]))

        if len(row) < 20 or row[1] == "year":
            return

        carrier = row[10]
        delay = row[6]

        yield (carrier, "total_flights"), 1

        if row[4] in ("NA", ""):
            yield (carrier, "missing_departure"), 1

        if delay not in ("NA", ""):
            yield (carrier, "departure_delay"), float(delay)
            yield (carrier, "recorded_departures"), 1
            yield (carrier, "on_time"), int(float(delay) < 15)

    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == "__main__":
    FlightAnalysis.run()
