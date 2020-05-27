# Rime-Vietnamese-Pinyin

## Rime 越南拼音輸入法

`這是一個一言不合就動手修改輪子的自用學習越南語小工具。`

> 2020年了，既然來越南工作一年多了，總要學習下越南語。
> 雖然在工作上，都有助理翻譯會處理。
> 但自己想在電腦上輸入越南字，還是覺得很麻煩。
> 1. 越南字明明都是羅馬拼音，爲何沒有{**無廣告**}的越南拼音輸入法？
> 2. 爲何打幾個越南字，還要背鍵盤位置，學習 VNI、TELEX、VIQR 輸入法？
> 3. 還有超級難用的 Windows 內建的越南輸入法。
> 4. 常常遇到 只有拼音字元, 沒有音調的越南字...好吧, 據說越南人都看得懂, 我看不懂啊, 大哥...
>
> PS. 現在越南人平時幾乎沒在使用漢喃字 
>


## 安裝：

### Step 1. 安裝輸入法引擎：[Rime 小狼毫輸入法](https://rime.im/)

   爲什麼選擇 Rime ? **1.無廣告 2.免費 3.可以修改**

   請按照官方網站的說明安裝吧.

### Step 2. 下載 [rime-vietnamese-pinyin](https://github.com/JaplinChen/rime-vietnamese-pinyin) 及解壓縮之後, 

   將 **4 個 .yaml copy** 到 **[Rime 的用戶文件夾]** 內, 如下圖.

   ![打開 Rime 用戶資料夾](Rime 用戶資料夾.png)

   Copy 好之後, 按 **[重新部署]** 即可.

### 如何新增詞匯整理到 Rime: 

1. Pinyin 字詞
   1. 將需要增加的越南字詞, 放到 WordList.txt
   2. 可使用 [vn_to_telex.py](vn_to_telex.py) 將 WordList.txt 的越南字詞轉成 vn_pinyin.txt 越南字詞+pinyin
   3. 再將 vn_pinyin.txt 的內容 copy 到 [vn.dict.yaml](vn.dict.yaml) 檔案最後面
   4. Rime 重新部署

2.越中字詞

   1. 網路上可以蒐集到很多越中的字詞教學, 可以先整理在 Excel
   2. 格式可以參考 [越南語基本詞匯3600.xlsx](越南語基本詞匯3600.xlsx)
   3. 再將相關內容 copy 到 [vn_han.dict.yaml](vn_han.dict.yaml) 檔案最後面. 格式如: A1=中文 B1=越南文 C1=權值
   4. Rime 重新部署

### 現有越南詞匯參考：

1. 越南詞匯來源：
   1. [越南常用字 7184 字](https://gist.github.com/hieuthi/1f5d80fca871f3642f61f7e3de883f3a) 保留 Telex, 並增加拼音
   2. 網路上找到+整理的 [越南語基本詞匯3600.xlsx](越南語基本詞匯3600.xlsx)
2. 修改自 [rime-vietnamese](https://github.com/gkovacs/rime-vietnamese)
3. 越南字庫基礎：[越南常用字 7184 字](https://gist.github.com/hieuthi/1f5d80fca871f3642f61f7e3de883f3a)
4. [漢喃字輸入法](https://chinese.com.vn/phan-mem-viet-chu-han-nom-weasel-hannom-mien-phi.html)

