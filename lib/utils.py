import toml
from pathlib import Path
import streamlit as st


def get_project_root() -> str:
    return str(Path(__file__).parent.parent)


def load_toml(name):
    return dict(toml.load(Path(get_project_root()) / f"{name}.toml"))


def display_links(links) -> None:
    n_links = len(links.keys())
    cols = st.columns(n_links)
    i = 0
    for link in links.keys():
        cols[i].markdown(
            f"<a style='display: block; text-align: center;' href={links[link]['url']}>{links[link]['name']}</a>",
            unsafe_allow_html=True,
        )
        i += 1


def display_resources(notes):
    with st.expander("Ressources", expanded=False):
        for section in notes['resources'].keys():
            st.write(f"{section} :")
            display_links(notes['resources'][section])
            st.write("")


def get_tooltip_link(link):
    return f"[{link['name']}]({link['url']})"

