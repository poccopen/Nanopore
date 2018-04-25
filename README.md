# Nanopore
ナノポアシークエンサーデータ解析のためのPythonスクリプトを置いてあります。

## Target_seq_extraction.py

#### [依存性]
マッピングのために minialign がインストールされている必要があります。(https://github.com/ocxtal/minialign)

#### [使い方]  
```$ python3 Target_seq_extraction.py [flanking_seq_1.fasta] [flanking_seq_2.fasta] [target_seq.fasta] [input.fastq]```

#### [目的]
上流側隣接配列、下流側隣接配列、ターゲット配列のすべての配列を含むリードを抽出します。  
上流側隣接配列と下流側隣接配列の間の塩基長を計算します。

#### [入力ファイル]
下記の4つのファイルが必要です。  
- 上流側隣接配列ファイル（FASTA形式）
- 下流側隣接配列ファイル（FASTA形式）
- ターゲット配列ファイル（FASTA形式）
- ナノポアシークエンサー出力ファイル（FASTQ形式）

#### [出力ファイル]
input.target.positive というファイル名形式のファイルひとつを出力します。  
各行には  
- 上流側隣接配列と下流側隣接配列の間の塩基長
- リードID
- リードの配列  
が記述されています。
