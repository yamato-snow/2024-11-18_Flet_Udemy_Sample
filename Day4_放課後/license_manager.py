import hashlib
import flet as ft
from datetime import datetime, timedelta
import base64

def generate_license_components(email: str, expiry_date: datetime) -> tuple[str, str]:
    """
    メールアドレスと有効期限からライセンス構成要素を生成します。
    
    Args:
        email (str): ユーザーのメールアドレス
        expiry_date (datetime): 有効期限
    
    Returns:
        tuple[str, str]: (有効期限部分, メールアドレスハッシュ部分)
    """
    # 有効期限をbase64エンコード
    expiry_bytes = expiry_date.isoformat().encode()
    expiry_part = base64.b64encode(expiry_bytes).decode()
    
    # メールアドレスのハッシュを生成
    email_hash = hashlib.sha256(email.encode()).hexdigest()[:16]
    
    return expiry_part, email_hash

def generate_license_key(email: str, expiry_date: datetime) -> str:
    """
    完全なライセンスキーを生成します。
    形式: [有効期限部分]:[メールアドレスハッシュ部分]
    """
    expiry_part, email_hash = generate_license_components(email, expiry_date)
    return f"{expiry_part}:{email_hash}"

def main(page: ft.Page):
    page.title = "ライセンスキー発行システム"
    page.theme_mode = "light"
    page.padding = 40
    page.scroll = ft.ScrollMode.AUTO
    
    # メールアドレス入力
    email_input = ft.TextField(
        label="メールアドレス",
        width=400,
        helper_text="ライセンスを発行するユーザーのメールアドレス"
    )
    
    # 開始日入力
    start_date = ft.TextField(
        label="開始日",
        width=400,
        hint_text="YYYY-MM-DD",
        helper_text="ライセンスの開始日を指定（空欄の場合は本日から）"
    )
    
    # ライセンスタイプの選択
    license_type = ft.Dropdown(
        label="ライセンスタイプ",
        width=400,
        options=[
            ft.dropdown.Option("trial", "トライアル版（30日間）"),
            ft.dropdown.Option("standard", "スタンダード版（1年間）"),
            ft.dropdown.Option("professional", "プロフェッショナル版（無期限）")
        ]
    )
    
    # 結果表示用
    result_display = ft.Text(
        size=16,
        width=400,
        selectable=True,  # テキスト選択可能
    )
    
    def calculate_expiry_date(start: datetime, license_type: str) -> datetime:
        """ライセンスタイプに基づいて有効期限を計算"""
        if license_type == "trial":
            return start + timedelta(days=30)
        elif license_type == "standard":
            return start + timedelta(days=365)
        else:  # professional
            return start + timedelta(days=36500)  # 約100年（実質無期限）
    
    def generate_license(e):
        """ライセンスキーを生成"""
        try:
            # 入力チェック
            if not email_input.value:
                raise ValueError("メールアドレスを入力してください")
            if not license_type.value:
                raise ValueError("ライセンスタイプを選択してください")
            
            # 開始日の処理
            try:
                if start_date.value:
                    start = datetime.strptime(start_date.value, "%Y-%m-%d")
                else:
                    start = datetime.now()
            except ValueError:
                raise ValueError("開始日の形式が正しくありません（YYYY-MM-DD）")
            
            # 有効期限の計算
            expiry = calculate_expiry_date(start, license_type.value)
            
            # ライセンスキーの生成
            license_key = generate_license_key(email_input.value, expiry)
            
            # 検証用の表示（デバッグ目的）
            expiry_part = license_key.split(':')[0]
            decoded_expiry = datetime.fromisoformat(
                base64.b64decode(expiry_part).decode()
            )
            
            # 結果の表示
            result_display.value = f"""
✅ ライセンスキーが生成されました

■ユーザー情報
メールアドレス: {email_input.value}
ライセンスタイプ: {license_type.value}
開始日: {start.strftime('%Y-%m-%d')}
有効期限: {expiry.strftime('%Y-%m-%d')}

■ライセンスキー（ユーザーに提供する情報）
{license_key}

※ユーザーはこのライセンスキーと登録したメールアドレスを使用して認証を行います。

■デバッグ情報
有効期限部分デコード: {decoded_expiry}
"""
            result_display.color = ft.colors.GREEN
            copy_button.visible = True
            
        except ValueError as e:
            result_display.value = f"⚠️ エラー: {str(e)}"
            result_display.color = ft.colors.RED
            copy_button.visible = False
            
        page.update()
    
    def copy_to_clipboard(e):
        """生成された情報をクリップボードにコピー"""
        if result_display.value:
            page.set_clipboard(result_display.value)
            snack = ft.SnackBar(
                content=ft.Text("ライセンス情報をクリップボードにコピーしました"),
                action="OK"
            )
            page.add(snack)
            snack.open = True
            page.update()
    
    # ボタンの作成
    generate_button = ft.ElevatedButton(
        "ライセンスキーを生成",
        on_click=generate_license,
        width=200
    )
    
    copy_button = ft.ElevatedButton(
        "クリップボードにコピー",
        on_click=copy_to_clipboard,
        visible=False
    )
    
    # レイアウトの構築
    page.add(
        ft.Text("ライセンスキー発行システム", size=32, weight="bold"),
        ft.Divider(),
        ft.Container(
            content=ft.Column([
                email_input,
                start_date,
                license_type,
                generate_button,
                ft.Divider(),
                result_display,
                copy_button,
            ]),
            padding=20,
            border_radius=10,
            border=ft.border.all(1, ft.colors.BLUE_200)
        )
    )

ft.app(target=main)