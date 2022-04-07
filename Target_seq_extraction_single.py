# -*- coding: utf-8 -*-
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
if argc < 3:
	print("Usage: python3 {} [target_seq.fasta] [input.fastq]".format(argvs[0]))
else:
	# それぞれのファイル名を格納する
	tseqname = argvs[1]
	fastqname = argvs[2]
	tempname = "temp.fasta"
	outputname = re.sub(r".fastq$", r".target.positive.fastq", fastqname)
	flag = 0

	with open(fastqname) as fastqfile:
		# 最終出力ファイルの最初の行にヘッダーを書かない
		# output = open(outputname, 'a')
		# output.write("Repeatsize\tReadID\tSequence\n")
		# output.close()

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
				tempfasta.write(">" + id + "\n" + line + "\n")
				tempfasta.close()
				# 上流側の隣接配列をクエリーとしてminialignを実行する（minialignの出力はPAF形式）
				target = subprocess.check_output(["minialign", "-t", "8", "-xont", "-Opaf", tseqname, tempname])
				target = target.decode().split()
				if (len(target) > 7):
					# リードID、リード配列を最終出力ファイルに追記する
					output = open(outputname, 'a')
					output.write(id + "\n" + line)
					output.close()
					# フラグを2にして次の行に移る
					flag = 2
					continue
				else:
					# フラグをゼロに戻して次の行に移る
					flag = 0
					continue

			# フラグが2のとき（minimap2がヒットを返した状態）はfastq情報を書き出す
			elif (flag == 2):
				output = open(outputname, 'a')
				output.write(line)
				output.close()
				continue

			else:
				flag = 0
				continue
