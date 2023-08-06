# Tggl Python Client

## Install
Intall the package using the package manager of your choice:
```
pip install tggl
```

## Quick Start
```python
from tggl import TgglClient

client = TgglClient('<Your API key>')

flags = client.eval_context({
    'user_id': 123,
    'email': 'foo@gmail.com',
    'plan': 'PRO'
})

# On/Off flags
if (flags.is_active('feature_1')):
    print('Feature 1 is active')

# A/B tests
if (flags.get('feature_2') == 'Variation A'):
    print('Should display variation A to user')

# A/B test with default value
if (flags.get('feature_2', 'Variation A') == 'Variation B'):
    print('Should display variation B to user')
```