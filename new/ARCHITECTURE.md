# 🏗️ Architecture Overview

## 📁 Project Structure

```
new/                                    # Root directory
│
├── app.py                              # 🚀 MAIN APPLICATION (start here!)
│   └── Streamlit entry point, UI layout, navigation
│
├── config/                             # ⚙️ CONFIGURATION
│   ├── __init__.py
│   └── settings.py                     # All constants, colors, sizes, layout
│
├── models/                             # 📐 DATA MODELS
│   ├── __init__.py
│   └── geometry.py                     # Point3D, Edge, Face, GeometryHelper
│
├── steps/                              # 📚 STEP DEFINITIONS
│   ├── __init__.py
│   ├── base_step.py                    # Abstract Step class (Template Method)
│   ├── step_registry.py                # Singleton Registry for step management
│   │
│   └── definitions/                    # Concrete step implementations
│       ├── __init__.py
│       ├── intro.py                    # Step 0: Introduction
│       ├── tetrahedron.py              # Steps 1-3: Tetrahedron
│       ├── octahedron.py               # TODO: Steps 4-5
│       ├── icosahedron.py              # TODO: Steps 6-8
│       ├── dodecahedron.py             # TODO: Steps 9-12
│       └── bonus.py                    # TODO: Step 13
│
├── views/                              # 🎨 PRESENTATION LAYER
│   ├── __init__.py
│   └── renderer.py                     # Renderer3D helper class
│
├── utils/                              # 🔧 UTILITIES
│   ├── __init__.py
│   └── helpers.py                      # (Currently empty, for future helpers)
│
├── requirements.txt                    # 📦 Dependencies
├── README.md                           # 📖 Main documentation
├── QUICKSTART.md                       # 🚀 Quick start guide
└── ARCHITECTURE.md                     # 📐 This file
```

---

## 🔄 Data Flow

```
User Interaction (Streamlit UI)
         │
         ▼
    app.py (Controller)
         │
         ├─────► StepRegistry ──► Get current Step instance
         │                              │
         │                              ▼
         │                         Step.get_metadata()
         │                         Step.get_description()
         │                         Step.render_diagram()
         │                              │
         ▼                              ▼
    Streamlit Layout            Matplotlib Figure
         │                              │
         ├── Left Column ──────►  3D Diagram (from render_diagram)
         │                        Uses: Renderer3D helpers
         │                        Uses: config/settings
         │
         └── Right Column ─────►  Description (Markdown)
                                  From: get_description()
```

---

## 🎯 Design Patterns Used

### 1. **Template Method Pattern**

**File:** `steps/base_step.py`

```python
class Step(ABC):
    """Abstract base class defines the structure"""

    @abstractmethod
    def get_metadata(self) -> StepMetadata:
        """Subclass MUST implement"""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Subclass MUST implement"""
        pass

    @abstractmethod
    def render_diagram(self, fig, ax) -> None:
        """Subclass MUST implement"""
        pass

    def setup_axes(self, ax) -> None:
        """Common implementation provided by base class"""
        # ... all subclasses can use this ...
```

**Benefits:**
- Enforces consistent structure for all steps
- Reduces code duplication
- Easy to add new steps

---

### 2. **Singleton Registry Pattern**

**File:** `steps/step_registry.py`

```python
class StepRegistry:
    """One global instance manages all steps"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._steps = []
        return cls._instance

    def register(self, step: Step) -> None:
        self._steps.append(step)

    def get_all_steps(self) -> List[Step]:
        return sorted(self._steps, key=lambda s: s.metadata.number)
```

**Benefits:**
- Centralized step management
- Automatic organization into categories
- Single source of truth

---

### 3. **Strategy Pattern**

**File:** Each step implements its own rendering strategy

```python
class TetraStep1_Cube(Step):
    def render_diagram(self, fig, ax):
        # Custom rendering for cube view
        Renderer3D.draw_edges(...)

class TetraStep3_Complete(Step):
    def render_diagram(self, fig, ax):
        # Different rendering for complete tetrahedron
        Renderer3D.draw_points(...)
```

**Benefits:**
- Each step can render completely differently
- Flexible and extensible
- No if/else chains

---

### 4. **Dependency Injection**

**File:** `config/settings.py` provides all dependencies

```python
# All steps use the same configuration
from config.settings import COLORS, SIZES

Renderer3D.draw_point(
    ax, point,
    color=COLORS['selected_point'],
    size=SIZES['point_large']
)
```

**Benefits:**
- Easy to change colors/sizes globally
- No magic numbers in code
- Testable (can inject mock config)

---

## 🔌 How Components Connect

### Adding a New Step - Complete Flow:

```
1. Create new class in steps/definitions/
   │
   ├─► Inherit from Step
   ├─► Implement get_metadata()
   ├─► Implement get_description()
   └─► Implement render_diagram()
         │
         └─► Use Renderer3D helpers
             Use config/settings constants

2. Register in app.py
   │
   └─► registry.register(NewStep())

3. Automatic effects:
   │
   ├─► Appears in sidebar (from category)
   ├─► Gets correct navigation buttons
   ├─► Renders in 2-column layout
   └─► Inherits all base functionality
```

---

## 📊 Component Responsibilities

### `app.py` - Application Controller
**Responsibilities:**
- Setup Streamlit page config
- Create UI layout (sidebar + main content)
- Handle navigation (buttons, session state)
- Coordinate between Registry and UI

**Does NOT:**
- Know about specific step implementations
- Contain rendering logic
- Store step data

---

### `base_step.py` - Step Interface
**Responsibilities:**
- Define step contract (abstract methods)
- Provide common utilities (setup_axes)
- Store metadata

**Does NOT:**
- Know about Streamlit
- Manage step collection
- Do actual rendering (delegates to subclasses)

---

### `step_registry.py` - Step Manager
**Responsibilities:**
- Store all step instances
- Organize steps by category
- Provide step lookup methods
- Generate sidebar menu data

**Does NOT:**
- Create step instances
- Render steps
- Handle UI

---

### `renderer.py` - Rendering Utilities
**Responsibilities:**
- Provide reusable drawing functions
- Handle matplotlib boilerplate
- Apply consistent styling

**Does NOT:**
- Know about steps
- Make decisions about what to draw
- Handle layout

---

### `settings.py` - Configuration
**Responsibilities:**
- Store ALL constants
- Define colors, sizes, layouts
- Centralize configuration

**Does NOT:**
- Contain logic
- Import other modules
- Change at runtime

---

## 🧪 Testing Strategy

### Unit Tests (TODO):

```python
# tests/test_steps.py
def test_tetra_step1_has_correct_metadata():
    step = TetraStep1_Cube()
    assert step.metadata.number == 1
    assert step.metadata.category == 'Čtyřstěn'

# tests/test_registry.py
def test_registry_sorts_steps_by_number():
    registry = StepRegistry()
    registry.register(Step(number=3))
    registry.register(Step(number=1))
    steps = registry.get_all_steps()
    assert steps[0].metadata.number == 1
```

### Integration Tests (TODO):

```python
# tests/test_integration.py
def test_all_steps_render_without_error():
    for step in registry.get_all_steps():
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        step.render_diagram(fig, ax)  # Should not throw
```

---

## 🔒 SOLID Principles Compliance

### **S - Single Responsibility**
✅ Each class has one reason to change:
- `Step`: Step definition only
- `Registry`: Step collection only
- `Renderer3D`: Drawing primitives only
- `app.py`: UI orchestration only

### **O - Open/Closed**
✅ Open for extension, closed for modification:
- Add new step: Extend Step, don't modify base
- Change rendering: Override method, don't modify Renderer3D

### **L - Liskov Substitution**
✅ Any Step subclass works anywhere Step is expected:
- `registry.register(any_step)` works for all Step types
- `step.render_diagram(fig, ax)` works for all implementations

### **I - Interface Segregation**
✅ No client forced to depend on unused methods:
- Step interface is minimal (3 abstract methods)
- Renderer3D provides specific methods, not one giant render()

### **D - Dependency Inversion**
✅ Depend on abstractions, not concretions:
- app.py depends on Step interface, not concrete steps
- Steps depend on Renderer3D interface, not specific implementations

---

## 🎓 Learning Path for New Developers

### Level 1: Add a Simple Step
1. Copy `intro.py` as template
2. Change metadata (number, title, category)
3. Edit description text
4. Modify render_diagram with simple drawing

### Level 2: Use Advanced Rendering
1. Study `tetrahedron.py` examples
2. Use Renderer3D helpers
3. Add custom calculations
4. Use geometry helpers

### Level 3: Extend the Framework
1. Add new Renderer3D methods
2. Create new geometry classes
3. Add configuration options
4. Implement custom base classes

---

## 📈 Future Enhancements

### Short Term:
- [ ] Add remaining steps (Octahedron, Icosahedron, Dodecahedron)
- [ ] Add unit tests
- [ ] Add keyboard navigation (arrow keys)

### Medium Term:
- [ ] Export diagrams as images
- [ ] Add animation between steps
- [ ] Implement step bookmarks
- [ ] Add quiz questions per step

### Long Term:
- [ ] Multi-language support (English)
- [ ] Interactive 3D manipulation (rotate with sliders)
- [ ] Export as PDF presentation
- [ ] Deployment to Streamlit Cloud

---

**Last Updated:** 2026-01-04
**Version:** 2.0.0
**Maintainer:** Educational Math Team
