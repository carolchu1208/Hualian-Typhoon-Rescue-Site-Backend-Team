#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新人力資源記錄
根據 out.json 中的記錄，逐一發送 PATCH API 請求來更新資料庫

API 格式: PATCH https://guangfu250923.pttapp.cc/human_resources/{id}

使用方法:
    python update_records.py                # 互動模式，會詢問確認
    python update_records.py --auto-confirm # 自動確認模式，直接執行
    python update_records.py -y             # 同上，簡短參數

參數說明:
    --auto-confirm, -y    自動確認，不需要互動輸入

依賴套件:
    pip install requests

功能特點:
    - 安全確認: 執行前會顯示摘要並要求確認（除非使用 --auto-confirm）
    - 錯誤處理: 包含完整的錯誤處理和日誌記錄
    - 請求限制: 每次請求間隔 1 秒，避免過於頻繁的 API 調用
    - 詳細日誌: 顯示每筆記錄的更新狀態和結果摘要
    - 容錯機制: 單筆記錄失敗不會影響其他記錄的更新

注意事項:
    - 確保 out.json 文件存在且格式正確
    - 確認網路連線正常，能夠訪問 API 端點
    - 腳本會自動移除請求主體中的 id 欄位
"""

import json
import requests
import time
from typing import List, Dict, Any
import sys
import argparse

# API 設定
BASE_URL = "https://guangfu250923.pttapp.cc/human_resources"
REQUEST_DELAY = 1  # 每次請求間隔秒數，避免過於頻繁的請求

def load_records(file_path: str) -> List[Dict[str, Any]]:
    """讀取 out.json 文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            records = json.load(f)
        print(f"✅ 成功讀取 {len(records)} 筆記錄")
        return records
    except FileNotFoundError:
        print(f"❌ 找不到文件: {file_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ JSON 格式錯誤: {e}")
        sys.exit(1)

def prepare_patch_data(record: Dict[str, Any]) -> Dict[str, Any]:
    """準備 PATCH 請求的資料，移除 id 欄位"""
    patch_data = record.copy()
    patch_data.pop('id', None)  # 移除 id，因為它不應該在請求主體中
    return patch_data

def update_record(record: Dict[str, Any]) -> bool:
    """發送 PATCH 請求更新單筆記錄"""
    record_id = record.get('id')
    if not record_id:
        print(f"❌ 記錄缺少 ID: {record}")
        return False

    url = f"{BASE_URL}/{record_id}"
    patch_data = prepare_patch_data(record)

    try:
        print(f"🔄 更新記錄: {record_id} ({record.get('org', 'N/A')})")

        # 發送 PATCH 請求
        response = requests.patch(
            url,
            json=patch_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )

        if response.status_code == 200:
            print(f"✅ 成功更新: {record_id}")
            return True
        else:
            print(f"❌ 更新失敗: {record_id}")
            print(f"   狀態碼: {response.status_code}")
            print(f"   回應: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ 網路錯誤: {record_id} - {e}")
        return False

def show_summary(records: List[Dict[str, Any]]):
    """顯示將要更新的記錄摘要"""
    print("\n📊 準備更新的記錄摘要：")
    print("-" * 60)
    for i, record in enumerate(records, 1):
        print(f"{i:2d}. {record.get('id', 'N/A'):<40} | {record.get('org', 'N/A')}")
    print("-" * 60)
    print(f"總共 {len(records)} 筆記錄")

def confirm_update(auto_confirm: bool = False) -> bool:
    """確認是否執行更新"""
    if auto_confirm:
        print("\n✅ 自動確認模式，直接執行更新")
        return True

    while True:
        answer = input("\n❓ 確定要執行批量更新嗎？(y/n): ").strip().lower()
        if answer in ['y', 'yes', '是']:
            return True
        elif answer in ['n', 'no', '否']:
            return False
        else:
            print("請輸入 y 或 n")

def main():
    """主函數"""
    # 解析命令行參數
    parser = argparse.ArgumentParser(description='批量更新人力資源記錄')
    parser.add_argument('--auto-confirm', '-y', action='store_true',
                       help='自動確認，不需要互動輸入')
    args = parser.parse_args()

    input_file = "out.json"

    print("🚀 人力資源記錄批量更新工具")
    print(f"📂 讀取文件: {input_file}")
    print(f"🌐 API 端點: {BASE_URL}")

    # 讀取記錄
    records = load_records(input_file)

    # 顯示摘要
    show_summary(records)

    # 確認執行
    if not confirm_update(args.auto_confirm):
        print("🛑 取消更新操作")
        return

    # 執行批量更新
    print(f"\n🔄 開始批量更新 (每次請求間隔 {REQUEST_DELAY} 秒)...")

    success_count = 0
    fail_count = 0

    for i, record in enumerate(records, 1):
        print(f"\n[{i}/{len(records)}]", end=" ")

        if update_record(record):
            success_count += 1
        else:
            fail_count += 1

        # 在請求之間添加延遲
        if i < len(records):
            time.sleep(REQUEST_DELAY)

    # 顯示最終結果
    print("\n" + "="*60)
    print("📊 更新結果摘要：")
    print(f"✅ 成功: {success_count} 筆")
    print(f"❌ 失敗: {fail_count} 筆")
    print(f"📊 總計: {len(records)} 筆")

    if fail_count > 0:
        print("\n⚠️  有部分記錄更新失敗，請檢查上方的錯誤訊息")
    else:
        print("\n🎉 所有記錄都已成功更新！")

if __name__ == "__main__":
    main()