import re
#import sys
#import os
import visen
# visen.clean_tone / Fix Tone position
# visen.remove_tone / Get pure English Character => PinYin key
# visen.get_enter_code / Get the Telex of every vietnamese word

# Other UTF-8 Character
UTF8Char = {

u'[à]':u'à',u'[á]':u'á',u'[ã]':u'ã',u'[ả]':u'ả',u'[ạ]':u'ạ',
u'[è]':u'è',u'[é]':u'é',u'[ẽ]':u'ẽ',u'[ẻ]':u'ẻ',u'[ẹ]':u'ẹ',
u'[ì]':u'ì',u'[í]':u'í',u'[ĩ]':u'ĩ',u'[ỉ]':u'ỉ',u'[ị]':u'ị',
u'[ò]':u'ò',u'[ó]':u'ó',u'[õ]':u'õ',u'[ỏ]':u'ỏ',u'[ọ]':u'ọ',
u'[ù]':u'ù',u'[ú]':u'ú',u'[ũ]':u'ũ',u'[ủ]':u'ủ',u'[ụ]':u'ụ',
u'[ầ]':u'ầ',u'[ấ]':u'ấ',u'[ẫ]':u'ẫ',u'[ẩ]':u'ẩ',u'[ậ]':u'ậ',
u'[ề]':u'ề',u'[ệ]':u'ệ',u'[ế]':'ế',
u'[ồ]':u'ồ',u'[ố]':u'ố',u'[ỗ]':u'ỗ',u'[ổ]':u'ổ',u'[ộ]':u'ộ',
u'[ằ]':u'ằ',u'[ắ]':u'ắ',u'[ẵ]':u'ẵ',u'[ẳ]':u'ẳ',u'[ặ]':u'ặ',
u'[ờ]':u'ờ',u'[ớ]':u'ớ',u'[ỡ]':u'ỡ',u'[ở]':u'ở',u'[ợ]':u'ợ',
u'[ứ]':u'ứ',u'[ữ]':u'ữ',u'[ử]':u'ử',u'[ự]':u'ự',
u'[ỹ]':u'ỹ',u'[ỷ]':u'ỷ',u'[ỵ]':u'ỵ',u'[ý]':u'ý',u'[ỳ]':u'ỳ',

}


# must use encoding="utf-8" -- 2020-05-22 Japlin Chen
f=open('./WordList.txt','r',encoding="utf-8")
a=open('./vn_telex.txt','w',encoding="utf-8")
SourceText = ''
for i in f:
    # Fix Other UTF8 vietnamese character
    ##for UTF8regex, UTF8replace in UTF8Char.items():
    ##    SourceText = re.sub(UTF8regex, UTF8replace, i)
    # Fix Tone position
    Clean_Tone_Text = visen.clean_tone(i)

    # Get the Telex of every vietnamese word
    TelexText = ''
    TempTelexText = ''
    for word in Clean_Tone_Text.split(' '):
        TempTelexText = visen.get_enter_code(word).replace('uwow', 'uow')
        TelexText += TempTelexText + ' '

    TelexText = TelexText.replace('\n', '').replace('\r', '')
    # Save to file
    print(Clean_Tone_Text.strip() + '	' + TelexText.strip() + '	' + '20000', file=a)
    #a.write(i.strip() + ' ' + convert(i) )

a.close()
f.close()

