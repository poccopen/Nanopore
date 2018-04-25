# argvを取得するためにsysモジュールをインポートする
import sys
# 正規表現を使用するためにreモジュールをインポートする
import re
# 外部コマンドを使用するためにsubprocessモジュールをインポートする
import subprocess

# コマンドライン引数をargvs（リスト）に格納する
argvs = sys.argv
# コマンドライン引数の数を変数argcに格納する
argc = len(argvs)

# 入力するファイル群が指定されていないときは使い方を表示して終了する
if argc < 5:
	print("Usage: python3 {} [flanking_seq_1.fasta] [flanking_seq_2.fasta] [target_seq.fasta] [input.fastq]".format(argvs[0]))
else:
	fseq1name = argvs[1]
	fseq2name = argvs[2]
	tseqname = argvs[3]
	fastqname = argvs[4]
	tempname = "temp.fasta"
	outputname = re.sub(r".fastq$", r".target.positive", fastqname)
	flag = 0
	
	with open(fastqname) as fastqfile:
		for line in fastqfile:
			if re.search(r"^@", line):
				line = line.split()
				id = line[0]
				flag = 1
				continue
			elif (flag == 0):
				continue
			elif (flag == 1):
				tempfasta = open(tempname, 'w')
				tempfasta.write("> " + id + "\n" + line + "\n")
				tempfasta.close()
				up = subprocess.check_output(["minialign", "-xont", "-Opaf", tempname, fseq1name])
				up = up.decode().split()
				if (len(up) > 7):
					down = subprocess.check_output(["minialign", "-xont", "-Opaf", tempname, fseq2name])
					down = down.decode().split()
					if (len(down) > 7):
						repeatsizelist = (abs(int(up[7])-int(down[7])), abs(int(up[7])-int(down[8])), abs(int(up[8])-int(down[7])), abs(int(up[8])-int(down[8])))
						repeatsize = min(repeatsizelist)
						target = subprocess.check_output(["minialign", "-xont", "-Opaf", tempname, tseqname])
						target = target.decode().split()
						if (len(target) > 7):
							output = open(outputname, 'a')
							output.write(str(repeatsize) + "\t" + id + "\t" + line)
							flag = 0
							continue
						else:
							flag = 0
							continue
					else:
						flag = 0
						continue
				else:
					flag = 0
					continue
			
				