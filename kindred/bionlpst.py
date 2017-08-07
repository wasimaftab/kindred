"""
Importer for BioNLP Shared Task data
"""

import tempfile
import sys
import shutil
import six

import kindred

def load(taskName,ignoreEntities=[]):
	"""
	Download and load the corresponding corpus from the BioNLP Shared Task
	
	:param taskName: The name of the shared task to download (e.g. 'BioNLP-ST-2016_BB-event_train')
	:param ignoreEntities: A list of any entities that should be ignored during loading
	:type taskName: str
	:type ignoreEntities: list of str
	:return: The loaded corpus
	:rtype: kindred.Corpus
	"""

	tempDir = tempfile.mkdtemp()

	taskOptions = {}

	# 2016-BB3-event-train
	files = [('http://2016.bionlp-st.org/tasks/bb2/BioNLP-ST-2016_BB-event_train.zip','BioNLP-ST-2016_BB-event_train.zip', '3b02adff92d8ba8814c9901f4af7681863569fe40cd0d87914258d48f989bb96')]
	expectedDir = 'BioNLP-ST-2016_BB-event_train'
	taskOptions['2016-BB3-event-train'] = (files,expectedDir,False)
	# 2016-BB3-event-dev
	files = [('http://2016.bionlp-st.org/tasks/bb2/BioNLP-ST-2016_BB-event_dev.zip','BioNLP-ST-2016_BB-event_dev.zip', '6d6555b425e42ecc4edf8ffc378439ba722c59922cdf6c5819959861ff683533')]
	expectedDir = 'BioNLP-ST-2016_BB-event_dev'
	taskOptions['2016-BB3-event-dev'] = (files,expectedDir,False)
	# 2016-BB3-event-test
	files = [('http://2016.bionlp-st.org/tasks/bb2/BioNLP-ST-2016_BB-event_test.zip','BioNLP-ST-2016_BB-event_test.zip', 'a1fce4657227bc55aaac5df72d2df615474e0d96a1518234d3e11b3af1e910e7')]
	expectedDir = 'BioNLP-ST-2016_BB-event_test'
	taskOptions['2016-BB3-event-test'] = (files,expectedDir,False)

	# 2016-SeeDev-binary-train
	files = [('http://2016.bionlp-st.org/tasks/seedev/BioNLP-ST-2016_SeeDev-binary_train.zip','BioNLP-ST-2016_SeeDev-binary_train.zip', 'ecca965ae09a31c5675cc2a62f238e0eb3a83c164a925a7e8984dd4d9dbcec84')]
	expectedDir = 'BioNLP-ST-2016_SeeDev-binary_train'
	taskOptions['2016-SeeDev-binary-train'] = (files,expectedDir,False)
	# 2016-SeeDev-binary-dev
	files = [('http://2016.bionlp-st.org/tasks/seedev/BioNLP-ST-2016_SeeDev-binary_dev.zip','BioNLP-ST-2016_SeeDev-binary_dev.zip', 'ea8e0f8bb1bc62982bb9a1a207df33a106c78b14aeb9a0701894943ec9262326')]
	expectedDir = 'BioNLP-ST-2016_SeeDev-binary_dev'
	taskOptions['2016-SeeDev-binary-dev'] = (files,expectedDir,False)
	# 2016-SeeDev-binary-test
	files = [('http://2016.bionlp-st.org/tasks/seedev/BioNLP-ST-2016_SeeDev-binary_test.zip','BioNLP-ST-2016_SeeDev-binary_test.zip', '744df7379a1777f7bdd92f37887f6ca03d15875bf8ae56389e409d5df9e614d2')]
	expectedDir = 'BioNLP-ST-2016_SeeDev-binary_test'
	taskOptions['2016-SeeDev-binary-test'] = (files,expectedDir,False)
	
	# 2016-SeeDev-full-train
	files = [('http://2016.bionlp-st.org/tasks/seedev/BioNLP-ST-2016_SeeDev-full_train.zip','BioNLP-ST-2016_SeeDev-full_train.zip', '52ac808251cf75a4c65f0227f53faf0d39dd6cb3a508becbce0a8dd131a2b7c4')]
	expectedDir = 'BioNLP-ST-2016_SeeDev-full_train'
	taskOptions['2016-SeeDev-full-train'] = (files,expectedDir,True)
	# 2016-SeeDev-full-dev
	files = [('http://2016.bionlp-st.org/tasks/seedev/BioNLP-ST-2016_SeeDev-full_dev.zip','BioNLP-ST-2016_SeeDev-full_dev.zip', '12a07592799197238a8b1b127b759e0d94dd30c52471538553006cafa2203638')]
	expectedDir = 'BioNLP-ST-2016_SeeDev-full_dev'
	taskOptions['2016-SeeDev-full-dev'] = (files,expectedDir,True)
	# 2016-SeeDev-full-test
	files = [('http://2016.bionlp-st.org/tasks/seedev/BioNLP-ST-2016_SeeDev-full_test.zip','BioNLP-ST-2016_SeeDev-full_test.zip', '253b45e1e0aae16f7ce19db4692633556d19fb9e5509e75dbb71de319fb7c2f5')]
	expectedDir = 'BioNLP-ST-2016_SeeDev-full_test'
	taskOptions['2016-SeeDev-full-test'] = (files,expectedDir,True)

	assert taskName in taskOptions.keys(), "%s not a valid option in %s" % (taskName, taskOptions.keys())
	filesToDownload,expectedDir,ignoreComplexRelations = taskOptions[taskName]

	try:
		kindred.utils._downloadFiles(filesToDownload,tempDir)
	except:
		exc_info = sys.exc_info()
		shutil.rmtree(tempDir)
		six.reraise(*exc_info)

	mainDir = kindred.utils._findDir(expectedDir,tempDir)

	corpus = kindred.loadDir(dataFormat='standoff',directory=mainDir,ignoreEntities=ignoreEntities,ignoreComplexRelations=ignoreComplexRelations)

	shutil.rmtree(tempDir)

	return corpus

