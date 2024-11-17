import flet as ft

def main(page: ft.Page):
    page.title = "基本的なコントロール"
    
    # 1. テキスト表示
    text1 = ft.Text(
        value="これは基本的なテキストです",
        size=20,            # フォントサイズ
        color="blue",       # 文字色
        weight="bold"       # 太字
    )
    
    # 2. ボタン
    def button_clicked(e):
        # クリック時にテキストを変更
        text1.value = "ボタンがクリックされました！"
        page.update()  # 重要：更新を反映させる
        
    button1 = ft.ElevatedButton(
        text="クリックしてください",
        on_click=button_clicked
    )
    
    # 3. テキスト入力フィールド
    def text_changed(e):
        # 入力内容をテキストに反映
        text1.value = f"あなたが入力した内容: {text_field1.value}"
        page.update()
        
    text_field1 = ft.TextField(
        label="ここに入力してください",
        hint_text="テキストを入力...",
        width=300,
        on_change=text_changed
    )
    
    # コントロールの配置
    page.add(
        text1,
        button1,
        text_field1
    )

ft.app(main)