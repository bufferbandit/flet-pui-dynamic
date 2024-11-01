from PUI.flet import PUIApp

from flet import app
from flet import colors
from flet import BoxDecoration
from flet import LinearGradient
from flet import alignment
from flet import DecorationImage
from flet import ImageFit
from flet import FontWeight
from flet import Page

from dynamic_pui import Root
from dynamic_pui import dff

from state import state


def inc(e): state.count += 1
def dec(e): state.count -= 1

@PUIApp
def main(page: Page) -> PUIApp:
    page.window.always_on_top_on_top = True
    page.window.width = 430

    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor = colors.TRANSPARENT

    page.decoration = BoxDecoration(
        image=DecorationImage(
            src="https://images.unsplash.com/photo-1547721064-da6cfb341d50",
            fit=ImageFit.COVER,
            opacity=0.2,
        ),
        gradient=LinearGradient(
            colors=[colors.RED, colors.BLUE],
            stops=[0, .6],
            begin=alignment.top_left,
            end=alignment.bottom_right,
        ),
    )


    with Root():
        with dff.Column():
            with dff.Row():
                dff.ElevatedButton("-", on_click=dec)
                dff.Text(f"{state.count}")
                dff.ElevatedButton("+",on_click=inc)
            # /Row
            with dff.Column():
                with dff.Column():
                    dff.Text("-Always visible Text in vbox1", italic=True, weight=FontWeight.BOLD, color="blue", bgcolor="black")
                    dff.Text("-Always visible Text in vbox2", italic=True, weight=FontWeight.BOLD, color="blue", bgcolor="black")
                # /Column
                if state.count >= 0:
                    with dff.Container(bgcolor=colors.AMBER):
                        dff.Text("Text from container")
                    # /Container
                    dff.ProgressBar(value=state.count/100)
                    dff.ProgressBar(value=state.count/100)
                    dff.Text(f"[1.1]Text before {state.count}")
                    dff.ProgressBar(value=state.count/100)
                    dff.ProgressBar(value=state.count/100)
                    dff.ProgressBar(value=state.count/100)
                    dff.ProgressBar(value=state.count/100)
                    dff.ProgressBar(value=state.count/100)
                    dff.Text(f"[1.2]Text before {state.count}")
                # /if
                else:
                    dff.Text(f"[2.1]Text after {state.count}")
                    dff.Text(f"[2.2]Text after {state.count}")
                    dff.Text(f"[2.3]Text after {state.count}")
                    dff.Text(f"[2.4]Text after {state.count}")
                    dff.Text(f"[2.5]Text after {state.count}")
                    dff.Text(f"[2.6]Text after {state.count}")
                    dff.Text(f"[2.7]Text after {state.count}")
                    dff.Text(f"[2.8]Text after {state.count}")
                # /else
            # /Column
        # /Column
    # /Root


if __name__ == "__main__":
    app(target=lambda p:main(p).flet_app(p))