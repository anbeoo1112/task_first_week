"""
Local package marker for compatibility shim.
This ensures Python treats the local `google` package before site-packages
so `import google.generativeai` can be redirected to `google.genai`.
"""

__all__ = ["generativeai"]
