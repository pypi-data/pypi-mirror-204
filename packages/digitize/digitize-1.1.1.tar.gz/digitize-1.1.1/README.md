#### digitize - open source available library for determining the bit depth of a number with the output of its name

```python
from digitize import Exact

var = Exact

print(var.discharge(5000)) # Output: 5,000
print(var.discharge(51030.4853)) # Output: 51,030.48
print(var.discharge(51030.4853, True, "en/ru")) # Output: 51,030.48 thousand