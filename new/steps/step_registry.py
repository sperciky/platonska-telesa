"""
Registry pro správu všech kroků prezentace
Step registry for managing all presentation steps
"""
from typing import List, Dict, Optional
from .base_step import Step


class StepRegistry:
    """
    Singleton registry pro správu všech kroků

    Použití:
        registry = StepRegistry()
        registry.register(IntroStep())
        registry.register(TetraStep1())
        ...
        all_steps = registry.get_all_steps()
    """

    _instance = None
    _steps: List[Step] = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StepRegistry, cls).__new__(cls)
            cls._instance._steps = []
        return cls._instance

    def register(self, step: Step) -> None:
        """Zaregistruje nový krok"""
        self._steps.append(step)

    def get_all_steps(self) -> List[Step]:
        """Vrátí všechny zaregistrované kroky seřazené podle čísla"""
        return sorted(self._steps, key=lambda s: s.metadata.number)

    def get_step_by_number(self, number: int) -> Optional[Step]:
        """Najde krok podle čísla"""
        for step in self._steps:
            if step.metadata.number == number:
                return step
        return None

    def get_steps_by_category(self, category: str) -> List[Step]:
        """Vrátí všechny kroky dané kategorie"""
        return [s for s in self._steps if s.metadata.category == category]

    def get_step_count(self) -> int:
        """Vrátí celkový počet kroků"""
        return len(self._steps)

    def clear(self) -> None:
        """Vymaže všechny kroky (užitečné pro testování)"""
        self._steps.clear()

    def get_sidebar_menu(self) -> Dict[str, List[tuple]]:
        """
        Vrátí data pro sidebar menu organizovaná podle kategorií

        Returns:
            Dictionary: {kategorie: [(číslo, short_name), ...]}
        """
        menu = {}
        for step in self.get_all_steps():
            category = step.metadata.category
            if category not in menu:
                menu[category] = []
            menu[category].append((
                step.metadata.number,
                step.metadata.short_name
            ))
        return menu


# Globální instance registry
_global_registry = StepRegistry()


def get_registry() -> StepRegistry:
    """Vrátí globální instanci registry"""
    return _global_registry
