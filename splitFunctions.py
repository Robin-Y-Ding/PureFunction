import subprocess
import json
import sys

def cmd2result(cmd):
	result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
	result = result.stdout.decode('utf-8')
	result = result.split("\n")
	result = list(filter(None, result))
	return result


def splitFunctions(fileDir):
	cmd = "find " + fileDir + " -name '*.c'"
	result1 = cmd2result(cmd)

	cmd = "find " + fileDir + " -name '*.cpp'"
	result2 = cmd2result(cmd)

	result = result1 + result2

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


if __name__ == '__main__':
	splitFunctions(sys.argv[1])
