import flet as ft

def main(page: ft.Page):

    c1 = ft.Container(
        ft.Text("Hello!", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
        alignment=ft.alignment.center,
        width=200,
        height=200,
        bgcolor=ft.colors.GREEN,
    )
    c2 = ft.Container(
        ft.Text("Bye!", size=50),
        alignment=ft.alignment.center,
        width=200,
        height=200,
        bgcolor=ft.colors.YELLOW,
    )
    anime = ft.AnimatedSwitcher(
        c1,
        transition=ft.AnimatedSwitcherTransition.SCALE,
        duration=500,
        reverse_duration=100,
        switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
        switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
    )

    def animate(e):
        anime.content = c2 if anime.content == c1 else c1
        anime.update()

    page.add(
        anime,
        ft.ElevatedButton("Animate!", on_click=animate),
    )

ft.app(main)