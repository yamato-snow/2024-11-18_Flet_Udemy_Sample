import flet as ft

def main(page: ft.Page):
    page.title = "レイアウトの基本"
    page.vertical_alignment = ft.MainAxisAlignment.START  # 垂直方向の中央寄せ
    page.bgcolor = ft.colors.BLUE_100  # 背景色
    page.padding = ft.padding.only(0, 100)  # 全方向に余白を設定
    page.magin = ft.margin.only(10, 100, 10)  # 全方向にマージンを設定

    # 横並び（Row）の例
    row = ft.Row(
        controls=[
            ft.ElevatedButton("ボタン1"),
            ft.ElevatedButton("ボタン2"),
            ft.ElevatedButton("ボタン3"),
        ],
        wrap=True,  # 折り返し
    )

    # 横並び（Row）の配置の制御
    row_ali = ft.Row([
            ft.Text("4番目のテキスト"),
            ft.Text("5番目のテキスト"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,  # 中央寄せ
    )
    
    # 縦並び（Column）の例
    column = ft.Column(
        controls=[
            ft.Text("1番目のテキスト"),
            ft.Text("2番目のテキスト"),
            ft.Text("3番目のテキスト"),
            row_ali
        ],
        spacing=20  # 間隔を設定
    )
    
    # レイアウトの組み合わせ
    container = ft.Container(
        content=ft.Column([
            ft.Text("基本的なレイアウト", size=24, weight="bold"),
            row,
            ft.Divider(),  # 区切り線
            column
        ]),
        margin=ft.margin.all(20),  # マージン
        padding=ft.padding.all(20),  # 余白
        bgcolor=ft.colors.BLUE_50,  # 背景色
        border_radius=10  # 角の丸み
    )
    
    page.add(container)

ft.app(main)