from setuptools import setup, find_packages

setup(name='chat_client_GB_course_april',
      version='0.1',
      description='Client packet',
      packages=find_packages(),  # ,Будем искать пакеты тут(включаем авто поиск пакетов)
      author_email='fantom-gtn@list.ru',
      author='Andrei Kasyyanyk',
      install_requeres=['PyQt5', 'sqlalchemy', 'pycruptodome', 'pycryptodomex']
      ##зависимости которые нужно до установить
      )
