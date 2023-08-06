# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import switch_api as sw


def set_cache(api_inputs, guide_id, key, val):
    """
    Sets data to be stored in cache for later retrieval.

    Parameters
    ----------
    api_inputs: ApiInputs
        Object returned by initialize() function.
    guide_id: str
        Guide Id, previously known as Journey Id, scope of the cache.
    key: str
        Key of to be stored data. Used when retrieving this data.
    val: any
        Data to be stored for later retrieval.

    """
    
    return sw.cache.set_cache(
        api_inputs=api_inputs,
        scope="Portfolio",
        key=f'{guide_id}-{key}',
        val=val
    )


def get_cache(api_inputs, guide_id, key):
    """
    Gets data stored in cache.

    Parameters
    ----------
    api_inputs: ApiInputs
        Object returned by initialize() function.
    guide_id: str
        Guide Id, previously known as Journey Id, scope of the cache.
    key: str
        Key of to be stored data. Used when retrieving this data.

    """
    
    return sw.cache.get_cache(
        api_inputs=api_inputs,
        scope="Portfolio",
        key=f'{guide_id}-{key}',
    )
