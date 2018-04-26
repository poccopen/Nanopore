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
	# それぞれのファイル名を格納する
	fseq1name = argvs[1]
	fseq2name = argvs[2]
	tseqname = argvs[3]
	fastqname = argvs[4]
	tempname = "temp.fasta"
	outputname = re.sub(r".fastq$", r".target.positive", fastqname)
	flag = 0
	
	with open(fastqname) as fastqfile:
		# 最終出力ファイルの最初の行にヘッダーを書く
		output = open(outputname, 'a')
		output.write("Repeatsize\tReadID\tSequence\n")
		output.close()
		
		for line in fastqfile:
			# FASTQファイルのIDの行に遭遇したらフラグを立てる
			if re.search(r"^@", line):
				line = line.split()
				id = line[0]
				flag = 1
				continue
			
			# フラグが立っていないときは何もせずに次の行に移る
			elif (flag == 0):
				continue
			
			# フラグが立っている（=FASTQファイル中のID行の次の行=配列の行）場合に実行する部分
			elif (flag == 1):
				# リードの配列をFASTA形式で一時保存する
				tempfasta = open(tempname, 'w')
				tempfasta.write("> " + id + "\n" + line + "\n")
				tempfasta.close()
				# 上流側の隣接配列をクエリーとしてminialignを実行する（minialignの出力はPAF形式）
				up = subprocess.check_output(["minialign", "-xont", "-Opaf", tempname, fseq1name])
				up = up.decode().split()
				if (len(up) > 7):
					# 下流側の隣接配列をクエリーとしてminialignを実行する（minialignの出力はPAF形式）
					down = subprocess.check_output(["minialign", "-xont", "-Opaf", tempname, fseq2name])
					down = down.decode().split()
					if (len(down) > 7):
						# 上下流の隣接配列をクエリーとしたminialignの出力結果から、リピートサイズ(bp)を計算する
						repeatsizelist = (abs(int(up[7])-int(down[7])), abs(int(up[7])-int(down[8])), abs(int(up[8])-int(down[7])), abs(int(up[8])-int(down[8])))
						repeatsize = min(repeatsizelist)
						# ターゲット配列をクエリーとしてminialignを実行する（minialignの出力はPAF形式）
						target = subprocess.check_output(["minialign", "-xont", "-Opaf", tempname, tseqname])
						target = target.decode().split()
						if (len(target) > 7):
							# リピートサイズ、リードID、リード配列を最終出力ファイルに追記する
							output = open(outputname, 'a')
							output.write(str(repeatsize) + "\t" + id + "\t" + line)
							output.close()
							# フラグをゼロに戻して次の行に移る
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
			
				