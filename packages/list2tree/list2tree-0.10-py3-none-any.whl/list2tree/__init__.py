import operator
import sys
from collections import defaultdict
from functools import reduce
import random
from typing import Any

from flatten_any_dict_iterable_or_whatsoever import fla_tu


def treedict(
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
    if not isinstance(pairs_list, list):
        pairs_list = list(pairs_list)
    pairs_as_list = pairs_list.copy()
    if bi_rl_lr.lower() == "bi":
        tem = [list(reversed(aa)) for aa in pairs_as_list]
        pairs_as_list.extend(tem)
    elif bi_rl_lr.lower() == "rl":
        pairs_as_list = [list(reversed(aa)) for aa in pairs_as_list]
    if not main_mapping_keys:
        main_mapping_keys = tuple(set([q[0] for q in fla_tu(pairs_as_list)]))
        try:
            main_mapping_keys = tuple(sorted(main_mapping_keys))
        except Exception:
            pass
    dummykey = sys.maxsize / random.uniform(2, 500) + random.uniform(1, 500)
    coun = 0

    def convert_to_normal_dict_simple(di):
        if isinstance(di, defaultdict):
            di = {k: convert_to_normal_dict_simple(v) for k, v in di.items()}
        return di

    def convert_to_normal_dict(di):
        nonlocal coun
        if isinstance(di, defaultdict):
            if dummykey in di:
                if di[dummykey] == 0:
                    del di[dummykey]
            di = {
                k: convert_to_normal_dict(v)
                if [q for q in v.keys() if q != dummykey]
                else convert_to_normal_dict(dummykey)
                for k, v in di.items()
            }
        if isinstance(di, float):
            if di == dummykey:
                coun = coun + 1
                return coun
        return di

    def get_all_routes():
        def get_all_subroutes(airportnick):
            if isinstance(airportnick, str):
                airportnick = (airportnick,)
            for child in copyofairportdict[airportnick[-1]]:
                all_parsed_flight_routes = tuple(fla_tu(airportvariations))
                for c, parsed_flight_route in all_parsed_flight_routes:
                    if airportnick[-1] in parsed_flight_route:
                        ina = parsed_flight_route.index(airportnick[-1])
                        cut_parsed_index = parsed_flight_route[: ina + 1]
                        if (
                            index_and_child := cut_parsed_index + (child,)
                        ) in alreadydone:
                            continue
                        subdict_of_airport = reduce(
                            operator.getitem, cut_parsed_index, airportvariations
                        )

                        if child not in subdict_of_airport:
                            subdict_of_airport[child] = dummydict.copy()
                        if activemainkey == child:
                            alreadydone.add((child,))
                            continue
                        if not index_and_child in alreadydone:
                            alreadydone.add(index_and_child)
                            get_all_subroutes(index_and_child)

            for _, parsedairportroute in tuple(fla_tu(airportvariations)):
                if parsedairportroute[:-1] not in alreadydone:
                    alreadydone.add(parsedairportroute[:-1])
                    get_all_subroutes(parsedairportroute[:-1])

        alreadydone = set()

        activemainkey = None
        for sta in main_mapping_keys:
            activemainkey = sta
            airportvariations[sta] = dummydict.copy()
            get_all_subroutes(sta)

    nested_dict = lambda: defaultdict(nested_dict)

    dummydict = nested_dict()
    dummydict[dummykey] = 0

    routes = pairs_as_list.copy()

    active_parser_dict = defaultdict(list)
    for r in routes:
        active_parser_dict[r[0]].append(r[1])

    copyofairportdict = active_parser_dict.copy()

    airportvariations = nested_dict()

    get_all_routes()
    fa = convert_to_normal_dict(airportvariations.copy())
    fa2 = list(fla_tu(fa))

    formatedlist = [
        x[1] if x[1][0] != x[1][-1] or len(x[1]) == 1 else x[1][:-1] for x in fa2
    ]
    formatedlist = sorted(
        [x if x[-1] not in x[:-1] else x[:-1] for x in formatedlist],
        key=len,
        reverse=False,
    )
    nested_final_dict = nested_dict()
    for ini, fo in enumerate(formatedlist):
        if len(fo) == 1:
            nested_final_dict[fo[0]] = dummydict.copy()
        else:
            reduce(operator.getitem, fo[:-1], nested_final_dict)[
                fo[-1]
            ] = dummydict.copy()

    coun = 0
    finalnice = convert_to_normal_dict(nested_final_dict.copy())
    return list(fla_tu(finalnice)), finalnice


def edit_value_in_treedict(d: dict, keys: list | tuple, newvalue: Any) -> None:
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
    if len(keys) == 1:
        d[keys[0]] = newvalue
    else:
        reduce(operator.getitem, keys[:-1], d)[keys[-1]] = newvalue


def get_value_in_treedict(d: dict, keys: list | tuple) -> Any:
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

    return reduce(operator.getitem, keys, d)
