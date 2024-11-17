import hashlib
import flet as ft
from datetime import datetime
import base64

def verify_license_key(email: str, license_key: str) -> tuple[bool, str]:
    """
    ライセンスキーを検証します。
    
    Args:
        email (str): ユーザーのメールアドレス
        license_key (str): 検証するライセンスキー
        
    Returns:
        tuple[bool, str]: (検証結果, メッセージ)
    """
    try:
        # ライセンスキーを分解
        expiry_part, email_hash = license_key.split(':')
        
        # 有効期限をデコード
        expiry_bytes = base64.b64decode(expiry_part)
        expiry_date = datetime.fromisoformat(expiry_bytes.decode())
        
        # 現在時刻との比較
        now = datetime.now()
        if expiry_date < now:
            days_expired = (now - expiry_date).days
            return False, f"ライセンスは{days_expired}日前に期限切れです"
        
        # メールアドレスのハッシュを検証
        correct_hash = hashlib.sha256(email.encode()).hexdigest()[:16]
        if email_hash != correct_hash:
            return False, "メールアドレスが一致しません"
        
        # 有効期限までの日数を計算
        days_remaining = (expiry_date - now).days
        return True, f"ライセンス有効 ✓ （残り{days_remaining}日）"
        
    except ValueError:
        return False, "ライセンスキーの形式が不正です"
    except Exception as e:
        return False, f"検証エラー: {str(e)}"

def main(page: ft.Page):
    page.title = "ライセンス認証システム"
    page.theme_mode = "light"
    page.padding = 40
    page.scroll = ft.ScrollMode.AUTO
    
    # 入力フィールド
    email_input = ft.TextField(
        label="メールアドレス",
        width=400,
        helper_text="登録したメールアドレスを入力してください"
    )
    
    license_input = ft.TextField(
        label="ライセンスキー",
        width=400,
        helper_text="提供されたライセンスキーを入力してください"
    )
    
    # 結果表示用
    result_display = ft.Text(
        size=16,
        width=400,
        selectable=True
    )
    
    def verify_license(e):
        """ライセンスキーを検証"""
        try:
            # 入力チェック
            if not email_input.value or not license_input.value:
                raise ValueError("メールアドレスとライセンスキーを入力してください")
            
            # ライセンスキーの検証
            is_valid, message = verify_license_key(
                email_input.value.strip(),
                license_input.value.strip()
            )
            
            if is_valid:
                result_display.value = f"""
✅ 認証成功

■認証結果
{message}

■認証情報
メールアドレス: {email_input.value}
ライセンスキー: {license_input.value}

※このアプリケーションの利用が可能になりました。
"""
            else:
                result_display.value = f"""
⚠️ 認証失敗

■エラー内容
{message}

■入力情報
メールアドレス: {email_input.value}
ライセンスキー: {license_input.value}

※正しい情報を入力してください。
"""
            
            result_display.color = ft.colors.GREEN if is_valid else ft.colors.RED
            
        except ValueError as e:
            result_display.value = f"⚠️ エラー: {str(e)}"
            result_display.color = ft.colors.RED
        
        page.update()
    
    # 検証ボタン
    verify_button = ft.ElevatedButton(
        "ライセンスを認証",
        on_click=verify_license,
        width=200
    )
    
    # レイアウトの構築
    page.add(
        ft.Text("ライセンス認証システム", size=32, weight="bold"),
        ft.Divider(),
        ft.Container(
            content=ft.Column([
                email_input,
                license_input,
                verify_button,
                ft.Divider(),
                result_display,
            ]),
            padding=20,
            border_radius=10,
            border=ft.border.all(1, ft.colors.BLUE_200)
        )
    )

ft.app(target=main)