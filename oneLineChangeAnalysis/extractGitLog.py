import json
import re
import javalang
import sys
import random
import subprocess
import os
import numpy as np


def ExtractGitLog():
	small = open('bugs.json','r')

	#smallStr = open('/home/robin/Documents/one-line-bug-dataset/BugsSmall.txt', 'w')
	#largeStr = open('/home/robin/Documents/one-line-bug-dataset/BugsLarge.txt', 'w')

	smallData = json.load(small)

	ProjDir = "/home/robin/Documents/projects"
	if not os.path.isdir(ProjDir):
		os.makedirs(ProjDir)

	projs = list()

	for idx, sd in enumerate(smallData):
		projectName = sd["projectName"]
		projs.append(projectName)
		
		#lineNum = sd["lineNum"]

	projs = set(projs)

	for proj in projs:

		p = proj.split('.')[-1]
		bugProj = os.path.join(ProjDir, p)
		
		if not os.path.isdir(bugProj):
			cmd = ""
			cmd += "cd " + ProjDir + ";"
			cmd += "git clone https://github.com/" + proj.replace('.', '/') + ".git"
			result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
		
		resultDir = os.path.join("/home/robin/Documents/dataset-analysis/results", p)
		if not os.path.isdir(resultDir):
			os.makedirs(resultDir)
		cmd = ""
		cmd += "cd " + bugProj + ";"
		cmd += "git log --stat --follow *.java > " + os.path.join(resultDir, "java_stats.txt") + ";"
		#cmd += "git log --stat > " + os.path.join(resultDir, "stats.txt") + ";"
		#cmd += "git log --numstat > " + os.path.join(resultDir, "numstats.txt") + ";"
	
		subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
	'''

	baseDirLarge = "/home/robin/Documents/DataSetLarge"
	if not os.path.isdir(baseDirLarge):
		os.makedirs(baseDirLarge)

	bugBaseDirLarge = os.path.join(baseDirLarge, "buggy")
	if not os.path.isdir(bugBaseDirLarge):
		os.makedirs(bugBaseDirLarge)

	patchBaseDirLarge = os.path.join(baseDirLarge, "patch")
	if not os.path.isdir(patchBaseDirLarge):
		os.makedirs(patchBaseDirLarge)


	for idx, sd in enumerate(largeData):
		projectName = sd["projectName"]
		proj = projectName.split('.')[-1]
		patchSHA1 = sd["commitSHA1"]
		patchFile = sd["commitFile"]
		#lineNum = sd["lineNum"]
		bugDir = os.path.join(bugBaseDirLarge, str(idx))
		if not os.path.isdir(bugDir):
			os.makedirs(bugDir)

		patchDir = os.path.join(patchBaseDirLarge, str(idx))
		if not os.path.isdir(patchDir):
			os.makedirs(patchDir)

		bugProj = os.path.join(ProjDir, proj)
		if not os.path.isdir(bugProj):
			cmd = ""
			cmd += "cd " + ProjDir + ";"
			cmd += "git clone https://github.com/" + projectName.replace('.', '/') + ".git"
			result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
		cmd = ""
		cmd += "cd " + bugProj + ";"
		cmd += "git checkout " + patchSHA1 + "^" + ";"
		cmd += "cp " + patchFile + " " + bugDir + ";"
		cmd += "git checkout " + patchSHA1 + ";"
		cmd += "cp " + patchFile + " " + patchDir
		subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
	'''


ExtractGitLog()