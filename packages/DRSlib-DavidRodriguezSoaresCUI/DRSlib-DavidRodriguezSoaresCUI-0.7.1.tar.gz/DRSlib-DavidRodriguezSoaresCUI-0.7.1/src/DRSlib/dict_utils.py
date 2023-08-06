"""
Dictionnary utils
=================

Methods that perform simple but convenient operations,
specifically on dictionnaries
"""

from typing import Any, Dict, List, Set

from .utils import assertTrue


def flatten_dict_join(d: Dict[str, Any]) -> Dict[str, Any]:
    """Returns a dictionnary with similar content but no nested dictionnary value
    WARNING: requires all keys to be str !
    Strategy to conserve key uniqueness is `key joining`:  d[k1][k2] -> d[k1.k2]
    """
    dflat = {}
    for k, v in d.items():
        assertTrue(isinstance(k, str), "Key {} is a {}, not str !", k, type(k))
        if isinstance(v, dict):
            d2 = flatten_dict_join(v)
            for k2, v2 in d2.items():
                assertTrue(
                    isinstance(k, str), "Key {} is a {}, not str !", k2, type(k2)
                )
                k1_2 = k + "." + k2
                assertTrue(
                    k1_2 not in dflat, "Collision: key {} already in dict !", k1_2
                )
                dflat[k1_2] = v2
            continue

        assertTrue(k not in dflat, "Collision: key {} already in dict !", k)
        dflat[k] = v

    return dflat


def dict_difference(dictA: dict, dictB: dict) -> dict:
    """Performs dictA - dictB on the values: Returns a dictionnary
    with all items from dictA minus the key-value pairs in common with dictB"""
    diff = {
        k: dict_difference(v_a, dictB[k])
        if isinstance(v_a, dict) and k in dictB
        else v_a
        for k, v_a in dictA.items()
        if (k not in dictB) or (isinstance(v_a, dict) or v_a != dictB[k])
    }
    for k in list(diff.keys()):
        if diff[k] == {}:
            del diff[k]
    return diff


def dict_list_keys(d: dict) -> List[str]:
    """Searches (recursively) for all keys within dictionnary and returns them in an ordered list.
    Warns on duplicate."""

    def add_item_to_set_or_warn(_set: Set[Any], item: Any) -> None:
        if item in _set:
            print(f"Item '{item}' already in set !")
        else:
            _set.add(item)

    keys: Set[str] = set()
    for k in d:
        if isinstance(d[k], dict):
            for k2 in dict_list_keys(d[k]):
                add_item_to_set_or_warn(keys, k2)
            continue
        add_item_to_set_or_warn(keys, k)

    return list(sorted(keys))
