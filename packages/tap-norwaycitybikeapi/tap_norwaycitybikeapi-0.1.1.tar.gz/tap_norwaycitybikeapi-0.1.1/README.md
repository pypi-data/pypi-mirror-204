<p align="center">
  <img src="assets/bysykkel_logo.png" width="150" title="logo">
</p>

# tap-norwaycitybikeapi

`tap-norwaycitybikeapi` is a Singer tap for the [Trondheim](https://trondheimbysykkel.no/en/open-data/realtime), [Oslo](https://oslobysykkel.no/en/open-data/realtime) and [Bergen](https://bergenbysykkel.no/en/open-data/realtime) City Bike APIs.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

> **Note**
> The City Bike APIs are published under the [Norwegian Licence for Open Government Data (NLOD) 2.0](https://data.norge.no/nlod/en/2.0).


## Capabilities

* `catalog`
* `state`
* `discover`
* `about`
* `stream-maps`
* `schema-flattening`

## Installation

Install from PyPi:

```bash
pipx install tap-norwaycitybikeapi
```

Install from GitHub:

```bash
pipx install git+https://github.com/andrejakobsen/tap-norwaycitybikeapi.git@main
```

## Configuration
There are two important configurations that need to be set to use this extractor: `client_identifier` and `city_name`
This can be done with the commands
```bash
meltano config tap-norwaycitybikeapi set client_identifier [value]
```
and
```bash
meltano config tap-norwaycitybikeapi set city_name [value]
```
### Accepted Config Options

| Setting             | Required | Default | Description |
|:--------------------|:--------:|:-------:|:------------|
| client_identifier   | True     | None    | The value should contain your company/organization name, follwed by a dash and the application's name. |
| city_name           | True     | oslo    | Name of Norwegian city having City Bikes. Currently only available for Trondheim, Oslo and Bergen. |
| stream_maps         | False    | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |
| stream_map_config   | False    | None    | User-defined config values to be used within map expressions. |
| flattening_enabled  | False    | None    | 'True' to enable schema flattening and automatically expand nested properties. |
| flattening_max_depth| False    | None    | The max depth to flatten schemas. |

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-norwaycitybikeapi --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

## Usage

You can easily run `tap-norwaycitybikeapi` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-norwaycitybikeapi --version
tap-norwaycitybikeapi --help
tap-norwaycitybikeapi --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-norwaycitybikeapi` CLI interface directly using `poetry run`:

```bash
poetry run tap-norwaycitybikeapi --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-norwaycitybikeapi
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-norwaycitybikeapi --version
# OR run a test `elt` pipeline:
meltano elt tap-norwaycitybikeapi target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
