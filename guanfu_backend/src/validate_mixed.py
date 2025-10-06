"""確認數量邏輯"""
from typing import Optional, List, Dict, Any
from fastapi.exceptions import RequestValidationError


def validate_mixed(
    # column name
    field_need: str, field_got: str,
    # from user input
    need_input: Optional[int] = None, got_input: Optional[int] = None,
    # from db
    need_db: Optional[int] = None, got_db: Optional[int] = None
) -> None:
    """
    規則：
      - 若只提供一邊，但另一邊在 DB 有值 → 以 DB 值檢核
      - 兩者皆有有效值時，檢查 got <= need
      - 兩者若有提供，皆檢查非負整數（可按需移除）
    """
    errors: List[Dict[str, Any]] = []
    loc_when_input, loc_when_db = ("body",), ("db",)

    # 有效值（input 優先，否則 fallback 到 DB）
    need_eff = need_input if need_input is not None else need_db
    got_eff  = got_input  if got_input  is not None else got_db

    # 來源標記（用於訊息）
    src_need = "input" if need_input is not None else ("db" if need_db is not None else "none")
    src_got  = "input" if got_input  is not None else ("db" if got_db  is not None else "none")

    def add_error(field: str, msg: str, value: Any, from_input: bool, type_: str = "check_error"):
        errors.append({
            "loc": (*(loc_when_input if from_input else loc_when_db), field),
            "msg": msg,
            "type": type_,
            "input": value
        })

    # 基本型別/範圍檢查
    if need_input is not None and need_input < 0:
        add_error(field_need, f"{field_need} must be >= 0.", need_input, from_input=True)
    if got_input is not None and got_input < 0:
        add_error(field_got,  f"{field_got} must be >= 0.", got_input,  from_input=True)

    # 關聯規則：got <= need（當兩者都有有效值時才檢查）
    if need_eff is not None and got_eff is not None:
        if got_eff > need_eff:
            # 優先把錯誤指到「使用者有改動的那個欄位」，否則就指向 DB 來源欄位
            point_input = (got_input is not None) or (need_input is not None)
            msg = (
                f"{field_got} must be less than or equal to {field_need} "
                f"(got={got_eff} from {src_got}, need={need_eff} from {src_need})."
            )
            add_error(field_got, msg, got_eff, from_input=point_input)

    if errors:
        raise RequestValidationError(errors)
