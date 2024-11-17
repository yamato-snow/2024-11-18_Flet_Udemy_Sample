import flet as ft

def main(page: ft.Page):
    page.title = "シンプル電卓"
    
    # 結果表示用のテキストフィールド
    result = ft.TextField(
        value="0", # 初期値
        text_align=ft.TextAlign.RIGHT, # 右寄せ
        read_only=True, # 読み取り専用
        width=320 # 幅
    )
    
    # ボタンクリック時の処理
    def button_clicked(e):
        data = e.control.data # ボタンのデータを取得
        if data == "C":
            result.value = "0"
        elif data == "=":
            try:
                result.value = str(eval(result.value)) # 計算結果を表示
            except:
                result.value = "Error"
        else:
            if result.value == "0":
                result.value = data
            else:
                result.value += data
        page.update()
    
    # ボタンの作成
    def create_button(text, data=None):
        return ft.ElevatedButton(
            text=text, # ボタンのテキスト
            data=data or text, # ボタンのデータ
            width=70, # 幅
            on_click=button_clicked # クリック時の処理
        )
    
    # ボタンの配置
    page.add(
        ft.Container(
            content=ft.Column([
                result, # 結果表示
                # ボタンの配置
                ft.Row([
                    create_button("7"), create_button("8"), create_button("9"), create_button("/")
                ]),
                ft.Row([
                    create_button("4"), create_button("5"), create_button("6"), create_button("*")
                ]),
                ft.Row([
                    create_button("1"), create_button("2"), create_button("3"), create_button("-")
                ]),
                ft.Row([
                    create_button("0"), create_button("."), create_button("="), create_button("+")
                ]),
                ft.Row([
                    create_button("C", "C")
                ])
            ]),
            padding=20 # 余白
        )
    )

ft.app(main)