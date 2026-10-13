import shutil
import traceback
from typing import Callable, Dict


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

    def supports(self, source: str, target: str) -> bool:
        """Kya ye conversion registered hai? (same format ko copy ke taur par allow hai)"""
        source = source.lower()
        target = target.lower()
        if source == target:
            return True
        return source in self._registry and target in self._registry[source]

    def convert(self, source: str, target: str, input_path: str, output_path: str) -> bool:
        source = source.lower()
        target = target.lower()

        # Same format: sirf copy (ye asli copy hai, fake conversion nahi)
        if source == target:
            try:
                shutil.copy(input_path, output_path)
                return True
            except Exception:
                print(f"Copy error: {traceback.format_exc()}")
                return False

        # Registered na ho to fake copy NAHI karte, saaf False dete hain
        if not self.supports(source, target):
            print(f"Conversion supported nahi hai: {source} -> {target}")
            return False

        try:
            conversion_func = self._registry[source][target]
            return bool(conversion_func(str(input_path), str(output_path)))
        except Exception:
            # Error ko chhupane ke bajaye log karo aur upar batao
            print(f"Conversion execution error ({source} -> {target}):\n{traceback.format_exc()}")
            return False


# Ek global 'registry' banayein jise poori app mein use karenge
registry = ConversionRegistry()