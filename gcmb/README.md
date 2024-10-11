## SMARD Data

[SMARD](https://www.smard.de/en) is an open data effort of the German Bundesnetzagentur
which is in charge of the German energy network. It contains data about the production 
and consumption of energy.

The data is published freely for public use under the CC BY 4.0 license. More information
can be found [here](https://www.smard.de/en/datennutzung).

## Current Energy Production in Germany

The following is the production in the last available 15m period:

* Photovoltaic: <Topic topic="DE/production/photovoltaic/value" /> MWh
* Brown Coal: <Topic topic="DE/production/brown-coal/value" /> MWh
* Wind Offshore: <Topic topic="DE/production/wind-offshore/value" /> MWh

## Topic structure

The topics are published with the following structure:

### Scalar values per 15 minutes in MWh

`stefan/smard/{country}/{production|consumption}/{energy_type}/value`

Example:

`stefan/smard/DE/production/photovoltaic/value`

The value is an ASCII string of the last 15 minutes in MWh.

### JSON values per 15 minutes in MWh

`stefan/smard/{country}/{production|consumption}/{energy_type}/json`

Example:

`stefan/smard/DE/production/photovoltaic/json`

An example of the value is:

`{"value": 2552.0, "timestamp": "2024-10-11T23:00:00Z", "resolution": "15m", "unit": "MWh"}`
