import os
import shutil
import subprocess
import sys


class WheelGenerator:
	"""
	Class used to generate wheel out of directory

	Attributes
	----------
	lib_path : str
		Library directory path string
	package_name : str
		Name of package to be generated
	"""

	def __init__(self, path, pkg_name):
		self.lib_path = os.path.abspath(path)
		self.package_name = pkg_name

	def generate_wheel(self):
		"""Creates package structure and generates wheel"""

		self.create_lib_structure()
		self.run_wheel_command()

	def create_lib_structure(self):
		"""Creates necessary library structure and files"""

		os.chdir(self.lib_path)
		files = [f for f in os.listdir(self.lib_path)]
		package_dir = os.path.join(self.lib_path, self.package_name)
		os.mkdir(package_dir)
		for file in files:
			shutil.move(os.path.join(self.lib_path, file), package_dir)
		libraries = [f for f in os.listdir(package_dir) if f.endswith(('.so', '.dll', '.pyd'))]
		libs = os.path.join(package_dir, 'lib')
		os.mkdir(libs)
		for lib in libraries:
			shutil.move(os.path.join(package_dir, lib), libs)
		self.create_necessary_files()

	def create_necessary_files(self):
		"""Creates necessary files for package e.g. setup.py"""

		package_dir = os.path.join(self.lib_path, self.package_name)
		libs_dir = os.path.join(package_dir, 'lib')
		if os.path.exists(libs_dir):
			open(os.path.join(libs_dir, '__init__.py'), 'a').close()
		open(os.path.join(package_dir, '__init__.py'), 'a').close()
		with open('setup.py', 'w+') as f:
			f.write('import setuptools\r\n')
			f.write('setuptools.setup(\r')
			f.write('    name="'+self.package_name+'",\r')
			f.write('    version="1.0.0",\r')
			f.write('    author_email="tetrite@gmail.com",\r')
			f.write('    description="Package build with cBinder",\r')
			f.write('    url="https://github.com/Tetrite/cBinder",\r')
			f.write("    packages=['"+self.package_name+"'],\r")
			f.write("    package_data={'': ['*.pyd','*.so','*.dll']},\r")
			f.write('    include_package_data=True)')

	def run_wheel_command(self):
		"""Runs wheel command"""
		subprocess.run([sys.executable, "setup.py", "sdist", "bdist_wheel"])
