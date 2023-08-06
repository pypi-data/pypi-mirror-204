import json as j
from .info import __info__

class HeroJson():
    
    def __init__(self, path : str, enconding : str = 'utf-8') -> None:
        self.path = path
        self.encoding = enconding
        self.__read__()

    def __read__(self, ) -> None:
        with open(file=self.path,encoding=self.encoding) as file:
            self.content_file = file.read()
            self.content_dict = j.loads(self.content_file)
    
    def key(self, key : str) -> str:
        try:
            return self.content_dict[key]
        except:
            return None
    
    def update(self, key : str, value : any) -> bool | None:
        if self.key(key) != None:
            
            self.content_dict[key] = value
            with open(self.path,mode='w',encoding=self.encoding) as file:
                j.dump(self.content_dict,file,sort_keys=True,indent=4,skipkeys=True)
            
            if self.key(key=key) == value:
                return True
            else: return None

        else:
            return False
    
    def drop(self, key : str) -> bool:
        del self.content_dict[key]
        with open(self.path,mode='w',encoding=self.encoding) as file:
            j.dump(self.content_dict,file,sort_keys=True,indent=4,skipkeys=True)
        if self.key(key) != None:
            return False
        else: return True

    def add(self, key : str , value : any ) -> bool | None:
        if self.key(key) != None:
            return False
        self.content_dict[key] = value
        with open(self.path,mode='w',encoding=self.encoding) as file:
            j.dump(self.content_dict,file,sort_keys=True,indent=4,skipkeys=True)     
        if self.key(key=key) == value:
            return True
        else: return None
    
    def AllKeys(self, ) -> list[str]:
        self.return_list = []
        for x in self.content_dict:
            self.return_list.append(x)
        return self.return_list
    
    def AllValues(self, ) -> list[any]:
        self.return_list = []
        for x in self.content_dict:
            self.return_list.append(self.content_dict[x])
        return self.return_list
    
    def Content(self, ) -> str:
        return self.content_file
    
    def info(self, ) -> object:
        __info__()

