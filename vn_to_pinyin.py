import re
#import sys
#import os
import visen
# visen.clean_tone / Fix Tone position
# visen.remove_tone / Get pure English Character => PinYin key
# visen.get_enter_code / Get the Telex of every vietnamese word

# Other UTF-8 Character
UTF8Char = {
# ử́ ử̃ ự̉  
'[ạ]':'ạ','[ẩ]':'ẩ','[ặ]':'ặ','[ã]':'ã','[ằ]':'ằ','[ắ]':'ắ','[ầ]':'ầ','[à]':'à',
'[ệ]':'ệ','[ẹ]':'ẹ','[é]':'é','[ẻ]':'ẻ','[ề]':'ề','[ế]':'ế',
'[í]':'í','[ị]':'ị','[ì]':'ì','[ỉ]':'ỉ','[ĩ]':'ĩ',
'[ỏ]':'ỏ','[ó]':'ó','[õ]':'õ','[ở]':'ở','[ổ]':'ổ','[ọ]':'ọ','[ỗ]':'ỗ','[ố]':'ố','[ồ]':'ồ','[ớ]':'ớ','[ờ]':'ờ',
'[ự]':'ự','[ụ]':'ụ','[ú]':'ú','[ủ]':'ủ','[ứ]':'ứ','[ử]':'ử',

}


# must use encoding="utf-8" -- 2020-05-22 Japlin Chen
f=open('./WordList.txt','r',encoding="utf-8")
a=open('./vn_pinyin.txt','w',encoding="utf-8")
SourceText = ''
for i in f:
    # Fix Other UTF8 vietnamese character
    ##for UTF8regex, UTF8replace in UTF8Char.items():
    ##    SourceText = re.sub(UTF8regex, UTF8replace, i)
    # Fix Tone position
    Clean_Tone_Text = visen.clean_tone(i)
    # Get pure English Character => PinYin key
    NoToneText = visen.remove_tone(Clean_Tone_Text).strip()
    # Get the Telex of every vietnamese word
    '''
    TelexText = ''
    TempTelexText = ''
    for word in Clean_Tone_Text.split(' '):
        TempTelexText = visen.get_enter_code(word)
        TelexText += TempTelexText + ' '
    '''
    # Save to file
    print(Clean_Tone_Text.strip() + '	' + NoToneText + '	' + '30000', file=a)
    #a.write(i.strip() + ' ' + convert(i) )

a.close()
f.close()

