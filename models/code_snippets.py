"""
models/code_snippets.py

Loader for snippet files. Scans models/snippets/<stack>/ for files and returns
random snippets. Safe: only reads files.
"""

import os
import random
from typing import List, Optional


class CodeSnippets:
    """
    Loads snippet files from a directory structure:

    hubstaff_simulator/
    └── models/
        └── snippets/
            ├── html/
            │   ├── sample1.html
            │   └── ...
            ├── python/
            │   └── sample1.py
            └── js/
                └── sample1.js

    get_random(stack) -> returns the file contents as a string.
    """

    def __init__(self, base_dir: Optional[str] = None):
        # default to models/snippets relative to this file
        here = os.path.dirname(__file__)
        default = os.path.abspath(os.path.join(here, "snippets"))
        self.base_dir = os.path.abspath(base_dir) if base_dir else default

    def available_stacks(self) -> List[str]:
        if not os.path.isdir(self.base_dir):
            return []
        return sorted(
            name for name in os.listdir(self.base_dir)
            if os.path.isdir(os.path.join(self.base_dir, name))
        )

    def list_files(self, stack: str) -> List[str]:
        stack_dir = os.path.join(self.base_dir, stack)
        if not os.path.isdir(stack_dir):
            return []
        return sorted(
            f for f in os.listdir(stack_dir)
            if os.path.isfile(os.path.join(stack_dir, f))
        )

    def get_random(self, stack: str) -> str:
        """
        Return the content of a random snippet file for `stack`.
        If stack/folder missing, returns a small default string.
        """
        stack_dir = os.path.join(self.base_dir, stack)
        if not os.path.isdir(stack_dir):
            return f"// No snippets found for stack '{stack}'.\n"

        files = self.list_files(stack)
        if not files:
            return f"// No snippet files in {stack_dir}\n"

        chosen = random.choice(files)
        path = os.path.join(stack_dir, chosen)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return fh.read()
        except Exception as exc:
            return f"// Failed to read {path}: {exc}\n"
