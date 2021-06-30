digit = {'一': 1, '二': 2, '兩': 2,'三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
        '1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}
power = {'十':10,'百':100,'千':1000,'萬':10000}
all = { '一': 1, '二': 2, '兩': 2,'三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
        '1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,
        '十':10,'百':100,'千':1000,'萬':10000}

def _trans(s):
    num = 0
    if s:
        idx_q, idx_b, idx_s = s.find('千'), s.find('百'), s.find('十')
        if idx_q != -1:
            num  = digit[s[idx_q - 1:idx_q]] * 1000
        if idx_b != -1:
            num  += digit[s[idx_b - 1:idx_b]] * 100
        if idx_s != -1:
            # 十前忽略一的處理
            num  += (digit.get(s[idx_s - 1:idx_s], 1)) * 10
        if s[-1] in digit:
            num  += digit[s[-1]]
    return num

def trans(chn, default=1):
    chn=find_num_part(chn)
    if(chn==""):
        return default
    chn = chn.replace('零', '')
    idx_y, idx_w = chn.rfind('億'), chn.rfind('萬')
    if idx_w < idx_y:
        idx_w = -1
    num_y, num_w = 100000000, 10000
    if idx_y != -1 and idx_w != -1:
        return trans(chn[:idx_y]) * num_y + _trans(chn[idx_y + 1:idx_w]) * num_w + _trans(chn[idx_w + 1:])
    elif idx_y != -1:
        return trans(chn[:idx_y]) * num_y + _trans(chn[idx_y + 1:])
    elif idx_w != -1:
        return _trans(chn[:idx_w]) * num_w + _trans(chn[idx_w + 1:])
    return _trans(chn)

def find_num_part(sentence):
    bo=False
    num = ""
    for i in range(len(sentence)):
        if sentence[len(sentence)-1-i] in all.keys():
            bo=True
            num = sentence[len(sentence)-1-i] + num
        else:
            if bo:
                break
    return num
