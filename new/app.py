"""
Hlavní Streamlit aplikace pro Platónská tělesa
Main Streamlit application for Platonic Solids tutorial
"""
import streamlit as st
import plotly.graph_objects as go

# Konfigurace musí být první Streamlit příkaz
from config.settings import PAGE_CONFIG, LAYOUT
st.set_page_config(**PAGE_CONFIG)

# Import kroků
from steps.step_registry import get_registry
from steps.definitions.intro import IntroStep
from steps.definitions.tetrahedron import (
    TetraStep1_Cube,
    TetraStep2_Selection,
    TetraStep3_Complete
)
from steps.definitions.octahedron import (
    OctaStep1_Axes,
    OctaStep2_Complete
)
from steps.definitions.icosahedron import (
    IcosaStep1_Rectangle,
    IcosaStep2_ThreeRectangles,
    IcosaStep3_Complete
)
from steps.definitions.dodecahedron import (
    DodecaStep1_Cube,
    DodecaStep2_GoldenRectangles,
    DodecaStep3_Complete
)
from steps.definitions.bonus import BonusStep_TriangleCenter


def register_all_steps():
    """Zaregistruje všechny kroky do registry"""
    registry = get_registry()
    registry.clear()  # Vyčisti registry (důležité pro reload)

    # Úvod
    registry.register(IntroStep())

    # Čtyřstěn (Tetrahedron)
    registry.register(TetraStep1_Cube())
    registry.register(TetraStep2_Selection())
    registry.register(TetraStep3_Complete())

    # Osmistěn (Octahedron)
    registry.register(OctaStep1_Axes())
    registry.register(OctaStep2_Complete())

    # Dvacetistěn (Icosahedron)
    registry.register(IcosaStep1_Rectangle())
    registry.register(IcosaStep2_ThreeRectangles())
    registry.register(IcosaStep3_Complete())

    # Dvanáctistěn (Dodecahedron)
    registry.register(DodecaStep1_Cube())
    registry.register(DodecaStep2_GoldenRectangles())
    registry.register(DodecaStep3_Complete())

    # Bonus
    registry.register(BonusStep_TriangleCenter())


def initialize_session_state():
    """Inicializuje session state pro Streamlit"""
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0

    # Nastavení pro vykreslování stěn
    if 'show_faces' not in st.session_state:
        st.session_state.show_faces = False

    if 'face_opacity' not in st.session_state:
        st.session_state.face_opacity = 0.5

    if 'face_color' not in st.session_state:
        st.session_state.face_color = '#00CED1'  # DarkTurquoise (výrazná azurová)

    # Nastavení pro hrany a vrcholy
    if 'edge_width' not in st.session_state:
        st.session_state.edge_width = 3

    if 'vertex_size' not in st.session_state:
        st.session_state.vertex_size = 12


def render_sidebar():
    """Vykreslí sidebar s navigací"""
    st.sidebar.title("📐 Navigace")
    st.sidebar.markdown("---")

    registry = get_registry()
    menu = registry.get_sidebar_menu()

    # Pro každou kategorii zobraz sekci
    for category, steps in menu.items():
        st.sidebar.subheader(category)

        for step_num, step_name in steps:
            # Tlačítko pro každý krok
            if st.sidebar.button(
                f"{step_num}. {step_name}",
                key=f"step_{step_num}",
                width='stretch'
            ):
                st.session_state.current_step = step_num

        st.sidebar.markdown("")  # Mezera mezi kategoriemi

    # Nastavení vykreslování stěn
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎨 Nastavení zobrazení")

    # Checkbox pro zobrazení stěn
    st.session_state.show_faces = st.sidebar.checkbox(
        "Zobrazit stěny těles",
        value=st.session_state.show_faces,
        help="Zapne/vypne vykreslování stěn 3D těles"
    )

    # Nastavení barvy a průhlednosti (pouze pokud jsou stěny zapnuté)
    if st.session_state.show_faces:
        st.session_state.face_color = st.sidebar.color_picker(
            "Barva stěn",
            value=st.session_state.face_color,
            help="Vyber barvu pro stěny těles"
        )

        st.session_state.face_opacity = st.sidebar.slider(
            "Průhlednost stěn",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.face_opacity,
            step=0.05,
            help="0.0 = průhledné, 1.0 = neprůhledné"
        )

    # Nastavení hran a vrcholů
    st.sidebar.markdown("### ⚙️ Hrany a vrcholy")

    st.session_state.edge_width = st.sidebar.slider(
        "Tloušťka hran",
        min_value=1,
        max_value=8,
        value=st.session_state.edge_width,
        step=1,
        help="Tloušťka čar pro hrany těles"
    )

    st.session_state.vertex_size = st.sidebar.slider(
        "Velikost vrcholů",
        min_value=5,
        max_value=25,
        value=st.session_state.vertex_size,
        step=1,
        help="Velikost bodů reprezentujících vrcholy"
    )

    # Informace na konci sidebaru
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### 💡 Tip:
    Můžeš otáčet 3D diagramem myší!

    ### 📚 O aplikaci:
    Interaktivní tutoriál pro
    konstrukci Platónských těles.

    **Verze:** 2.0.0
    """)


def render_step_navigation(position="top"):
    """Vykreslí navigační tlačítka mezi kroky

    Args:
        position: "top" nebo "bottom" - pro unikátní klíče tlačítek
    """
    registry = get_registry()
    current = st.session_state.current_step
    total = registry.get_step_count()

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if current > 0:
            if st.button("⬅️ Předchozí",
                        key=f"prev_{position}",
                        width='stretch'):
                st.session_state.current_step -= 1
                st.rerun()

    with col2:
        st.markdown(
            f"<h4 style='text-align: center'>Krok {current} / {total - 1}</h4>",
            unsafe_allow_html=True
        )

    with col3:
        if current < total - 1:
            if st.button("Další ➡️",
                        key=f"next_{position}",
                        width='stretch'):
                st.session_state.current_step += 1
                st.rerun()


def create_plotly_figure(step):
    """
    Vytvoří interaktivní Plotly 3D figure pro daný krok

    Args:
        step: Instance kroku

    Returns:
        Plotly Figure s interaktivní 3D vizualizací
    """
    # Nech krok vykreslit Plotly diagram
    fig = step.render_plotly_diagram()
    return fig


def render_main_content():
    """Vykreslí hlavní obsah - diagram + popis"""
    registry = get_registry()
    step = registry.get_step_by_number(st.session_state.current_step)

    if step is None:
        st.error("Krok nenalezen!")
        return

    # Vytvoř dva sloupce - diagram vlevo, popis vpravo
    col_diagram, col_description = st.columns([
        LAYOUT['diagram_column_ratio'],
        LAYOUT['description_column_ratio']
    ])

    # Levý sloupec - 3D diagram
    with col_diagram:
        st.markdown("### 🔷 Interaktivní 3D Diagram")
        st.info("💡 **Tip:** Použij myš k otáčení diagramu! Scroll kolečkem přiblíží/oddálí.")

        # Vytvoř interaktivní Plotly figure
        fig = create_plotly_figure(step)
        st.plotly_chart(fig, width='stretch')

    # Pravý sloupec - popis
    with col_description:
        st.markdown("### 📝 Vysvětlení")
        st.markdown(step.get_description())


def main():
    """Hlavní funkce aplikace"""
    # Inicializace
    register_all_steps()
    initialize_session_state()

    # Vykreslení UI
    render_sidebar()

    # Hlavní nadpis
    st.title("📐 Platónská tělesa - Interaktivní tutoriál")
    st.markdown("---")

    # Navigační tlačítka nahoře
    render_step_navigation(position="top")

    st.markdown("---")

    # Hlavní obsah
    render_main_content()

    # Navigační tlačítka dole (pro pohodlí)
    st.markdown("---")
    render_step_navigation(position="bottom")


if __name__ == "__main__":
    main()
