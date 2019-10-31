import os
import shutil
import subprocess


class WheelGenerator:

	def __init__(self, path, pkg_name):
		self.lib_path = os.path.abspath(path)
		self.package_name = pkg_name

	def generate_wheel(self):
		self.create_lib_structure()
		self.run_wheel_command()

	def create_lib_structure(self):
		os.chdir(self.lib_path)
		files = [f for f in os.listdir(self.lib_path)]
		package_dir = os.path.join(self.lib_path, self.package_name)
		os.mkdir(package_dir)
		for file in files:
			shutil.move(os.path.join(self.lib_path, file), package_dir)
		self.create_necessary_files()

	def create_necessary_files(self):
		package_dir = os.path.join(self.lib_path, self.package_name)
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
			f.write("    package_data={'"+self.package_name+"': ['*.pyd']},\r")
			f.write('    include_package_data=True)')

	def run_wheel_command(self):
		subprocess.run(["python", "setup.py", "sdist", "bdist_wheel"])
