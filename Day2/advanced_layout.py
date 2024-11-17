import flet as ft

def main(page: ft.Page):
    page.title = "高度なレイアウト"
    page.padding = 50  # ここでページ全体の余白を設定します

    # 1. Containerの高度な使い方
    styled_container = ft.Container(
        content=ft.Text("スタイル付きコンテナ"),
        width=200,
        height=100,
        bgcolor=ft.colors.BLUE_100,
        border_radius=10,        # 角の丸み
        padding=15,              # 内側の余白
        margin=10,               # 外側の余白
        ink=True,               # クリックエフェクト
        on_click=lambda e: print("クリック!"),
    )

    # 2. Stackを使った重ね合わせ
    stack = ft.Stack([
        ft.Container(
            width=100,
            height=100,
            bgcolor=ft.colors.RED_100,
        ),
        ft.Container(
            width=50,
            height=50,
            bgcolor=ft.colors.GREEN_100,
            left=25,            # 左からの位置
            top=25,             # 上からの位置
        ),
    ])

    # 3. GridViewを使ったグリッドレイアウト
    grid = ft.GridView(
        expand=1,
        runs_count=3,          # 列数を3に設定
        max_extent=150,        # 各要素の最大幅
        spacing=10,            # 要素間の間隔
        run_spacing=10,        # 行間の間隔
        controls=[
            ft.Container(
                bgcolor=ft.colors.AMBER_100,
                height=100,
                alignment=ft.alignment.center,
                content=ft.Text(f"Item {i}")
            ) for i in range(9)
        ]
    )

    page.add(
        ft.Text("1. Container(スタイル付きコンテナ)", size=20, weight="bold"),
        styled_container,
        ft.Divider(),
        ft.Text("2. Stack（重ね合わせ）", size=20, weight="bold"),
        stack,
        ft.Divider(),
        ft.Text("3. GridView（グリッドレイアウト）", size=20, weight="bold"),
        grid
    )

ft.app(main)