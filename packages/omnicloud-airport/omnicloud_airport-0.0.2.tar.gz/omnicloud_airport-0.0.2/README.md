
# Omnicloud.Airport


Omnicloud.Airport is a Python package for handling data transfer to and from cloud storage providers. It provides a set of classes that implement a common interface for working with cloud storage, making it easy to switch between providers and abstract classes for extending self.

<br/>


## Conception

### Terminal

It is an object that provides cloud related features to existing objects. For example:

- omnicloud.airport.terminals.Dict contains methods for processing dictionary;
- omnicloud.airport.terminals.Pickle - for handling a pickle object.

Every terminal is inherited fom his based object: Dict from dict, Pickle from pickle, so
you can use it in your code directly.

Each terminals contains one or more Gates.


### Gate

Gate is a object that interacts with single cloud.

- omnicloud.airport.terminals.Dict.GStorageJSON - with JSON files at the Google Cloud
Storage bucket;
- omnicloud.airport.terminals.Dict.LocalJSON - with local file.


### Addons

The omnicloud.airport is a platform additional terminals or gates can be installed
into that.

For more information please read [the developer docs](https://docs.omnicloud.world/projects/py-airport/development).


> ## Filling with objects
>
> The base package omnicloud.airport contains terminals for object from a pretty python only and gates for local files to theme.
>
> If you need more please install additional packages. For example omnicloud-airport-dict-gcs
> to get a gate to Google Cloud Storage for dictionary or omnicloud-airport-pydantic to get a
> terminal for pydantic.


## Installation & usage

```bash linenums="1"
pip3 install --upgrade omnicloud-airport
```

```py linenum=1
from omnicloud.airport.terminals import Dict

test_dict = {}
Dict(test_dict).departure('LocalJSON::/tmp::ensure_ascii=False', 'file_name.json')
```

The first argument of the method departure is a "waybill". The second is a filename.

The waybill is a specification for processing data in string format that contains three elements
separated by "::":

1) name of class that represented needs gate;

2) the place for saving to;

3) additional options in format "key=value||key=value||key=b64:..."; it is optional argument.


As a waybill well as filename can contains a part of path:

```py
Dict(test_dict).departure('LocalJSON::/tmp/a::ensure_ascii=False', 'file.json')
Dict(test_dict).departure('LocalJSON::/tmp::ensure_ascii=False', 'a/file.json')
```

Both command in the tutorial above save a data to file "/tmp/a/file.json"

For interaction with different storage (cloud provider) you have to change waybill in your config
or environment variable:

```bash
pip3 install omnicloud-airport-gcp
```

then

```py
Dict(test_dict).departure('GStorageJSON::gs://bucket::ensure_ascii=False||key_file=...', 'a/file.json')
```
