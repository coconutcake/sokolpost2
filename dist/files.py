import os
import json


class File():
    """ Klasa operacji na pliku """
    def __init__(self,*args,**kwargs):
       pass

    @property
    def path(self) -> str:
        return self._path

    @property
    def absolute_path(self,*args,**kwargs) -> str:
        return os.path.abspath(self._path)

    @path.setter
    def path(self,value):
        path = value
        if path:
            self._path = path
        else:
            raise ValueError("Brak danych wejściowych")
            
    def read(self,*args,**kwargs):
        if self._path:
            with open(self._path,"r") as f:
                return f.read()

    def write(self,*args,**kwargs):
        if self._path:
            with open(self._path,"w") as f:
                return f.write(kwargs.get("content",""))

class Convertion(File):
    """ Klasa Konwersji """
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def to_dict(self,*args,**kwargs):
        return json.loads(json.dumps(self.read()))

    def to_str(self,*args,**kwargs):
        return json.dumps(self.read())

class Config(Convertion):
    """ Klasa pliku configuracyjnego """
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def get_config(self,*args,**kwargs):
        """ funkcja pomocnicza importujaca config """
        return json.loads(self.to_dict())
    
    def override_config(self):
        """ Pomocnicza funkcja zapisywania configa do pliku """
        self.write(content=json.dumps(self._config))

    @property
    def server(self,*args,**kwargs) -> str:
        """ Zwraca konfiguracje servera """
        return self.config.get("server")

    @property
    def config(self,*args,**kwargs) -> str:
        return self.get_config()
    
    @property
    def address(self) -> str:
        return self.config.get("address")

    @property
    def authorization(self) -> str:
        return self.config.get("header")['Authorization']

    @authorization.setter
    def authorization(self,value):
        self._config = self.config
        if value:
            self._config['header']['Authorization'] = value
            self.override_config()
        else:
            raise ValueError("Brak danych wejsciowych")

    @config.setter
    def config(self,value):
        self._config = self.config
        if value:
            self._config = value
            self.override_config()
        else:
            raise ValueError("Brak danych wejsciowych")


    @address.setter
    def address(self,value):
        self._config = self.config
        if value:
            self._config['address'] = value
            self.override_config()
        else:
            raise ValueError("Brak danych wejsciowych")



