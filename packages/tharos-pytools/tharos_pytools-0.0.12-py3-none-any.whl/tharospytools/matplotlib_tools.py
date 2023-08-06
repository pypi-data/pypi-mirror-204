'Tools to assist with graphs creation'
import matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex, hex2color
from mycolorpy import colorlist


def get_palette(number_of_colors: int, cmap_name: str = 'viridis', as_hex: bool = False, as_rgba: bool = False, alpha_value: float = 1.0) -> list:
    """Returns a number_of_colors-sized palette, as a list,
    that one can access with colors[i].

    Args:
        number_of_colors (int): number of colors needed
        cmap_name (str, optionnal) : name of the matplotlib colormap. Defaults to viridis.
        as_hex (bool, optional) : specifies if colors shall be returned by rgb values (False, default) or hex (True)
        as_rgba (bool, optional) : specifies if colors shall be returned by rgb values (False, default) or rgba (True)
        alpha_value (float, optional) : specifies the alpha for rgba monde, only if rgba mode is enlabled. Defaults to 1.0

    Returns:
        list: palette of colors
    """
    try:
        colormap = eval(f"plt.cm.{cmap_name}")
    except Exception as exc:
        raise ValueError(
            f"The colormap {cmap_name} is not a valid colormap") from exc
    number_of_colors = min(colormap.N, number_of_colors)
    if as_hex:
        return [rgb2hex(colormap(int(x*colormap.N/number_of_colors))) for x in range(number_of_colors)]
    elif as_rgba:
        if alpha_value < 0 or alpha_value > 1:
            alpha_value = 1.0
        colors: list = list()
        for x in range(number_of_colors):
            r, g, b = colormap(int(x*colormap.N/number_of_colors))
            colors.append(f"rgba({r},{g},{b},{alpha_value})")
        return colors
    else:
        return [colormap(int(x*colormap.N/number_of_colors)) for x in range(number_of_colors)]


def get_palette_from_list(data_array: list, cmap_name: str = 'viridis', as_hex: bool = False, as_rgba: bool = False, alpha_value: float = 1.0) -> list:
    """Returns a number_of_colors-sized palette, as a list,
    that one can access with colors[i].

    Args:
        data_array (list): array of data to be normalized
        cmap_name (str, optional): matplotlib cmap to use. Defaults to 'viridis'.
        as_hex (bool, optional): if value shoud be hex or rgba. Defaults to False.
        as_rgba (bool, optional) : specifies if colors shall be returned by rgb values (False, default) or rgba (True)
        alpha_value (float, optional) : specifies the alpha for rgba monde, only if rgba mode is enlabled. Defaults to 1.0

    Returns:
        list: list of colors, one per value
    """
    colormap: list = colorlist.gen_color_normalized(
        cmap=cmap_name, data_arr=[i/max(data_array) for i in data_array])
    if as_hex:
        return [hex2color(color) for color in colormap]
    elif as_rgba:
        if alpha_value < 0 or alpha_value > 1:
            alpha_value = 1.0
        return [f"rgba({r},{g},{b},{alpha_value})" for (r, g, b) in colormap]
    else:
        return colormap
