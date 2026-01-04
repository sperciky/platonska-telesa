# 📐 Platónská tělesa - Streamlit App

Moderní, škálovatelná webová aplikace pro interaktivní výuku konstrukce Platónských těles.

## ✨ Vlastnosti

- **Streamlit UI**: Moderní webové rozhraní
- **Čistá architektura**: Separation of concerns, design patterns
- **Snadná rozšiřitelnost**: Přidání nového kroku = vytvoření jedné třídy
- **Responzivní layout**: Diagram vlevo, popis vpravo, žádné překryvy
- **Sidebar navigace**: Intuitivní menu organizované podle kategorií

## 🏗️ Architektura

```
new/
├── app.py                    # Hlavní Streamlit aplikace
├── config/
│   └── settings.py           # Všechny konstanty a nastavení
├── models/
│   └── geometry.py           # Základní geometrické třídy
├── steps/
│   ├── base_step.py          # Abstraktní třída Step
│   ├── step_registry.py      # Registry pattern pro kroky
│   └── definitions/          # Konkrétní kroky
│       ├── intro.py
│       ├── tetrahedron.py
│       ├── octahedron.py     # TODO
│       └── ...
├── views/
│   └── renderer.py           # Helper funkce pro vykreslování
└── utils/
    └── helpers.py            # Pomocné nástroje
```

## 🚀 Spuštění

### 1. Instalace závislostí

```bash
cd new/
pip install -r requirements.txt
```

### 2. Spuštění aplikace

```bash
streamlit run app.py
```

Aplikace se otevře na `http://localhost:8501`

## 📚 Jak přidat nový krok

### Krok 1: Vytvoř novou třídu kroku

```python
# steps/definitions/octahedron.py
from steps.base_step import Step, StepMetadata
from views.renderer import Renderer3D

class OctaStep1(Step):
    def get_metadata(self) -> StepMetadata:
        return StepMetadata(
            number=4,
            category='Osmistěn',
            title='Osmistěn - Krok 1: Vrcholy na osách',
            short_name='1. Vrcholy na osách'
        )

    def get_description(self) -> str:
        return '''
## Osmistěn - Krok 1

Osmistěn má **6 vrcholů** umístěných na osiích...
'''

    def render_diagram(self, fig, ax):
        self.setup_axes(ax)
        # Tvoje vykreslování zde...
        Renderer3D.draw_point(ax, [1, 0, 0], color='red')
```

### Krok 2: Zaregistruj krok v app.py

```python
# app.py
from steps.definitions.octahedron import OctaStep1

def register_all_steps():
    registry = get_registry()
    # ... existující kroky ...
    registry.register(OctaStep1())  # Přidej zde!
```

**Hotovo!** Krok se automaticky objeví v sidebaru.

## 🎨 Design Patterns použité

1. **Template Method Pattern** (`base_step.py`)
   - Abstraktní třída definuje strukturu
   - Subclasses implementují specifické části

2. **Singleton Registry** (`step_registry.py`)
   - Centrální správa všech kroků
   - Automatické organizování do kategorií

3. **Strategy Pattern** (renderování)
   - Každý krok má vlastní strategii vykreslení

4. **Dependency Injection** (konfigurace)
   - Všechny nastavení v `config/settings.py`

## 🔧 Konfigurace

Všechna nastavení v `config/settings.py`:

```python
# Změň velikost figure
FIGURE = {
    'figsize': (10, 8),  # Větší diagram
    'dpi': 150,          # Vyšší kvalita
}

# Změň barvy
COLORS = {
    'tetrahedron': '#FF0000',  # Červená
}
```

## 📁 Struktura kroku

Každý krok musí implementovat:

1. **`get_metadata()`** - Vrací StepMetadata
   - `number`: Pořadové číslo (0-based)
   - `category`: Kategorie pro sidebar
   - `title`: Plný název kroku
   - `short_name`: Krátký název do sidebaru

2. **`get_description()`** - Vrací Markdown text
   - Podporuje **Markdown** formátování
   - Může obsahovat math: `$\\sqrt{2}$`
   - Code bloky: ` ```python ... ``` `

3. **`render_diagram(fig, ax)`** - Vykreslí 3D diagram
   - `fig`: Matplotlib Figure
   - `ax`: Matplotlib 3D Axes
   - Použij `Renderer3D` helper třídu

## 🧪 Testování

### Manuální test:

1. Spusť aplikaci
2. Proklikej všechny kroky
3. Ověř, že diagram a popis sedí dohromady

### Automatické testy (TODO):

```bash
pytest tests/
```

## 📊 Současný stav

✅ **Hotové:**
- Základní architektura
- Streamlit UI s navigací
- Úvodní krok
- Čtyřstěn - všechny 3 kroky (0-3)

🚧 **TODO:**
- Osmistěn (kroky 4-5)
- Dvacetistěn (kroky 6-8)
- Dvanáctistěn (kroky 9-12)
- Bonus: Střed trojúhelníku (krok 13)

## 🆚 Porovnání se starou verzí

| Aspekt | Stará verze (`navod2.py`) | Nová verze (`new/`) |
|--------|---------------------------|---------------------|
| **UI** | Matplotlib buttons | Streamlit web app |
| **Layout** | Překrývání textů | Čistý 2-column layout |
| **Přidání kroku** | Editace 3-4 souborů | Vytvoření 1 třídy |
| **Konfigurace** | Rozházeno v kódu | Vše v `settings.py` |
| **Testovatelnost** | Těžká | Snadná (unit tests) |
| **Deployment** | Desktop only | Web (Streamlit Cloud) |
| **Kód** | 750 řádků v 1 souboru | ~50 řádků na soubor |

## 🎓 Pro výuku

Tato aplikace je ideální pro:
- **Interaktivní prezentace** ve škole
- **Domácí studium** s vlastním tempem
- **Matematické kroužky**
- **Online výuku** (sdílení přes Streamlit Cloud)

## 📝 License

Educational use - pro výuku matematiky.

---

**Vytvořeno s ❤️ pro 10leté matematiky!**
