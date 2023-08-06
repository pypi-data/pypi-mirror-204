import streamlit.components.v1 as components
import os

_RELEASE = True

if not _RELEASE:
    # Declare the component with a given name and URL if we're not in release mode.
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "st_ant_menu",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3000",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_ant_menu", path=build_dir)

def st_ant_menu(menu_data = None, key="first_menu", defaultValue=None, defaultSelectedKeys=None, defaultOpenKeys=None, additionalHeight=100, multiple=False, css_styling=None, theme="light",menu_click=False, iconSize=15) :
    """
    Create a menu component that can be used in Streamlit.

    :param menu_data: The data to be displayed in the menu. Must be a list of dictionaries
        that conform to the Ant Design Menu item specification. See
        https://ant.design/components/menu/#Menu.Item for more information.
    :param key: The key associated with the component. This is used to ensure that
        the component is rendered properly when its value changes.
    :param defaultValue: The default value to be displayed in the component.
    :param defaultSelectedKeys: The default selected keys in the menu.
    :param defaultOpenKeys: The default open keys in the menu.
    :param additionalHeight: The additional height of the menu that should be added
        to the Streamlit iframe height. This is used to ensure that the entire menu
        is visible in the Streamlit app.
    :param multiple: Whether the menu allows multiple selections. (Broken)
    :param css_styling: A dictionary of CSS styling to be applied to the component.
    :param theme: The theme of the menu. Can be either "light" or "dark".
    :param iconSize: The size of the icons in the menu. Default is 15.

    :return: The value of the component.
    """

    # Call the component function with the given parameters.
    component_value = _component_func(
        menu_data=menu_data,
        key=key,
        defaultSelectedKeys=defaultSelectedKeys,
        defaultOpenKeys=defaultOpenKeys,
        default=defaultValue,
        multiple=multiple,
        additionalHeight=additionalHeight,
        css_styling=css_styling,
          theme = theme, 
          menu_click = menu_click,
            iconSize = iconSize
    )

    # Return the component value, handling the case where it's a list.
    if menu_click == True:
        if isinstance(component_value, list):
            return component_value[0] if len(component_value) == 1 else component_value[-1]
        
    if multiple == False:
        if isinstance(component_value, list):
            if len(component_value) == 0:
                return None
            else:
                return component_value[0]
        

    return component_value