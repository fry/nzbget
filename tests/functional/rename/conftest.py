import os
import shutil
import subprocess
import pytest

def pytest_addoption(parser):
	parser.addini('par2_bin', 'path to par2 binary', default=None)

@pytest.fixture(scope='session', autouse=True)
def prepare_testdata(request):
	print('Preparing test data for "rename"')

	nserv_datadir = pytest.config.getini('nserv_datadir')
	nzbget_bin = pytest.config.getini('nzbget_bin')
	par2_bin = pytest.config.getini('par2_bin')

	if not os.path.exists(par2_bin):
		pytest.exit('Cannot prepare test files. Set option "par2_bin in pytest.ini"')

	if not os.path.exists(nserv_datadir):
		print('Creating nserv datadir')
		os.makedirs(nserv_datadir)

	nzbget_srcdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
	testdata_dir = nzbget_srcdir + '/tests/testdata'

	if not os.path.exists(nserv_datadir + '/parrename'):
		os.makedirs(nserv_datadir + '/parrename')
		shutil.copyfile(testdata_dir + '/rarrenamer/testfile3.part01.rar', nserv_datadir + '/parrename/testfile3.part01.rar')
		shutil.copyfile(testdata_dir + '/rarrenamer/testfile3.part02.rar', nserv_datadir + '/parrename/testfile3.part02.rar')
		shutil.copyfile(testdata_dir + '/rarrenamer/testfile3.part03.rar', nserv_datadir + '/parrename/testfile3.part03.rar')
		os.chdir(nserv_datadir + '/parrename')
		if 0 != subprocess.call([par2_bin, 'c', '-c1', '-u', 'parrename.par2', '*']):
			pytest.exit('Test file generation failed')
		os.rename(nserv_datadir + '/parrename/testfile3.part01.rar', nserv_datadir + '/parrename/abc.21')
		os.rename(nserv_datadir + '/parrename/testfile3.part02.rar', nserv_datadir + '/parrename/abc.02')
		os.rename(nserv_datadir + '/parrename/testfile3.part03.rar', nserv_datadir + '/parrename/abc.15')

	prepare_rarrenametest('rarrename3', 'testfile3', testdata_dir, nserv_datadir, par2_bin)
	prepare_rarrenametest('rarrename5', 'testfile5', testdata_dir, nserv_datadir, par2_bin)

	if 0 != subprocess.call([nzbget_bin, '--nserv', '-d', nserv_datadir, '-v', '2', '-z', '3000', '-q']):
		pytest.exit('Test file generation failed')

def prepare_rarrenametest(dirname, testfile, testdata_dir, nserv_datadir, par2_bin):
	if not os.path.exists(nserv_datadir + '/' + dirname + '.nzb'):
		os.makedirs(nserv_datadir + '/' + dirname)
		shutil.copyfile(testdata_dir + '/rarrenamer/' + testfile + '.part01.rar', nserv_datadir + '/' + dirname + '/abc.21')
		shutil.copyfile(testdata_dir + '/rarrenamer/' + testfile + '.part02.rar', nserv_datadir + '/' + dirname + '/abc.02')
		shutil.copyfile(testdata_dir + '/rarrenamer/' + testfile + '.part03.rar', nserv_datadir + '/' + dirname + '/abc.15')
		os.chdir(nserv_datadir + '/' + dirname)
		if 0 != subprocess.call([par2_bin, 'c', '-c1', '-u', 'parrename.par2', '*']):
			pytest.exit('Test file generation failed')
