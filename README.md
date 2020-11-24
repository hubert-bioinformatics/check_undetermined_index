## check_undetermined_index
This repository contains the script used to count the read number by index sequence in undetermined fastq file. The contents of this repository are 100% open source.

## Table of Contents
* [Intallation](#installation)
* [Usage](#usage)
* [Contributing](#contributing)
* [Credits](#credits)
* [License](#license)


## <a name="installation">Installation</a>
### Requirements
* The server state that [pigz](https://zlib.net/pigz/) has already been installed is needed to run the script


## <a name="usage">Usage</a>

* Basic
  * The script counts the reads by index sequence in the undetermined fastq, and sorts it.
  * command
    * python check_undetermined_index.py \
      -u [undetermined fastq]
  * input
    * undetermined fastq: the file is output of the illumina SW, bcl2fastq2, and gz compressed state.
  * output
    * the csv output: this csv format file has the index sequences and its read count. ]
    <br>

     [![pic](https://github.com/hubert-bioinformatics/check_undetermined_index/blob/main/README_images/undetermined_index.PNG)](https://github.com/hubert-bioinformatics/check_undetermined_index/blob/main/README_images/undetermined_index.PNG)
     <br>
     
* demo play
<br>

[![usage](https://github.com/hubert-bioinformatics/check_undetermined_index/blob/main/README_images/check_undetermined_index.gif)](https://github.com/hubert-bioinformatics/check_undetermined_index/blob/main/README_images/check_undetermined_index.gif)


## <a name="contributing">Contributing</a>


Welcome all contributions that can be a issue report or a pull request to the repository.


## <a name="credits">Credits</a>


hubert (Jong-Hyuk Kim)


## <a name="license">License</a>

Licensed under the MIT License.
