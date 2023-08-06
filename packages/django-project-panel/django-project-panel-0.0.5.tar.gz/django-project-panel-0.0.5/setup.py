import setuptools

# py setup.py sdist bdist_wheel
# py -m twine upload --repository pypi dist/*

with open("readme.txt", "r", encoding='utf-8') as fh:
	long_description = fh.read()

requirements = [
	"psutil<=5.9.5"
]

setuptools.setup(
	name="django-project-panel",
	version="0.0.5",
	author="EfrosiniaPetrovna",
	author_email="je.to.prace@gmail.com",
	description="Простая мониторинг-панель проекта (размеры всех таблиц в базе данных, медиа файлов и т.д)",
	long_description=long_description,
	long_description_content_type="text",
	url="https://github.com/EfrosiniaPetrovna/django-project-panel",
	packages=setuptools.find_packages(),
	install_requires=requirements,
	# Предоставляет pip некоторые метаданные о пакете. Также отображается на странице PyPi.
	classifiers=[
		"Programming Language :: Python :: 3.10",
	],
	# Требуемая версия Python.
	python_requires='>=3.6',
)