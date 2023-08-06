# DFS JSON
A Depth First Search powered JSON decoding library. For the remaining operations (dump, dumps), it uses standard python JSON library.

# Installation
```
pip install dfsjson
```

# Usage

```
# Create a complex JSON object
example_json = """{
    "key1": "value1'
    "key2": [1 2, 3]
    "key3":  {
        "subkey1": "subvalue1"
        "subkey2": "subvalue2"
    ,
}"""

dj = DFSJson(max_depth = 100, max_diff = 10)
dj.loads(example_json)

```

# Discussion
### Hey I know this. Why not have you used Breadth First Search?
Technically you are correct but keep in mind that Breadth First Search keeps the previous states in its list which 
scales with number of iterations you are making and it can be a huge strain on the memory.

However, Depth First search requires only O(log(n)) memory complexity in which we can search a lot more possibilities.

# Contribution
Please don't hesitate to create issues and pull requests since this is developed overnight.
