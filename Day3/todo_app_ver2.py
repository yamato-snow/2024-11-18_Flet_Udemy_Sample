import flet as ft

class Task(ft.Column):
    """
    個々のタスクを表現するクラス
    ft.Columnを継承し、1つのToDo項目として表示される
    """
    def __init__(self, task_name, task_status_change, task_delete):
        # 親クラス(ft.Column)の初期化
        super().__init__()
        # タスクの状態を管理する変数の初期化
        self.completed = False  # タスクの完了状態（初期値: 未完了）
        self.task_name = task_name  # タスク名を保存
        self.task_status_change = task_status_change  # 状態変更時のコールバック関数
        self.task_delete = task_delete  # 削除時のコールバック関数

        # タスクの表示用チェックボックスを作成
        self.display_task = ft.Checkbox(
            value=False,  # チェックボックスの初期状態（未チェック）
            label=self.task_name,  # チェックボックスの横に表示されるテキスト
            on_change=self.status_changed  # チェックボックスの状態が変更された時の処理
        )
        # タスク名編集用のテキストフィールド
        self.edit_name = ft.TextField(expand=1)

        # タスク表示用のビューを作成（通常時の表示）
        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # 要素を両端に配置
            vertical_alignment=ft.CrossAxisAlignment.CENTER,  # 垂直方向に中央揃え
            controls=[
                self.display_task,  # チェックボックスを配置
                ft.Row(
                    spacing=0,
                    controls=[
                        # 編集ボタン
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="ToDoを編集",
                            on_click=self.edit_clicked,
                        ),
                        # 削除ボタン
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="ToDoを削除",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        # タスク編集用のビューを作成（編集時の表示）
        self.edit_view = ft.Row(
            visible=False,  # 初期状態では非表示
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,  # 編集用テキストフィールド
                # 保存ボタン
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="ToDoを更新",
                    on_click=self.save_clicked,
                ),
            ],
        )
        # 表示ビューと編集ビューをコントロールリストに追加
        self.controls = [self.display_view, self.edit_view]

    def edit_clicked(self, e):
        """編集ボタンがクリックされた時の処理"""
        self.edit_name.value = self.display_task.label  # 現在のタスク名をテキストフィールドにセット
        self.display_view.visible = False  # 通常表示を非表示
        self.edit_view.visible = True  # 編集表示を表示
        self.update()  # UI更新

    def save_clicked(self, e):
        """保存ボタンがクリックされた時の処理"""
        self.display_task.label = self.edit_name.value  # 編集した内容を保存
        self.display_view.visible = True  # 通常表示を表示
        self.edit_view.visible = False  # 編集表示を非表示
        self.update()  # UI更新

    def status_changed(self, e):
        """チェックボックスの状態が変更された時の処理"""
        self.completed = self.display_task.value  # 完了状態を更新
        self.task_status_change(self)  # コールバック関数を呼び出し

    def delete_clicked(self, e):
        """削除ボタンがクリックされた時の処理"""
        self.task_delete(self)  # 削除用コールバック関数を呼び出し


class TodoApp(ft.Column):
    """
    ToDoアプリケーション全体を管理するメインクラス
    ft.Columnを継承し、アプリケーションのメインビューとなる
    """
    def __init__(self):
        super().__init__()  # 親クラスの初期化

        # ブレークポイントの定義
        self.BREAKPOINTS = {
            "MOBILE": 600,    # 600px以下をモバイル
            "TABLET": 1024    # 1024px以下をタブレット
        }
        
        # 新規タスク入力用のテキストフィールド
        self.new_task = ft.TextField(
            hint_text="何をする必要がありますか？",  # プレースホルダーテキスト
            on_submit=self.add_clicked,  # Enterキーが押された時の処理
            expand=True  # 利用可能な幅いっぱいに広がる
        )
        # タスクリストを表示するための列
        self.tasks = ft.Column()

        # フィルタータブの設定
        self.filter = ft.Tabs(
            scrollable=False,  # スクロール不可
            selected_index=0,  # 初期選択タブ（すべて）
            on_change=self.tabs_changed,  # タブ変更時の処理
            tabs=[
                ft.Tab(
                    text="すべて",
                    icon=ft.icons.LIST_ALT,
                ),
                ft.Tab(
                    text="実行中",
                    icon=ft.icons.PENDING_ACTIONS,
                ),
                ft.Tab(
                    text="完了",
                    icon=ft.icons.TASK_ALT,
                ),
            ],
        )

        # 残タスク数の表示
        self.items_left = ft.Text("0 個の実行中の項目が残っています")

        # UIの構築（レスポンシブ対応）
        self._build_ui()
    
    def did_mount(self):
        """コンポーネントがマウントされた後に呼ばれる"""
        self.page.on_resized = self._handle_resize
        self._update_layout_width()
        self.update()

    def _update_layout_width(self):
        """画面幅に応じてレイアウト幅を更新"""
        window_width = self.page.window.width
        
        if window_width <= self.BREAKPOINTS["MOBILE"]:
            # モバイル: 画面幅の95%
            self.width = window_width * 0.95
            self.padding = 10
        elif window_width <= self.BREAKPOINTS["TABLET"]:
            # タブレット: 画面幅の85%または800px
            self.width = min(800, window_width * 0.85)
            self.padding = 15
        else:
            # デスクトップ: 画面幅の70%または1000px
            self.width = min(1000, window_width * 0.70)
            self.padding = 20

    def _handle_resize(self, e):
        """リサイズイベントの処理"""
        self._update_layout_width()
        self.update()

    def _build_ui(self):
        """UIの構築"""
        self.controls = [
            # ヘッダー部分
            ft.Row(
                [
                    ft.Text(
                        value="ToDo一覧",
                        theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM # テーマスタイルの設定
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER, # 中央揃え
            ),
            # 新規タスク入力部分
            ft.Container(
                content=ft.Row(
                    controls=[
                        self.new_task, # 新規タスク入力フィールド
                        ft.FloatingActionButton(  # 追加ボタン
                            icon=ft.icons.ADD, # アイコン
                            on_click=self.add_clicked # クリック時の処理
                        ),
                    ],
                ),
                padding=ft.padding.symmetric(vertical=10)# 上下に10pxの余白
            ),
            # タスクリスト部分
            ft.Container(
                content=ft.Column(
                    spacing=25,
                    controls=[
                        self.filter,  # フィルタータブ
                        self.tasks,   # タスクリスト
                        ft.Row(       # フッター部分
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                self.items_left,  # 残タスク数表示
                                ft.OutlinedButton(  # 完了タスク一括削除ボタン
                                    text="完了項目を削除",
                                    on_click=self.clear_clicked
                                ),
                            ],
                        ),
                    ],
                ),
                padding=10
            ),
        ]

    def add_clicked(self, e):
        """新規タスク追加時の処理"""
        if self.new_task.value:  # 入力値が存在する場合
            # 新しいタスクを作成
            task = Task(
                self.new_task.value, # タスク名
                self.task_status_change,    # タスクの状態変更時の処理
                self.task_delete # タスクの削除時の処理
            )
            self.tasks.controls.append(task)  # タスクリストに追加
            self.new_task.value = ""  # 入力フィールドをクリア
            self.new_task.focus()  # 入力フィールドにフォーカス
            self.update()  # UI更新

    def task_status_change(self, task):
        """タスクの状態が変更された時の処理"""
        self.update()  # UI更新

    def task_delete(self, task):
        """タスクが削除された時の処理"""
        self.tasks.controls.remove(task)  # タスクリストから削除
        self.update()  # UI更新

    def tabs_changed(self, e):
        """フィルタータブが変更された時の処理"""
        self.update()  # UI更新

    def clear_clicked(self, e):
        """完了タスクの一括削除処理"""
        for task in self.tasks.controls[:]:  # タスクリストのコピーでループ
            if task.completed:  # 完了状態のタスクのみ
                self.task_delete(task)  # 削除

    def before_update(self):
        """UI更新前の処理（タスクの表示制御とカウント更新）"""
        status = self.filter.tabs[self.filter.selected_index].text  # 現在選択中のタブ
        count = 0  # 未完了タスクのカウンター
        # 各タスクの表示/非表示を設定
        for task in self.tasks.controls:
            task.visible = (
                status == "すべて"  # すべてのタスクを表示
                or (status == "実行中" and task.completed == False)  # 未完了タスクのみ表示
                or (status == "完了" and task.completed)  # 完了タスクのみ表示
            )
            if not task.completed:
                count += 1  # 未完了タスクをカウント
        # 残タスク数の表示を更新
        self.items_left.value = f"{count} 個の実行中の項目が残っています"


def main(page: ft.Page):
    """
    アプリケーションのメイン関数
    ページの設定と初期化を行う
    """
    page.title = "ToDoアプリ"  # ウィンドウタイトルの設定
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # 水平方向の中央揃え
    page.scroll = ft.ScrollMode.ADAPTIVE  # スクロールモードを適応的に設定

    # テーマカラーの設定
    page.theme = ft.Theme(
        color_scheme_seed="blue",  # ベースカラーの設定
        visual_density=ft.VisualDensity.COMFORTABLE,  # 余白の設定
    )
    
    # ダークモード切り替えボタンの作成
    def theme_changed(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        page.update()
    
    theme_button = ft.IconButton(
        icon=ft.icons.DARK_MODE,
        tooltip="テーマ切り替え",
        on_click=theme_changed,
    )
    
    # アプリバーの追加
    page.appbar = ft.AppBar(
        title=ft.Text("ToDoアプリ"),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[theme_button],
    )

    # ToDoアプリのインスタンスを作成してページに追加
    page.add(TodoApp())

# アプリケーションの実行
ft.app(main)