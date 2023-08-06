# RUDI Node tools: _rudi-node-read_ library

This library offers tools to take advantage of
the [external API](https://app.swaggerhub.com/apis/OlivierMartineau/RUDI-PRODUCER) of a RUDI Producer node (also
referred as RUDI node).

The Jupyter notebook [README.ipynb](https://github.com/OlivierMartineau/rudi-node-read/blob/release/README.ipynb) offers
an overview of the available functionalities.

## Installation

```bash
$ pip install rudi_node_read
```

## Usage

```python
from rudi_node_read.rudi_node_reader import RudiNodeReader

node_reader = RudiNodeReader('https://bacasable.fenix.rudi-univ-rennes1.fr')
print(node_reader.metadata_count)
print(len(node_reader.metadata_list))
print(node_reader.organization_names)
print(node_reader.find_metadata_with_media_name('toucan.jpg'))

```
## Testing

```bash
pip install pytest-cov

python3 -m pytest --cov=rudi_node_read --cov-report term-missing --cov-report html
```

