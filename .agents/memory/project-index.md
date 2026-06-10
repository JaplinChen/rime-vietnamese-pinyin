# 專案索引

更新時間：2026-06-08

## 專案摘要

- Rime 越南語拼音輸入方案，來源詞彙在 Excel，透過 Python 腳本產生 `vn.dict.yaml` 與 `vn_han.dict.yaml`。

## 目錄職責

- `make_dict/`：詞彙來源、產生器、驗證腳本與本地 Web UI。
- `make_dict/web/`：詞彙表 Web UI 靜態前端。
- `readme.assets/`：README 圖片資產。
- 專案根目錄：Rime 發布用 schema 與 dict YAML。

## 常用命令

- `python make_dict\excel_to_vndict.py --sync-root`：從 Excel 重新產生並同步根目錄 YAML。
- `python make_dict\verify.py`：檢查 Python 語法、字典格式、根目錄同步與缺來源檔保護。
- `python make_dict\web_ui.py --port 8765`：啟動本地詞彙表 Web UI。

## 驗證策略

- 修改產生器或 Web UI 後，至少跑 `python -m py_compile make_dict\web_ui.py`。
- 修改 Excel 或產生器後，跑 `python make_dict\excel_to_vndict.py --sync-root` 與 `python make_dict\verify.py`。

## 重要規則

- `VietnameseWordList.xlsx` 的 A 欄是越南語，B 欄是中文；C、D、E、F 欄由腳本產生。
- 沒有可靠中文翻譯的越南語詞，B 欄保持空白。
- Web UI 寫入正式 `VietnameseWordList.xlsx` 前會自動備份到 `make_dict/backups/`。
- 不要手動編輯根目錄與 `make_dict/` 內的字典輸出差異；用產生器同步。

## 常用入口

- `make_dict/excel_to_vndict.py`：Excel 到 Rime YAML 的主要產生器。
- `make_dict/web_ui.py`：本地 Web UI 後端與 API。
- `make_dict/web/index.html`：Web UI 主頁。
