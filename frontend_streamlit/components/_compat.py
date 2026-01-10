"""Compatibility helpers for Streamlit API differences.

Some Streamlit versions accept `use_container_width` while older ones expect
`use_column_width`. These helpers try the newer argument first and fall back
to older names or remove unsupported kwargs so the app works across
environments.
"""
from typing import Any
import streamlit as st


def safe_image(*args: Any, **kwargs: Any) -> Any:
    """Call `st.image` compatibly across Streamlit versions.

    Tries to call `st.image` with the provided kwargs; if a TypeError is
    raised because of an unexpected keyword like `use_container_width`, it
    will attempt to map it to `use_column_width` and retry.
    """
    try:
        return st.image(*args, **kwargs)
    except TypeError as e:
        # If the error was caused by the newer kwarg, try the older one
        if 'use_container_width' in kwargs:
            val = kwargs.pop('use_container_width')
            kwargs['use_column_width'] = val
            return st.image(*args, **kwargs)
        raise


def safe_button(*args: Any, **kwargs: Any) -> Any:
    """Call `st.button` compatibly across Streamlit versions.

    Many Streamlit UI functions accept `use_container_width` in newer
    releases. If it's not supported, remove it and retry.
    """
    try:
        return st.button(*args, **kwargs)
    except TypeError:
        kwargs.pop('use_container_width', None)
        return st.button(*args, **kwargs)
