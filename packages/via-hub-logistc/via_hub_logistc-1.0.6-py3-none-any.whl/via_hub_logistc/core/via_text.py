from robot.api import Error

class Text():
    ### Split text informations $text and $length cut  ###
    def split_text(self, text:str, length:str, start=0):
        try:
            return str(text)[start: int(length)]
        except Exception as e:
            raise Error(e)

### Cut text informations $separator and $length cut  ###
    def cut_text(self, text:str, separator:str, maxsplit:str):
        try:
            return str(text).rsplit(separator, -1)[maxsplit]
        except Exception as e:
            raise Error(e)
