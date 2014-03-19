import os
import nipype.pipeline.engine as pe
from nipype.interfaces.base import Bunch
import nipype.interfaces.spm as spm
import nipype.interfaces.utility as util
import nipype.interfaces.freesurfer as fs


# folder where  dicom files are located
experiment_dir = '/media/Data/EMPATHYP_DATA' 

# specification of a list with identifier of each subjects
subjects_list = ['Pilote1', 'Pilote2', 'Pilote3']

# name of dicom and output folder
dicom_dir_name = 'Dicom'
data_dir_name = 'Data'

#------------------------------------------------------------
# Node: infosource: specify the list of subjects the pipeline 
#should be executed on
#------------------------------------------------------------

infosource = pe.Node(interface = util.IdentityInterface(fields = ['subject_id']), name='infosource')

infosource.iterables = ('subject_id', subjects_list)

# main node for data conversion
dicom2nifti = pe.Node(interface=fs.DICOMConvert(), name='dicom2nifti')

# store nifti files output
dicom2nifti.inputs.base_output_dir = experiment_dir + '/' + data_dir_name 

# specify optional inputs
dicom2nifti.inputs.file_mapping = [('nifti', '*.nii'), ('info', 'dicom.txt'), ('dti', '*dti.bv*')]
dicom2nifti.inputs.out_type = 'nii'
dicom2nifti.inputs.subject_dir_template = '%s'


#------------------------------------------------------------
# Node ParseDICOMDIR - creates a nicer nifti overview textfile
#------------------------------------------------------------

dcminfo = pe.Node(interface = fs.ParseDICOMDir(), name = 'dcminfo')
dcminfo.inputs.sortbyrun = True
dcminfo.inputs.summarize = True
dcminfo.inputs.dicom_info_file = 'nifti_overview.txt'


#------------------------------------------------------------
# Initiation of preparation pipeline
#------------------------------------------------------------
prepareflow = pe.Workflow(name = 'prepareflow')

#Define where the workingdir of the all_consuming_workflow should be stored at
prepareflow.base_dir = experiment_dir + '/workingdir_prepareflow'

def pathfinder(subjectname, foldername):
	import os
	experiment_dir = '/media/Data/EMPATHYP_DATA' 
	return os.path.join(experiment_dir, foldername, subjectname)

#Connect all components
prepareflow.connect([(infosource, dicom2nifti,[('subject_id', 'subject_id')]),
                     (infosource, dicom2nifti,[(('subject_id', pathfinder, dicom_dir_name), 'dicom_dir')]),
                     (infosource, dcminfo,[(('subject_id', pathfinder, dicom_dir_name), 'dicom_dir')]), ])

prepareflow.run(plugin = 'MultiProc', plugin_args={'n_procs':2})



