from robot.api.deco import keyword
from robot.api import Error

class Scenarios():
    ###Load id the scenarios ###
    def get_id_scenario(self, lst_tags:list, tag_id:str):
        try:
            for tag in lst_tags:
                if str(tag).startswith(tag_id.casefold()):
                    return str(tag).upper()

            return None
        except Exception as e:
            raise Error(e)