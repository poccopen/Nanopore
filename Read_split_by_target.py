# -*- coding: utf-8 -*-
# argvを取得するためにsysモジュールをインポートする
import sys
# 正規表現を使用するためにreモジュールをインポートする
import re
# 外部コマンドを使用するためにsubprocessモジュールをインポートする
import subprocess
# pandasモジュールをインポートする
import pandas as pd
# numpyモジュールをインポートする
import numpy as np

# コマンドライン引数をargvs（リスト）に格納する
argvs = sys.argv
# コマンドライン引数の数を変数argcに格納する
argc = len(argvs)

# 入力するファイル群が指定されていないときは使い方を表示して終了する
if argc < 3:
	print("")
	print("Usage: python3 {} [target_seq.fasta] [input.fastq]".format(argvs[0]))
else:
	# それぞれのファイル名を格納する
	tseqname = argvs[1]
	fastqname = argvs[2]
	tempname = "temp.fasta"
	flag = 0

	with open(fastqname) as fastqfile:

		for line in fastqfile:
			# FASTQファイルのIDの行に遭遇したらフラグを立てる
			if re.search(r"^@", line):
				line = line.split()
				id = line[0].replace('@','')
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
				# 入力配列をサブジェクト、標的配列をクエリーとしてblastnを実行する（blastnの出力はCSV形式）
				f = open("temp.csv", "w")
				f.write("Query,Subject,Identity,Alignment_length,Mismatches,Gap_opens,Q.start,Q.end,S.start,S.end,E-value,Bit_score\n")
				f.close()
				f = open("temp.csv", "a")
				ret = subprocess.run(["blastn", "-subject", tempname, "-query", tseqname, "-outfmt", "10"], text=True, stdout = f, stderr = subprocess.STDOUT)
				df = pd.read_csv("temp.csv")
				if len(df.index) != 0:
					read_name = id
					read_name5 = read_name + "-5side"
					read_name3 = read_name + "-3side"

					# S.startの最小値・最大値を求める
					SstartMin = df['S.start'].min()
					SstartMax = df['S.start'].max()

					# S.endの最小値・最大値を求める
					SendMin = df['S.end'].min()
					SendMax = df['S.end'].max()

					# アラインされた部分の最小値・最大値を求める
					AlignmentMin = min([SstartMin, SendMin])
					# print(AlignmentMin)
					AlignmentMax = max([SstartMax, SendMax])
					# print(AlignmentMax)

					# 5'側の配列を取り出す
					seq5 = line[0:AlignmentMin-1]
					if len(seq5) != 0:
						print(">" + read_name5)
						print(seq5)

					# 3'側の配列を取り出す
					seq3 = line[AlignmentMax:-1]
					if len(seq3) != 0:
						print(">" + read_name3)
						print(seq3)

				# フラグをゼロに戻して次の行に移る
				flag = 0
				continue

			else:
				# フラグをゼロに戻して次の行に移る
				flag = 0
				continue
