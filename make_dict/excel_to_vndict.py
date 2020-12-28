import re
import visen
import openpyxl

# -- Update vn.dict.yaml and vn_han.dict.yaml
vn_file = open('vn.dict.yaml', 'wt',encoding="utf-8")
vnhan_file = open('vn_han.dict.yaml', 'wt',encoding="utf-8")

print('''# Rime dictionary
# encoding: utf-8
---
name: vn
version: "2020.05.29"
sort: original
use_preset_vocabulary: false
max_phrase_length: 10
min_phrase_weight: 100
...
''', file=vn_file)

print('''# Rime dictionary
# encoding: utf-8
---
name: vn_han
version: "2020.05.29"
sort: original
use_preset_vocabulary: false
...
''', file=vnhan_file)

# -- open vietnamese word/phrase source file (Excel file)
wb = openpyxl.load_workbook('VietnameseWordList.xlsx')
sheet = wb.active    # -- open active sheet name Ex: 'Sheet1'

last_text = ''
#last_chinese = ''
now_chinese = ''
rcount = 0
count = 1   
# -- for "A" column 
for column in list(sheet.columns)[0]:

    # -- if A[xxx] have data
    if column.value is not None:
        if count > 1:   # Skip Excel Sheet1 Title
            # -- Fix Tone position
            Clean_Tone_Text = visen.clean_tone(column.value)
            # -- Get pure English Character => PinYin key
            NoToneText = visen.remove_tone(Clean_Tone_Text).strip()
            # -- Get the Telex key for each vietnamese word
            TelexText = ''
            TempTelexText = ''
            for word in Clean_Tone_Text.split(' '):
                # -- 'ươ' telex = 'uwow', now change to 'uow' 
                TempTelexText = visen.get_enter_code(word).replace('uwow', 'uow')
                TelexText += TempTelexText + ' '

            TelexText = TelexText.replace('\n', '').replace('\r', '').strip()

            # -- set Excel C/D/E column value
            sheet.cell(row=count,column=3).value = Clean_Tone_Text
            sheet.cell(row=count,column=4).value = NoToneText
            sheet.cell(row=count,column=5).value = TelexText
            #--爲了方便整理字詞，找到重覆的字詞，並在空白欄位，填入次數
            if last_text == column.value :
                now_chinese = sheet.cell(row=count,column=2).value

                count += 1
                sheet.cell(row=count,column=6).value = count
            else:
                rcount = 0
                last_text = column.value
                #last_chinese = sheet.cell(row=count,column=2).value

            # -- save to 'vn.dict.yaml'
            print(Clean_Tone_Text+' 	'+TelexText+'	50000', file=vn_file)
            print(Clean_Tone_Text+' 	'+NoToneText+'	40000', file=vn_file)

            if sheet.cell(row=count,column=2).value is not None:
                Chinese_Text = sheet.cell(row=count,column=2).value
                Chinese_Text = Chinese_Text.replace(', ','; ').replace('、','; ')
                sheet.cell(row=count,column=2).value = Chinese_Text.strip()

                print(Chinese_Text+'	'+Clean_Tone_Text+'	30000', file=vnhan_file)
                print(Chinese_Text+'	'+TelexText+'	20000', file=vnhan_file)
                print(Chinese_Text+'	'+NoToneText+'	10000', file=vnhan_file)

                #print(str(count)+'	'+column.value+'	'+Chinese_Text+'	'+Clean_Tone_Text+'	'+NoToneText+'	'+TelexText)

    count += 1
# -- Save
wb.save(r'VietnameseWordList.xlsx')




