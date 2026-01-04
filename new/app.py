"""
Hlavní Streamlit aplikace pro Platónská tělesa
Main Streamlit application for Platonic Solids tutorial
"""
import streamlit as st
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Konfigurace musí být první Streamlit příkaz
from config.settings import PAGE_CONFIG, LAYOUT, FIGURE
st.set_page_config(**PAGE_CONFIG)

# Import kroků
from steps.step_registry import get_registry
from steps.definitions.intro import IntroStep
from steps.definitions.tetrahedron import (
    TetraStep1_Cube,
    TetraStep2_Selection,
    TetraStep3_Complete
)


def register_all_steps():
    """Zaregistruje všechny kroky do registry"""
    registry = get_registry()
    registry.clear()  # Vyčisti registry (důležité pro reload)

    # Zaregistruj všechny kroky
    registry.register(IntroStep())
    registry.register(TetraStep1_Cube())
    registry.register(TetraStep2_Selection())
    registry.register(TetraStep3_Complete())

    # TODO: Přidej další kroky zde:
    # registry.register(OctaStep1())
    # registry.register(OctaStep2())
    # ...


def initialize_session_state():
    """Inicializuje session state pro Streamlit"""
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0


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
                use_container_width=True
            ):
                st.session_state.current_step = step_num

        st.sidebar.markdown("")  # Mezera mezi kategoriemi

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
                        use_container_width=True):
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
                        use_container_width=True):
                st.session_state.current_step += 1
                st.rerun()


def create_3d_figure(step, elevation=None, azimuth=None):
    """
    Vytvoří matplotlib 3D figure pro daný krok

    Args:
        step: Instance kroku
        elevation: Úhel elevace (nahoru/dolů) v stupních
        azimuth: Úhel azimutu (otočení) v stupních

    Returns:
        matplotlib Figure
    """
    fig = plt.figure(figsize=FIGURE['figsize'], dpi=FIGURE['dpi'])
    fig.patch.set_facecolor(FIGURE['facecolor'])

    ax = fig.add_subplot(111, projection='3d')

    # Nech krok vykreslit diagram
    step.render_diagram(fig, ax)

    # Nastav úhel pohledu, pokud je specifikován
    if elevation is not None or azimuth is not None:
        current_elev, current_azim = ax.elev, ax.azim
        ax.view_init(
            elev=elevation if elevation is not None else current_elev,
            azim=azimuth if azimuth is not None else current_azim
        )

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
        st.markdown("### 🔷 3D Diagram")

        # Ovládání rotace
        with st.expander("🔄 Otáčení diagramu", expanded=False):
            col_elev, col_azim = st.columns(2)
            with col_elev:
                elevation = st.slider(
                    "Elevace (nahoru/dolů)",
                    min_value=-90,
                    max_value=90,
                    value=20,
                    step=5,
                    key=f"elev_{st.session_state.current_step}"
                )
            with col_azim:
                azimuth = st.slider(
                    "Azimut (otočení)",
                    min_value=0,
                    max_value=360,
                    value=45,
                    step=5,
                    key=f"azim_{st.session_state.current_step}"
                )

        # Vytvoř figure s nastaveným úhlem pohledu
        fig = create_3d_figure(step, elevation=elevation, azimuth=azimuth)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)  # Uvolni paměť

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
