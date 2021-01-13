import subprocess
import json
import sys
import os


def cmd2result(cmd):
	result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
	result = result.stdout.decode('utf-8')
	result = result.split("\n")
	result = list(filter(None, result))
	return result


def splitFunctions(fileDir):
	cmd = "find " + fileDir + " -name '*.c'"
	result1 = cmd2result(cmd)

	# cmd = "find " + fileDir + " -name '*.cpp'"
	# result2 = cmd2result(cmd)

	# result = result1 + result2
	result = result1

	dictResult = list()
	filecnt = 0
	funccnt = 0
	for f in result:
		cmd = "clang-split-function " + f + " --"
		try:
			strResult = cmd2result(cmd)
		except:
			continue
		filecnt += 1
		print("No. " + str(filecnt) + " files is processing.........")
		for s in strResult:
			json_acceptable_string = s.replace("'", "\"")
			d = json.loads(json_acceptable_string)
			dictResult.append(d)
			funccnt += 1
			print("Processed " + str(funccnt) + " funcs already.")
			
	with open("FuncInfo.json", 'w') as fi:
		json.dump(dictResult, fi, indent=2)


def readFunc(func):
	with open(func["file"], 'r', encoding="ISO-8859-1") as f:
		lines = f.readlines()
		funcStr = ''.join(lines[(func["begin"][0]-1):func["end"][0]])
	return funcStr


def extractJson(jsonFile, tgtDir):
	with open(jsonFile, 'r') as jf:
		functions = json.load(jf)
		for func in functions:
			try:
				code = readFunc(func)
			except:
				continue
			fileBase = os.path.basename(func["file"])
			tgtFileBase = func["function"] + "_" + fileBase
			tgtFile = os.path.join(tgtDir, tgtFileBase)
			with open(tgtFile, "w") as tf:
				tf.write(code)


if __name__ == '__main__':
	# splitFunctions(sys.argv[1])
	extractJson(sys.argv[1], sys.argv[2])