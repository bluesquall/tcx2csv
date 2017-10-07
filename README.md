tcx2csv
=======

For the athlete who wants to plot and analyze data from their activities
outside Garmin Connect, Strava, etc., the Training Center XML format (`tcx`)
does not offer much that cannot be found in a well-formed `csv` file. Since
almost any analysis tool can read a `csv` without a special library or
extension, it makes more sense to me to convert the data, then use a built-in
`csv` reader, rather than writing a `tcx` importer or parser for each tool.

Plus, this is a well-defined task, so it could be a good exercise when I feel
like implementing it in different languages to learn them better.

Input format
------------

The Training Center XML format (`tcx`) [schema][TCX] is defined by Garmin.
Most `tcx` files have one activity -- either biking or running -- with one or
more laps comprised of tracks defined by trackpoints.

Output format
-------------

```csv
timestamp,longitude,latitude,altitude,lap,distance,speed,cadence,heartrate,power |

```

Note that `tcx2csv` will put `RunCadence` into the `cadence` column for runs,
and use the top-level `Cadence` for biking.


As a table, this would look like:

| timestamp | longitude | latitude | altitude | lap | distance | speed | cadence | heart rate | power |
|-----------|-----------|----------|----------|-----|----------|-------|---------|------------|-------|
|           |           |          |          |     |          |       |         |            |       |
|           |           |          |          |     |          |       |         |            |       |

Once you have the output `csv` you should be able to import it easily into
whatever tool you prefer, e.g.:

```python
import numpy as np
data = np.loadtxt('output.csv', delimiter=',', skiprows=1)
```


-------------
[TCX]: https://wikipedia.org/wiki/Training_Center_XML
[AEv2]: http://www8.garmin.com/xmlschemas/ActivityExtensionv2.xsd
[sample TCX]: https://developer.garmin.com/downloads/connect-api/sample_file.tcx
