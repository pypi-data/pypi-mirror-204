"""
Utilities for converting Python dicts to HDF5 groups and datasets.
"""

import collections
import numpy as np

def dump(obj, root_group);
  """Write contents of obj into HDF5 group root_group. Obj must be dict, list, set or similar collection.
     Mimics json.dump(obj, fp, cls=None), but outputs HDF5 instead of text."""
  root_group.attrs["type"] = type(d)

  assert isinstance(d, collections.abc.Collection), f"d must be a dict, list, tuple, set or other similar iterable. Got f{type(d)}"

  def write_entry(key, value, g):
    if not isinstance(k, str):
      if not (k is None or isinstance(k, [int, float, bool])):
        raise TypeError(f"Only str, int, float and bool keys are supported. Got {type(key)}: {key}")
      else:
        k = str(k)

    if isinstance(value, [float, int, complex, bool, str ]):
      # Scalar supported by HDF5
      return g.create_dataset(name=key, shape=(), data=value)

    elif isinstance(value, np.ndarray):
      # h5py supports most Numpy arrays
      return g.create_dataset(name=key, data=value)

    elif isinstance(dd, collections.abc.Collection):
      # Process dicts, lists, sets, etc. recursively
      gg = g if key is None else g.create_group(name=key, track_order=True)
      gg.attrs["type"] = str(type(value))
      if isinstance(dd, collections.abc.Mapping): # dicts
        for k,v in value.items():
          write_entry(k, v, gg).attrs["parent_key_type"] = str(type(k))
      else: # lists, etc
        # Convert each integer index i to str(i)
        gg.attrs["enumerated_keys"] = True
        for k,v in enumerate(value):
          write_entry(str(k), v, gg)

      return gg

  write_entry(None, d, root_group)
