import argparse
import subprocess

def printcol(str):
	print('\x1b[6;30;42m' + str + '\x1b[0m')

parser = argparse.ArgumentParser(description=
	"File downloader for ios device, "
	"no jailbreak need, "
	"Usage: "
	"python downloader.py network.jibrel.jwallet ./iphoneDump1"
	)
parser.add_argument("bundle", action='store', help="app bundle id")
parser.add_argument("to", action='store', help="destination path")
parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")

args = parser.parse_args()

cmdDownload = "ios-deploy --bundle_id {} --download=/ --to {}".format(args.bundle, args.to)

printcol("Downloading")

process = subprocess.Popen(cmdDownload.split(), stdout=subprocess.PIPE)
res, error = process.communicate()
print(res)


printcol("Done")
