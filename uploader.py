import argparse
import glob
import subprocess


def printcol(str):
	print('\x1b[6;30;42m' + str + '\x1b[0m')

parser = argparse.ArgumentParser(description=
	"File uploader for ios device, "
	"no jailbreak need, "
	"Usage: "
	"python3.7 uploader.py network.jibrel.jwallet /Users/bogdan/hack/iphoneDump2 config.txt"
	)
parser.add_argument("bundle", action='store', help="app bundle id")
parser.add_argument("source", action="store", help="app files source path")
parser.add_argument("config", action="store", help="uploadin files config path")
parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")

args = parser.parse_args()

configs = [line.rstrip('\n') for line in open(args.config)]
configs = [x for x in configs if not x.startswith('#')]

printcol("Configs:")

[print(config) for config in configs]

files = []
for config in configs:
	files = files + glob.glob("{}/{}".format(args.source, config), recursive=True)

filesDest = [line.split(args.source)[1] for line in files]

printcol("Uploading:")
for file in filesDest: 
	print(file);
	source = "{}{}".format(args.source, file)
	to = "{}".format(file)
	cmdUpload = "ios-deploy --bundle_id {} -o {} --to {} ".format(args.bundle, source, to)

	process = subprocess.Popen(cmdUpload.split(), stdout=subprocess.PIPE)
	res, error = process.communicate()

printcol("Done")

