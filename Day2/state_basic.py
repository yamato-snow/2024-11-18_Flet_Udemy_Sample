import flet as ft

def main(page: ft.Page):
    page.title = "状態管理の基礎"
    page.padding = 50

    # 1. シンプルな状態管理
    count = 0  # これが管理する状態です
    
    # 状態を表示するテキスト
    count_text = ft.Text(
        str(count),
        size=30,
        weight="bold"
    )

    def update_counter(e, delta):
        nonlocal count  # 外部の変数を更新するために必要
        count += delta
        count_text.value = str(count)  # 表示を更新
        page.update()  # 重要：画面の更新を忘れずに

    # 増減用のボタン
    minus_button = ft.ElevatedButton("-1", on_click=lambda e: update_counter(e, -1))
    plus_button = ft.ElevatedButton("+1", on_click=lambda e: update_counter(e, 1))
    
    # カウンターのUI
    counter_row = ft.Row(
        controls=[
            minus_button,
            count_text,
            plus_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # 2. 複数の状態を持つコンポーネント
    class TogglePanel(ft.Container):
        def __init__(self, title: str):
            super().__init__()
            # 状態の初期化
            self.is_expanded = False
            self.title = title
            
            # UI要素の作成
            self.title_text = ft.Text(title, size=20)
            self.content = ft.Column(
                controls=[
                    ft.Text("詳細な内容がここに表示されます。"),
                    ft.Text("この部分は折りたたむことができます。")
                ],
                visible=False  # 初期状態は非表示
            )
            
            # クリックイベントの設定
            self.on_click = self.toggle
            
            # 見た目の設定
            self.padding = 10
            self.bgcolor = ft.colors.BLUE_50
            self.border_radius = 5
            self.content = ft.Column([self.title_text, self.content])
        
        def toggle(self, e):
            # 状態の切り替え
            self.is_expanded = not self.is_expanded
            self.content.controls[1].visible = self.is_expanded
            self.bgcolor = ft.colors.BLUE_100 if self.is_expanded else ft.colors.BLUE_50
            self.update()

    # パネルの作成と配置
    panels = ft.Column(
        controls=[
            TogglePanel("セクション1"),
            TogglePanel("セクション2"),
            TogglePanel("セクション3"),
        ],
        spacing=10
    )

    # ページへの追加
    page.add(
        ft.Text("1. シンプルな状態管理", size=24, weight="bold"),
        counter_row,
        ft.Divider(),
        ft.Text("2. 複数の状態を持つコンポーネント", size=24, weight="bold"),
        panels
    )

ft.app(main)