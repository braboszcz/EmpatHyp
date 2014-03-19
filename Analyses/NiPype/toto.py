import os
import nipype.pipeline.engine as pe
from nipype.interfaces.base import Bunch
import nipype.interfaces.utility as util
import nipype.interfaces.freesurfer as fs
import nipype.interfaces.dcm2nii as d2n

# folder where  dicom files are located
experiment_dir ='/media/Data/EMPATHYP_DATA/' 

# specification of a list with identifier of each subjects
subjects_list = ['Pilote1', 'Pilote2', 'Pilote3']

# name of dicom and output folder
dicom_dir = 'Dicom'
data_dir = 'Data'

#------------------------------------------------------------
# Node: infosource: specify the list of subjects the pipeline 
#should be executed on
#------------------------------------------------------------

infosource = pe.Node(interface = util.IdentityInterface(fields = ['subject_id']), name='infosource')

infosource.iterables = ('subject_id', subjects_list)

# main node for data conversion
dicom2nifti = pe.Node(interface=d2n.Dcm2nii(), name='dicom2nifti')
dicom2nifti.terminal_output = 'file'

# store nifti files output
dicom2nifti.inputs.output_dir = experiment_dir + data_dir 

# specify optional inputs
#dicom2nifti.inputs.file_mapping = [('nifti', '*.nii'), ('info', 'dicom.txt'), ('dti', '*dti.bv*')]
#dicom2nifti.inputs.out_type = 'nii'
#dicom2nifti.inputs.subject_dir_template = '%s'


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
prepareflow.base_dir = experiment_dir + 'workingdir_prepareflow'

def pathfinder(subjectname, foldername):
	import os
	experiment_dir ='/media/Data/EMPATHYP_DATA/' 
	return os.path.join(experiment_dir, foldername, subjectname)

#Connect all components
prepareflow.connect([(infosource, dicom2nifti,[('subject_id', 'subject_id')]),
                     (infosource, dicom2nifti,[(('subject_id', pathfinder, dicom_dir), 'dicom_dir')]),
                     (infosource, dcminfo,[(('subject_id', pathfinder, dicom_dir), 'dicom_dir')]), ])

# Run pipeline and create graph
prepareflow.run(plugin = 'MultiProc', plugin_args={'n_procs':2})
prepareflow.write_graph(graph2use='flat')


