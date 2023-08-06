from distutils.core import setup

setup(
    name='chejoLib',                                            # Nombre del paquete
    packages=['libs'],                                          # Folder del paquete
    version='0.1',                                              # Version de la libreria
    license='MIT',                                              # Licencia
    description='Libreria de Chejo',                            # Breve descripcion de la libreria
    author='Sergio Guzman',
    author_email='sergiohumberto27@gmail.com',
    url='https://github.com/sergioguzman27',                    # Url del sitio web o de Github
    download_url='https://github.com/sergioguzman27/mi-lib',    # Link del repositorio de la libreria
    keywords=[],                                                # Keywords para definir el paquete/libreria
    install_requires=[                                          # Dependencias que se requieran instalar
        'pytz',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',                      # Estados del paquete "3 - Alpha", "4 - Beta", "5 - Production/Stable"
        'Intended Audience :: Developers',                      # Definir cual es el publico al que va dirigido el paquete
        'License :: OSI Approved :: MIT License',               # Licencia
        'Programming Language :: Python :: 3',                  # Especificar las versiones de python que soportan el paquete
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)