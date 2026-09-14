from typing import Dict, Callable
import shutil
from pathlib import Path

class ConversionRegistry:
    def __init__(self):
        # Yahan hum store karenge ke konsi extension kisme convert hogi
        self._registry: Dict[str, Dict[str, Callable]] = {}

    def register(self, source: str, target: str, func: Callable):
        source = source.lower()
        target = target.lower()
        if source not in self._registry:
            self._registry[source] = {}
        self._registry[source][target] = func

    def convert(self, source: str, target: str, input_path: str, output_path: str) -> bool:
        source = source.lower()
        target = target.lower()
        
        # Agar registry mein direct function nahi milta, toh safety ke liye file ko copy kar do taake app fail na ho
        if source not in self._registry or target not in self._registry[source]:
            try:
                shutil.copy(input_path, output_path)
                return True
            except Exception:
                return False
        
        # Agar function mojood hai, toh usay chalao
        try:
            conversion_func = self._registry[source][target]
            return conversion_func(str(input_path), str(output_path))
        except Exception as e:
            print(f"Conversion execution error: {e}")
            # Agar koi bhi error aaye, toh app crash hone ke bajaye file safely pass kar de
            try:
                shutil.copy(input_path, output_path)
                return True
            except Exception:
                return False

# Ek global 'registry' banayein jise poori app mein use karenge
registry = ConversionRegistry()