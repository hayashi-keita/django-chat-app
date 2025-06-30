from django import template
# カスタムテンプレートフィルターを登録するための「レジストリオブジェクト」を作成
register = template.Library()
# 関数を「テンプレートフィルター」として登録するデコレーター
@register.filter
# 辞書 d から key に対応する値を取得
def dict_get(d, key):
    # 指定した key が辞書に存在しない場合は デフォルトで 0 を返す 
    return d.get(key, 0)
