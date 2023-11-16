import qdarktheme

PRIMARY_COLOR = '#1e81b0'
DARKER_PRIMARY_COLOR = '#16658a'
DARKEST_PRIMARY_COLOR = '#115270'
# Sizing
BIG_FONT_SIZE = 40
MEDIUM_FONT_SIZE = 18
SMALL_FONT_SIZE = 12
TEXT_MARGIN = 0.5
MINIMUM_WIDTH = 500
MINIMUM_HEIGHT = 500


qss = f"""
    QPushButton[cssClass="specialButton"] {{
        color: #fff;
        background: {PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"]:hover {{
        color: #fff;
        background: {DARKER_PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"]:pressed {{
        color: #fff;
        background: {DARKEST_PRIMARY_COLOR};
    }}
"""


def setupTheme():
    qdarktheme.setup_theme(
        theme='light',
        corner_shape='rounded',
        custom_colors={
            "[dark]": {
                "primary": f"{PRIMARY_COLOR}",
            },
            "[light]": {
                "primary": f"{PRIMARY_COLOR}",
            },
        },
        additional_qss=qss

    )
