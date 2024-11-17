import flet as ft
from flet import DragTargetAcceptEvent, border

def main(page: ft.Page):
    page.title = "イベント処理の発展"
    
    # 状態表示用のテキスト
    status_text = ft.Text(size=20)
    input_status_text = ft.Text(size=20)

    # 1. 複数のイベントタイプ
    def handle_pointer_events(e):
        status_text.value = f"ステータス:{e}"

        page.update()
    
    pointer_demo = ft.Container(
        content=ft.Text("ここにマウスを重ねてください"),
        width=300,
        height=100,
        bgcolor=ft.colors.BLUE_100,
        border_radius=5,
        # 複数のイベントを登録
        on_hover=handle_pointer_events,
        on_click=handle_pointer_events,
        on_long_press=handle_pointer_events,
    )

    # 2. フォームの入力検証
    def validate_input(e):
        if not name_field.value:
            name_field.error_text = "名前を入力してください"
        else:
            name_field.error_text = None
            
        if not email_field.value:
            email_field.error_text = "メールアドレスを入力してください"
        elif "@" not in email_field.value:
            email_field.error_text = "有効なメールアドレスを入力してください"
        else:
            email_field.error_text = None
            
        page.update()
    
        # フォームが有効な場合の処理
        if not name_field.error_text and not email_field.error_text:
            input_status_text.value = "入力が有効です！"
            input_status_text.color = ft.colors.GREEN
        else:
            input_status_text.value = "入力を確認してください"
            input_status_text.color = ft.colors.RED
        
    name_field = ft.TextField(
        label="名前",
        width=300,
        on_change=validate_input
    )
    
    email_field = ft.TextField(
        label="メールアドレス",
        width=300,
        on_change=validate_input
    )

    # 3. ドラッグ&ドロップ
    def drag_will_accept(e):
        # ドロップ可能かどうかで枠線の色を変更します
        e.control.content.border = border.all(
            2, ft.colors.BLACK if e.data == "true" else ft.colors.RED
        )
        e.control.update()

    def drag_accept(e: DragTargetAcceptEvent):
        # ドロップされた要素の色を適用します
        src = page.get_control(e.src_id)
        e.control.content.bgcolor = src.content.bgcolor
        e.control.content.border = None
        e.control.update()

    def drag_leave(e):
        # ドラッグが離れたら枠線をクリアします
        e.control.content.border = None
        e.control.update()

    # すべてのコントロールをページに追加
    page.add(
        # 1. ポインターイベントのデモ
        ft.Text("1. ポインターイベント", size=20, weight="bold"),
        pointer_demo,
        status_text,
        ft.Divider(),

        # 2. フォーム検証のデモ
        ft.Text("2. フォーム検証", size=20, weight="bold"),
        name_field,
        email_field,
        input_status_text,
        ft.Divider(),

        # 3. ドラッグ&ドロップのデモ
        ft.Text("3. ドラッグ&ドロップ", size=20, weight="bold"),
        ft.Row(
            [
                ft.Column(
                    # ドラッグ可能なアイテムたち
                    [
                        # Draggableコントロールを使ってドラッグ可能なアイテムを作成
                        ft.Draggable(
                            # group属性でドラッグ可能なグループを指定
                            group="color",
                            # 青色のコンテナ
                            content=ft.Container(
                                width=50,
                                height=50,
                                bgcolor=ft.colors.CYAN,
                                border_radius=5,
                            ),
                            # ドラッグ中の表示をカスタマイズ
                            content_feedback=ft.Container(
                                width=20,
                                height=20,
                                bgcolor=ft.colors.CYAN,
                                border_radius=3,
                            ),
                        ),
                        # ドラッグ可能なアイテムをもう一つ追加
                        ft.Draggable(
                            # group属性でドラッグ可能なグループを指定
                            group="color",
                            # 黄色のコンテナ
                            content=ft.Container(
                                width=50,
                                height=50,
                                bgcolor=ft.colors.YELLOW,
                                border_radius=5,
                            ),
                        ),
                        # もう一つのグループのドラッグ可能なアイテム
                        ft.Draggable(
                            # group属性でドラッグ可能なグループを指定
                            group="color1",
                            # 緑色のコンテナ
                            content=ft.Container(
                                width=50,
                                height=50,
                                bgcolor=ft.colors.GREEN,
                                border_radius=5,
                            ),
                        ),
                    ]
                ),
                ft.Container(
                        width=50,
                ),
                ft.DragTarget(
                    group="color",
                    content=ft.Container(
                        width=50,
                        height=50,
                        bgcolor=ft.colors.BLUE_GREY,
                        border_radius=5,
                    ),
                    on_will_accept=drag_will_accept,
                    on_accept=drag_accept,
                    on_leave=drag_leave,
                ),
            ]
        )
    )

ft.app(main)