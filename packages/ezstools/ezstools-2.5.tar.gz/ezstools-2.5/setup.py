import pathlib
from setuptools import find_packages, setup
from ezstools.json_tools import open_json

with open_json("./data.json", mode="r") as data:
    VERSION = data["version"]

HERE = pathlib.Path(__file__).parent

PACKAGE_NAME = 'ezstools' #Debe coincidir con el nombre de la carpeta 
AUTHOR = 'Hendrick Y. "NoVa' #Modificar con vuestros datos
AUTHOR_EMAIL = 'hendrickrodriguez.nova@gmail.com' #Modificar con vuestros datos
URL = '' #Modificar con vuestros datos

LICENSE = 'MIT' #Tipo de licencia
DESCRIPTION = 'Libreria Multi proposito, con modulos variados para ayudar con ciertos problemas' #Descripción corta
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') #Referencia al documento README con una descripción más elaborada
LONG_DESC_TYPE = "text/markdown"


#Paquetes necesarios para que funcione la libreía. Se instalarán a la vez si no lo tuvieras ya instalado
INSTALL_REQUIRES = [
    "datetime", "pyenchant", "importlib", "pick"
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)