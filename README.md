## SMARD Data Collector

This data collector retrieves SMARD data and publishes it to [gcmb.io](https://gcmb.io).

[SMARD](https://www.smard.de/en) is an open data effort of the German Bundesnetzagentur
which is in charge of the German energy network. It contains data about the production 
and consumption of energy.

The data is published freely for public use under the CC BY 4.0 license. More information
can be found [here](https://www.smard.de/en/datennutzung).

## Implementation

The data collector is implemented in Python. It uses Poetry as a build system.

Information about the used API can be found [here on GitHub](https://github.com/bundesAPI/smard-api)

## Usage

Clone this repository and fetch the dependencies using:

```bash
poetry update
```

Then configure it by copying the `.env.template` to `.env` and configuring the values.

You can then start the collector with:

```bash
poetry run python main.py
```
