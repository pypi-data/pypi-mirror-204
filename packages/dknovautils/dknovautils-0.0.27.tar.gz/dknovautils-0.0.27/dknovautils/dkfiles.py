
from dknovautils.commons import *


_debug = False


class DkPyFiles(object):

    @staticmethod
    def f_remove_comments_v1(py: str) -> str:
        # 可以在文件中添加如下字符串阻止移除多行注释
        KEEP = '__keep_quotes__'

        assert py is not None, 'err5242'

        # 注意ln已经有末尾的回车符 最好替换成\n方便后续处理 rstrip 将去掉末尾的回车符

        lns = '\n'.join(ln.rstrip() for ln in py.splitlines())

        keep_quotes = KEEP in lns

        if _debug:
            print(lns)
            print("=====")

        fr_single_a = r'\n\s*#.*'
        pattern = re.compile(fr_single_a)
        lns = re.sub(pattern, "", lns)  # 查找匹配 然后替换

        '''
        是匹配单引号还是匹配双引号？
        个人写注释习惯用得最多的是单引号。所以还是删除单引号好了。


        '''

        # 首行开始的文本不会被替换掉，因为前方没有回车符
        # fr_multi = r'(?s)""".*?"""'
        fr_multi = r"(?s)'''.*?'''"
        pattern = re.compile(fr_multi)
        if not keep_quotes:
            lns = re.sub(pattern, "", lns)  # 查找匹配 然后替换

        _removeAstSentence = True
        if _removeAstSentence:
            fr_single_a = r'\n\s*assert\s.+'
            pattern = re.compile(fr_single_a)
            lns = re.sub(pattern, "", lns)

        if _debug:
            print(lns)

        return lns
