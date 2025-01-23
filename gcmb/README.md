## SMARD Data

[SMARD](https://www.smard.de/en) is an open data effort of the German Bundesnetzagentur
which is in charge of the German energy network. It contains data about the production 
and consumption of energy.

The data is published freely for public use under the CC BY 4.0 license. More information
can be found [here](https://www.smard.de/en/datennutzung).

## Current Energy Production in Germany

The following is the production in the last available 15m period:

### Conventional vs Renewable Energy Sources

Right now <Topic topic="stefan/smard/DE/production/total-renewable/percent" unit="%" decimals="1"/> of energy is
produced from renewable sources in Germany.

<PieChart>
  <Slice topic="stefan/smard/DE/production/total-conventional/value" label="Total Conventional" />
  <Slice topic="stefan/smard/DE/production/total-renewable/value" label="Total Renewable" />
</PieChart>

### Individual Energy Sources

<PieChart>
  <Slice topic="stefan/smard/DE/production/biomass/value" label="Biomass" />
  <Slice topic="stefan/smard/DE/production/brown-coal/value" label="Brown Coal" />
  <Slice topic="stefan/smard/DE/production/hard-coal/value" label="Hard Coal" />
  <Slice topic="stefan/smard/DE/production/hydro/value" label="Hydro" />
  <Slice topic="stefan/smard/DE/production/misc-conventional/value" label="Misc Conventional" />
  <Slice topic="stefan/smard/DE/production/misc-renewable/value" label="Misc Renewable" />
  <Slice topic="stefan/smard/DE/production/natural-gas/value" label="Natural Gas" />
  <Slice topic="stefan/smard/DE/production/nuclear/value" label="Nuclear" />
  <Slice topic="stefan/smard/DE/production/photovoltaic/value" label="Photovoltaic" />
  <Slice topic="stefan/smard/DE/production/pumped-storage/value" label="Pumped Storage" />
  <Slice topic="stefan/smard/DE/production/wind-offshore/value" label="Wind Offshore" />
  <Slice topic="stefan/smard/DE/production/wind-onshore/value" label="Wind Onshore" />
</PieChart>

### Data

#### Renewable

* Biomass: <Topic topic="stefan/smard/DE/production/biomass/value" /> MWh
* Hydro: <Topic topic="stefan/smard/DE/production/hydro/value" /> MWh
* Misc Renewable: <Topic topic="stefan/smard/DE/production/misc-renewable/value" /> MWh
* Photovoltaic: <Topic topic="stefan/smard/DE/production/photovoltaic/value" /> MWh
* Pumped Storage: <Topic topic="stefan/smard/DE/production/pumped-storage/value" /> MWh
* Wind Offshore: <Topic topic="stefan/smard/DE/production/wind-offshore/value" /> MWh
* Wind Onshore: <Topic topic="stefan/smard/DE/production/wind-onshore/value" /> MWh

#### Conventional

* Brown Coal: <Topic topic="stefan/smard/DE/production/brown-coal/value" /> MWh
* Hard Coal: <Topic topic="stefan/smard/DE/production/hard-coal/value" /> MWh
* Misc Conventional: <Topic topic="stefan/smard/DE/production/misc-conventional/value" /> MWh
* Natural Gas: <Topic topic="stefan/smard/DE/production/natural-gas/value" /> MWh
* Nuclear: <Topic topic="stefan/smard/DE/production/nuclear/value" /> MWh

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
