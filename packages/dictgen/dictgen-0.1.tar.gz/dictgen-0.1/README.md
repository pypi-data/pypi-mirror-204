# dictgen
Generate random Python dictionaries for testing.

``` python
import dictgen
dictgen.generate()

### Outputs
{
    "": [
        280633528141071517,
        [
            -4279251701116042058
        ]
    ],
    "X": 957269515550119532
}
```

Control the number of keys allowed at a single level in the library
using `max_height`.

``` python
import dictgen
dictgen.generate(max_height=2)

### Outputs
{
    "PZ70": "BD3X3",
    "M6": {}
}

dictgen.generate(max_height=5)

### Outputs
{
    "PZ70": "BD3X3",
    "M6": {},
    123 : None,
    "B1223S3S": [9243, None],
    "XLXSM35PW3": "1AHLFB06"
}
```

Control the maximum number of nested dictionaries and arrays using `max_depth`.

``` python
print( dictgen.generate(max_depth=3) )

### Outputs
{
    "POARS2": 2.6720361072638525e+18,
    "6": {
        "BZVADP": -1.646104091641211e+18,
        "V": []
    }
}
```

You can reproduce the same dictionary consistently using the `seed`
parameter.
``` python
dictgen.generate(rand_seed=1)

### Outputs
{'4YNG5BY': -7.048155888731118e+18}

dictgen.generate(rand_seed=1)

### Outputs
{'4YNG5BY': -7.048155888731118e+18}
```

You can control the different functions that are used to generate your dictionaries.

`key_generators`, `val_generators`, `nested_generators` arguments

``` python
# Generate a dictionary with only strings as keys and values
dictgen.generate(key_generators=(dictgen.random_string,), val_generators=(dictgen.random_string,))

### Outputs
{'QM':
    {
        '57S': 'MBBO6XZP',
        '': '5WWU8AY'
    },
    '': [{'M0ISLL4': '8'}, 'XE0'],
    'EHEOL1I5': {}
}

# Generate a dictionary with a custom generator method
from uuid import uuid4

def generate_uuid(**kwargs):
    return uuid4()

dictgen.generate(key_generators=(generate_uuid,), val_generators=(dictgen.random_string,))

### Outputs
{UUID('2f85cf3e-b8f4-4750-ac3d-8ce84b9f7ed1'): [[]], UUID('a840fd05-daba-49ce-a695-fad8c1fd3675'): 'EeuM0N', UUID('6dab8e6d-35f1-479e-8763-b671b46a86b0'): 'aj'}
```

# Examples
[./examples/fuzz_tomlkit.py](fuzz_tomlkit.py) - an example of fuzz testing a popular toml encoder library

```
...

Test 5 -------------
test_data: {'HX': [[]], 'YiG': datetime.time(15, 55)}
result:
HX = [[]]
YiG = 15:55:00
```

# CONTRIBUTING
Make sure all unit tests are passing

```
pip install -e .
python -m unittest
```
