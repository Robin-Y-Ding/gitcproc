import subprocess
import json
import os
import sys
import re


def readProj():
	small = open('bugs.json','r')

	smallData = json.load(small)

	ProjDir = "/home/robin/Documents/projects"
	if not os.path.isdir(ProjDir):
		print ("Error projects!")
		return

	projs = list()

	for idx, sd in enumerate(smallData):
		projectName = sd["projectName"]
		projs.append(projectName)
		
	projs = set(projs)
	#finalReport = open('finalReport.txt', 'w')
	finalReport = open('finalReportAll.txt', 'w')

	totalOneRepCnt = 0
	totalCnt = 0

	for proj in projs:
		p = proj.split('.')[-1]
		

		bugProj = os.path.join(ProjDir, p)
		if not os.path.isdir(bugProj):
			print ("No such project: " + p)
			continue

		finalReport.write("----------------------\n")
		finalReport.write("Project: " + p + '\n')

		resultDir = os.path.join("/home/robin/Documents/dataset-analysis/results", p)
		if not os.path.isdir(resultDir):
			print ("Error results!")
			return

		statsFile = open(os.path.join(resultDir, "stats.txt"), 'r', encoding="ISO-8859-1")
		statsString = statsFile.read()
		oneReplaceCnt = statsString.count("| 2 +-\n 1 file changed, 1 insertion(+), 1 deletion(-)\n")
		oneInsertCnt = statsString.count(" 1 file changed, 1 insertion(+)\n")
		oneDeleteCnt = statsString.count(" 1 file changed, 1 deletion(-)\n")

		oneLineChange = oneReplaceCnt + oneInsertCnt + oneDeleteCnt
		
		totalOneRepCnt = totalOneRepCnt + oneLineChange
		
		finalReport.write("Count of commits that only contains one line replacement: " + str(oneReplaceCnt) + '\n')
		finalReport.write("Count of commits that only contains one line insertion: " + str(oneInsertCnt) + '\n')
		finalReport.write("Count of commits that only contains one line deletion: " + str(oneDeleteCnt) + '\n')
		finalReport.write("Count of commits that contains one line change: " + str(oneLineChange) + '\n')

		cmd = ""
		cmd += "cd " + bugProj + ";"
		cmd = cmd + "git rev-list --count HEAD"
		result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
		result = result.stdout.decode('utf-8').strip()

		totalCnt = totalCnt + int(result)
		
		finalReport.write("Count of commits: " + result + '\n')

		pct = 100 * oneLineChange / int(result)
		finalReport.write("Percentage of one line replacement: " + str(pct) + '%' + '\n')

	finalReport.write("----------------------------------\n----------------------------------\n")
	finalReport.write("Total one line replacement count: " + str(totalOneRepCnt) + '\n')
	finalReport.write("Count of commits: " + str(totalCnt) + '\n')
	totalPct = 100 * totalOneRepCnt / totalCnt
	finalReport.write("Overall percentage of one line replacement: " + str(totalPct) + '%' + '\n')

	small.close()
	finalReport.close()


def readProjJavaOnly():
	small = open('bugs.json','r')

	smallData = json.load(small)

	ProjDir = "/home/robin/Documents/projects"
	if not os.path.isdir(ProjDir):
		print ("Error projects!")
		return

	projs = list()

	for idx, sd in enumerate(smallData):
		projectName = sd["projectName"]
		projs.append(projectName)
		
	projs = set(projs)
	finalReport = open('finalReportJavaOnlyAll.txt', 'w')

	totalOneRepCnt = 0
	totalCnt = 0

	for proj in projs:
		p = proj.split('.')[-1]
		

		bugProj = os.path.join(ProjDir, p)
		if not os.path.isdir(bugProj):
			print ("No such project: " + p)
			continue

		finalReport.write("----------------------\n")
		finalReport.write("Project: " + p + '\n')

		resultDir = os.path.join("/home/robin/Documents/dataset-analysis/results", p)
		if not os.path.isdir(resultDir):
			print ("Error results!")
			return

		statsFile = open(os.path.join(resultDir, "java_stats.txt"), 'r', encoding="ISO-8859-1")
		statsString = statsFile.read()
		oneReplaceCnt = statsString.count("| 2 +-\n 1 file changed, 1 insertion(+), 1 deletion(-)\n")
		oneInsertCnt = statsString.count(" 1 file changed, 1 insertion(+)\n")
		oneDeleteCnt = statsString.count(" 1 file changed, 1 deletion(-)\n")

		oneLineChange = oneReplaceCnt + oneInsertCnt + oneDeleteCnt
		
		totalOneRepCnt = totalOneRepCnt + oneLineChange
		
		finalReport.write("Count of commits that only contains one line replacement: " + str(oneReplaceCnt) + '\n')
		finalReport.write("Count of commits that only contains one line insertion: " + str(oneInsertCnt) + '\n')
		finalReport.write("Count of commits that only contains one line deletion: " + str(oneDeleteCnt) + '\n')
		finalReport.write("Count of commits that contains one line change: " + str(oneLineChange) + '\n')

		result = statsString.count("Author: ")
		result = str(result)

		totalCnt = totalCnt + int(result)
		
		finalReport.write("Count of commits: " + result + '\n')

		pct = 100 * oneLineChange / int(result)
		finalReport.write("Percentage of one line replacement: " + str(pct) + '%' + '\n')

	finalReport.write("----------------------------------\n----------------------------------\n")
	finalReport.write("Total one line replacement count: " + str(totalOneRepCnt) + '\n')
	finalReport.write("Count of commits: " + str(totalCnt) + '\n')
	totalPct = 100 * totalOneRepCnt / totalCnt
	finalReport.write("Overall percentage of one line replacement: " + str(totalPct) + '%' + '\n')

	small.close()
	finalReport.close()
	

def genProjectsList():
	small = open('bugs.json','r')
	projList = open("ProjList.txt", 'w')
	smallData = json.load(small)
	projs = list()

	for sd in smallData:
		projectName = sd["projectName"]
		projs.append(projectName)
		
	projs = set(projs)

	for proj in projs:
		p = proj.replace('.','/')
		projList.write(p + '\n')


def bugFixAnalysis():
	changeSum = open('ChangeSummary.csv', 'r')
	bugFixCommitsStat = open('BugFixCommitsStats.txt', 'w')
	bugFixCommitsNumstat = open('BugFixCommitsNumstats.txt', 'w')
	projectsBase = "projects/"
	commits = changeSum.readlines()
	cnt = 0

	for c in commits:
		proj, sha, author, email, date, bugFix = c.strip().replace("'", "").split(',')
		proj = proj.replace('"', '')
		if bugFix == 'True':
			projPath = os.path.join(projectsBase, proj)
			cmd = ''
			cmd = cmd + "cd " + projPath + ";"
			cmd = cmd + "git show --stat " + sha
			result1 = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
			result1 = result1.stdout.decode('utf-8')
			bugFixCommitsStat.write(result1)

			cmd = ''
			cmd = cmd + "cd " + projPath + ";"
			cmd = cmd + "git show --numstat " + sha
			result2 = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
			result2 = result2.stdout.decode('utf-8')
			bugFixCommitsNumstat.write(result2)

			cnt += 1

	print("Total bug fix commits: " + str(cnt))


def countFiles():
	bugFixCommitsStat = open('BugFixCommitsStats.txt', 'r')
	bugFixCommitsNumstat = open('BugFixCommitsNumstats.txt', 'r')
	Stat = bugFixCommitsStat.readlines()
	Numstat = bugFixCommitsNumstat.read()

	modFile = 0
	for l in Stat:
		#if "file changed, " in l or "files changed, " in l:
		x = re.findall("\s[0-9]+\sfiles?\schanged,\s", l)
		if (x):
			m = int(l.split(' ')[1])
			modFile = modFile + m

	print(modFile)

	y = len(re.findall("commit\s[a-zA-Z0-9]+\nAuthor:\s", Numstat))
	print(y)
	rep = Numstat.count("\n1\t1\t")
	dele = Numstat.count("\n1\t0\t")
	inst = Numstat.count("\n0\t1\t")

	modif = rep + dele + inst
	print(modif)
#getOneLineChange()
#readProj()
#readProjJavaOnly()
#genProjectsList()

#bugFixAnalysis()

countFiles()