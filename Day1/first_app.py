import flet as ft

def main(page: ft.Page):
    # ページのタイトルを設定
    page.title = "はじめてのFletアプリ"
    
    # テキストを追加
    page.add(ft.Text("こんにちは、Flet!"))

ft.app(main)