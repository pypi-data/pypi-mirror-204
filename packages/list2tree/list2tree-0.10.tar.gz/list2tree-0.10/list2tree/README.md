# Converts a list of tuples to a nested "family tree dict"  

## pip install list2tree


#### Tested against Windows 10 / Python 3.10 / Anaconda


```python
from list2tree import treedict,edit_value_in_treedict,get_value_in_treedict
import pprint as pa
pprintx=pa.PrettyPrinter(indent=1,width=1,compact=True)
pprint=pprintx.pprint
nameconnections = [
    ("Maria", "Anna"),
    ("Anna", "Joao"),
    ("Kasimir", "Maria"),
    ("Hans", "Fritz"),
    ("Fritz", "Anna"),
    ("Günther", "Wolfgang"),
    ("Joao", "Wolfgang"),
]
print("0) --------------------------------------------------------------")
mapped, airvar = treedict(
    pairs_list=nameconnections, main_mapping_keys=(), bi_rl_lr="lr"
)
pprint(mapped)
pprint(airvar)
print("1) --------------------------------------------------------------")
mapped, airvar = treedict(
    pairs_list=nameconnections, main_mapping_keys=(), bi_rl_lr="rl"
)
pprint(mapped)
pprint(airvar)
print("2) --------------------------------------------------------------")
mapped, airvar = treedict(
    pairs_list=nameconnections, main_mapping_keys=(), bi_rl_lr="bi"
)
pprint(mapped)
pprint(airvar)
print("3) --------------------------------------------------------------")
mapped, airvar = treedict(
    pairs_list=nameconnections, main_mapping_keys=("Anna", "Günther"), bi_rl_lr="lr"
)
pprint(mapped)
pprint(airvar)
print("4) --------------------------------------------------------------")
mapped, airvar = treedict(
    pairs_list=nameconnections, main_mapping_keys=("Anna", "Wolfgang"), bi_rl_lr="rl"
)
pprint(mapped)
pprint(airvar)
print("5) --------------------------------------------------------------")
mapped, airvar = treedict(
    pairs_list=nameconnections, main_mapping_keys=("Anna",), bi_rl_lr="bi"
)
pprint(mapped)
pprint(airvar)
print("6) --------------------------------------------------------------")
v1 = get_value_in_treedict(airvar, ("Anna", "Joao", "Wolfgang", "Günther"))
print(v1)
edit_value_in_treedict(
    airvar, ("Anna", "Joao", "Wolfgang", "Günther"), "new_value_edit"
)
pprint(airvar)
v2 = get_value_in_treedict(airvar, ("Anna", "Joao", "Wolfgang", "Günther"))
print(v2)
print("7) --------------------------------------------------------------")
0) --------------------------------------------------------------
[(1,
  ('Wolfgang',)),
 (2,
  ('Günther',
   'Wolfgang')),
 (3,
  ('Joao',
   'Wolfgang')),
 (4,
  ('Anna',
   'Joao',
   'Wolfgang')),
 (5,
  ('Fritz',
   'Anna',
   'Joao',
   'Wolfgang')),
 (6,
  ('Maria',
   'Anna',
   'Joao',
   'Wolfgang')),
 (7,
  ('Hans',
   'Fritz',
   'Anna',
   'Joao',
   'Wolfgang')),
 (8,
  ('Kasimir',
   'Maria',
   'Anna',
   'Joao',
   'Wolfgang'))]
{'Anna': {'Joao': {'Wolfgang': 4}},
 'Fritz': {'Anna': {'Joao': {'Wolfgang': 5}}},
 'Günther': {'Wolfgang': 2},
 'Hans': {'Fritz': {'Anna': {'Joao': {'Wolfgang': 7}}}},
 'Joao': {'Wolfgang': 3},
 'Kasimir': {'Maria': {'Anna': {'Joao': {'Wolfgang': 8}}}},
 'Maria': {'Anna': {'Joao': {'Wolfgang': 6}}},
 'Wolfgang': 1}
1) --------------------------------------------------------------
[(1,
  ('Günther',)),
 (2,
  ('Hans',)),
 (3,
  ('Kasimir',)),
 (4,
  ('Fritz',
   'Hans')),
 (5,
  ('Maria',
   'Kasimir')),
 (6,
  ('Wolfgang',
   'Günther')),
 (7,
  ('Wolfgang',
   'Joao',
   'Anna',
   'Maria',
   'Kasimir')),
 (8,
  ('Wolfgang',
   'Joao',
   'Anna',
   'Fritz',
   'Hans')),
 (9,
  ('Anna',
   'Maria',
   'Kasimir')),
 (10,
  ('Anna',
   'Fritz',
   'Hans')),
 (11,
  ('Joao',
   'Anna',
   'Maria',
   'Kasimir')),
 (12,
  ('Joao',
   'Anna',
   'Fritz',
   'Hans'))]
{'Anna': {'Fritz': {'Hans': 10},
          'Maria': {'Kasimir': 9}},
 'Fritz': {'Hans': 4},
 'Günther': 1,
 'Hans': 2,
 'Joao': {'Anna': {'Fritz': {'Hans': 12},
                   'Maria': {'Kasimir': 11}}},
 'Kasimir': 3,
 'Maria': {'Kasimir': 5},
 'Wolfgang': {'Günther': 6,
              'Joao': {'Anna': {'Fritz': {'Hans': 8},
                                'Maria': {'Kasimir': 7}}}}}
2) --------------------------------------------------------------
[(1,
  ('Anna',
   'Joao',
   'Wolfgang',
   'Günther')),
 (2,
  ('Anna',
   'Maria',
   'Kasimir')),
 (3,
  ('Anna',
   'Fritz',
   'Hans')),
 (4,
  ('Fritz',
   'Anna',
   'Joao',
   'Wolfgang',
   'Günther')),
 (5,
  ('Fritz',
   'Anna',
   'Maria',
   'Kasimir')),
 (6,
  ('Fritz',
   'Hans')),
 (7,
  ('Günther',
   'Wolfgang',
   'Joao',
   'Anna',
   'Maria',
   'Kasimir')),
 (8,
  ('Günther',
   'Wolfgang',
   'Joao',
   'Anna',
   'Fritz',
   'Hans')),
 (9,
  ('Hans',
   'Fritz',
   'Anna',
   'Joao',
   'Wolfgang',
   'Günther')),
 (10,
  ('Hans',
   'Fritz',
   'Anna',
   'Maria',
   'Kasimir')),
 (11,
  ('Joao',
   'Wolfgang',
   'Günther')),
 (12,
  ('Joao',
   'Anna',
   'Maria',
   'Kasimir')),
 (13,
  ('Joao',
   'Anna',
   'Fritz',
   'Hans')),
 (14,
  ('Kasimir',
   'Maria',
   'Anna',
   'Joao',
   'Wolfgang',
   'Günther')),
 (15,
  ('Kasimir',
   'Maria',
   'Anna',
   'Fritz',
   'Hans')),
 (16,
  ('Maria',
   'Anna',
   'Joao',
   'Wolfgang',
   'Günther')),
 (17,
  ('Maria',
   'Anna',
   'Fritz',
   'Hans')),
 (18,
  ('Maria',
   'Kasimir')),
 (19,
  ('Wolfgang',
   'Günther')),
 (20,
  ('Wolfgang',
   'Joao',
   'Anna',
   'Maria',
   'Kasimir')),
 (21,
  ('Wolfgang',
   'Joao',
   'Anna',
   'Fritz',
   'Hans'))]
{'Anna': {'Fritz': {'Hans': 3},
          'Joao': {'Wolfgang': {'Günther': 1}},
          'Maria': {'Kasimir': 2}},
 'Fritz': {'Anna': {'Joao': {'Wolfgang': {'Günther': 4}},
                    'Maria': {'Kasimir': 5}},
           'Hans': 6},
 'Günther': {'Wolfgang': {'Joao': {'Anna': {'Fritz': {'Hans': 8},
                                            'Maria': {'Kasimir': 7}}}}},
 'Hans': {'Fritz': {'Anna': {'Joao': {'Wolfgang': {'Günther': 9}},
                             'Maria': {'Kasimir': 10}}}},
 'Joao': {'Anna': {'Fritz': {'Hans': 13},
                   'Maria': {'Kasimir': 12}},
          'Wolfgang': {'Günther': 11}},
 'Kasimir': {'Maria': {'Anna': {'Fritz': {'Hans': 15},
                                'Joao': {'Wolfgang': {'Günther': 14}}}}},
 'Maria': {'Anna': {'Fritz': {'Hans': 17},
                    'Joao': {'Wolfgang': {'Günther': 16}}},
           'Kasimir': 18},
 'Wolfgang': {'Günther': 19,
              'Joao': {'Anna': {'Fritz': {'Hans': 21},
                                'Maria': {'Kasimir': 20}}}}}
3) --------------------------------------------------------------
[(1,
  ('Günther',
   'Wolfgang')),
 (2,
  ('Anna',
   'Joao',
   'Wolfgang'))]
{'Anna': {'Joao': {'Wolfgang': 2}},
 'Günther': {'Wolfgang': 1}}
4) --------------------------------------------------------------
[(1,
  ('Wolfgang',
   'Günther')),
 (2,
  ('Wolfgang',
   'Joao',
   'Anna',
   'Maria',
   'Kasimir')),
 (3,
  ('Wolfgang',
   'Joao',
   'Anna',
   'Fritz',
   'Hans')),
 (4,
  ('Anna',
   'Maria',
   'Kasimir')),
 (5,
  ('Anna',
   'Fritz',
   'Hans'))]
{'Anna': {'Fritz': {'Hans': 5},
          'Maria': {'Kasimir': 4}},
 'Wolfgang': {'Günther': 1,
              'Joao': {'Anna': {'Fritz': {'Hans': 3},
                                'Maria': {'Kasimir': 2}}}}}
5) --------------------------------------------------------------
[(1,
  ('Anna',
   'Joao',
   'Wolfgang',
   'Günther')),
 (2,
  ('Anna',
   'Maria',
   'Kasimir')),
 (3,
  ('Anna',
   'Fritz',
   'Hans'))]
{'Anna': {'Fritz': {'Hans': 3},
          'Joao': {'Wolfgang': {'Günther': 1}},
          'Maria': {'Kasimir': 2}}}
6) --------------------------------------------------------------
1
{'Anna': {'Fritz': {'Hans': 3},
          'Joao': {'Wolfgang': {'Günther': 'new_value_edit'}},
          'Maria': {'Kasimir': 2}}}
new_value_edit
7) --------------------------------------------------------------




treedict(
    pairs_list: list | tuple, main_mapping_keys: tuple | list = (), bi_rl_lr: str = "lr"
):
    """
    This function takes a list or tuple of pairs, a tuple or list of main mapping keys, and a string indicating the type
    of bidirectional mapping to be used. It returns a tuple of flattened dictionary and a nested dictionary.

    :param pairs_list: A list or tuple of pairs.
    :type pairs_list: list | tuple
    :param main_mapping_keys: A tuple or list of main mapping keys.
    :type main_mapping_keys: tuple | list
    :param bi_rl_lr: A string indicating the type of bidirectional mapping to be used. Default is "lr", Valid options are
                     lr - left to right / rl - right to left / bi - bidirectional
    :type bi_rl_lr: str
    :return: A tuple of flattened dictionary and a nested dictionary.
    :rtype: tuple
    """
	
edit_value_in_treedict(d: dict, keys: list | tuple, newvalue: Any) -> None:
    """
    Edit the value of a nested dictionary given a list of keys.

    Args:
        d (dict): The nested dictionary to be edited.
        keys (list,tuple): A list of keys representing the path to the value to be edited.
        newvalue (Any): The new value to be assigned to the specified key path.

    Returns:
        None: This function does not return anything, but it changes the ORIGINAL dict! If you want to keep a copy of
        the original dict, use copy.deepcopy(d) before you call the function

    Raises:
        KeyError: If any of the keys in the list do not exist in the dictionary.

    Example:
        d = {'a': {'b': {'c': 1}}}
        keys = ['a', 'b', 'c']
        newvalue = 2
        edit_value_in_treedict(d, keys, newvalue)
        # d is now {'a': {'b': {'c': 2}}}
    """	
	
	
get_value_in_treedict(d: dict, keys: list | tuple) -> Any:
    """
    Returns the value in a nested dictionary `d` at the specified `keys`.

    Args:
        d (dict): The nested dictionary to search for the value.
        keys (list|tuple): The list or tuple of keys to traverse the nested dictionary.

    Returns:
        Any: The value at the specified `keys` in the nested dictionary `d`.

    Raises:
        TypeError: If `d` is not a dictionary or `keys` is not a list or tuple.
        KeyError: If any of the keys in `keys` do not exist in the nested dictionary `d`.
    """
	
```