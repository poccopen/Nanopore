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

## Target_seq_ex2fasta.py

#### [依存性]
マッピングのために minialign がインストールされている必要があります。(https://github.com/ocxtal/minialign)

#### [使い方]  
```$ python3 Target_seq_extraction.py [flanking_seq_1.fasta] [flanking_seq_2.fasta] [target_seq.fasta] [input.fastq]```

#### [目的]
上流側隣接配列、下流側隣接配列、ターゲット配列のすべての配列を含むリードを抽出して、複数配列を含むFASTA形式ファイルを出力します。  

#### [入力ファイル]
下記の4つのファイルが必要です。  
- 上流側隣接配列ファイル（FASTA形式）
- 下流側隣接配列ファイル（FASTA形式）
- ターゲット配列ファイル（FASTA形式）
- ナノポアシークエンサー出力ファイル（FASTQ形式）

#### [出力ファイル]
input.target.positive.fasta というファイル名形式のファイルひとつを出力します。  
各行には  
- リードID
- リードの配列

が記述されています。

## Target_seq_extraction_single.py

#### [依存性]
マッピングのために minialign がインストールされている必要があります。(https://github.com/ocxtal/minialign)

#### [使い方]  
```$ python3 Target_seq_extraction_single.py [target_seq.fasta] [input.fastq]```

#### [目的]
ターゲット配列を含むリードを抽出し、fastq形式で保存します。

#### [入力ファイル]
下記の2つのファイルが必要です。
- ターゲット配列ファイル（FASTA形式）
- ナノポアシークエンサー出力ファイル（FASTQ形式）

#### [出力ファイル]
fastqファイルがひとつ出力されます。

## Read_split_by_target.py

#### [依存性]
マッピングのために blastn がインストールされている必要があります。
```$ sudo apt install ncbi-blast+```

#### [使い方]  
```$ python3 Read_split_by_target.py [target_seq.fasta] [input.fastq]```

#### [目的]
ターゲット配列を含むリードを抽出し、ターゲット配列がアラインされる最大領域の外側の配列を5'側・3'側に分割して、別々のレコードとしてfasta形式で出力します。

#### [入力ファイル]
下記の2つのファイルが必要です。
- ターゲット配列ファイル（FASTA形式）
- ナノポアシークエンサー出力ファイル（FASTQ形式。あらかじめターゲット配列を含むものを抽出したファイルを使うことをおすすめします）

#### [出力ファイル]
デフォルトの出力先は標準出力です。適宜ファイルに保存してください。

