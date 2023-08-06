# kibana-ql

## Install

```shell
pip install kibana-ql
```

## Use

```python
from kibana_ql import KqlParser

p = KqlParser()
p.parse("field: value")
```

## Tests

```shell
py -m unittest discover -v -s tests -p "*_test.py"
```
