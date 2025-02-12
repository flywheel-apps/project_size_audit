# -*- coding: utf-8 -*-
"""GetAccurateProjectSize.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1J8fOK_J3FXWV5o8IUCuBYW2w4ccKehdV
"""


import os
import flywheel
api_key = os.environ['SS_API']

fw = flywheel.Client(api_key)

#@title Define some functions

def get_container_size(container):
  print(f"working on {container.label} {container.container_type}")
  total_size = 0

  container = container.reload()
  if container.container_type == 'project':
    children = container.subjects.iter()
  elif container.container_type == 'subject':
    children = container.sessions.iter()
  elif container.container_type == 'session':
    children = container.acquisitions.iter()
  else:
    children = []

  total_size += get_analysis_outputs(container)
  total_size += get_file_outputs(container)

  for child in children:
    total_size += get_container_size(child)

  return(total_size)

def get_analysis_outputs(container):

  analyses_size = 0

  if container.get('analyses'):
    analyses = container.get('analyses')

    for analysis in analyses:
      analysis = analysis.reload()
      analyses_size += get_file_outputs(analysis)

  return(analyses_size)


def get_file_outputs(container):

  file_size = 0

  if container.get('files'):

    for file in container.get('files'):
      file_size += file.get('size',0)

  return(file_size)

#@title Set Project
#@markdown Determine which project to get stats on, or set this to "all" to get all projects

project = '5dc1d8b1e74aa3005e0dbec7' # RepoBrainChart

# Get the projects to work on

if project.lower() == 'all':
  projects = fw.projects()
else:
  projects = [fw.get(project)]

# Do the actual calculation

project_report = {}

for project in projects:

  if not project_report.get(project.label):
    current_project = project.label
  else:
    project_iter = 1
    while project_report.get(f"{project.label}_{project_iter}"):
      project_iter += 1

    current_project = f"{project.label}_{project_iter}"

  size = get_container_size(project)
  project_report[current_project] = {'size':size}
  
from pprint import pprint
pprint(project_report)
