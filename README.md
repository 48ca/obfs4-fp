This is code for analyzing the fingerprintability of obfs4proxy packet traces while using the obfs4 pluggable transport. This code is experimental and as written for my capstone project at the University of Virginia.

What is contained:

1. fpgen: Fingerprint generator
2. classification: Fingerprint classification
3. obfs4: obfsproxy fork submodule that contains the modified obfs4 PT

For more information about each module, look at their respective READMEs.

## Setup

1. Download Tor Browser and place it into fpgen/tor-browser_en-US. Install Tor (separate from the TBB) somewhere such that it can be found in the PATH.

2. Setup python3 and install the packages in requirements.txt.

```
$ ./setup-venv.sh
```

3. Pull all submodules if not pulled already.

```
$ ./pull-submodules.sh
```

4. Setup a Go runtime environment that is up-to-date enough to build obfs4proxy. Build obfs4proxy.

```
$ cd obfs4; ./build.sh
```

5. Edit fpgen/env.sh to include your information. This includes your network interface ($IF) and the bridge IP ($BRIDGE). Set $CAPDIR and $LOGFILE to suit your needs. `source` this file after you are done making changes. These environment variables are used by several scripts in this repository.

6. Start a bridge and configure it to run obfs4proxy. Edit torrc here to ensure that the Tor instance here connects to the bridge via obfs4proxy.

## Usage

### Getting packet traces.

(Working directory: traces)

1. Start Tor.

```
$ ./tor.sh
```

2. If you want to observe status logs during a run, tail the LOGFILE you set in env.sh.

```
$ tail -f $LOGFILE
```

3. If you want to observe obfsproxy logs during a run, tail its log file.

```
$ tail -f tor-data/pt_state/obfs4proxy.log
```

4. Start fpgen.

```
(venv) $ python3 fpgen.py
```

While fpgen is running, you can pause the fetching with pause() or stop it entirely with stop(). You can add other commands on the fly. You can configure Tor to open a control port or socket if you so desire.

Upon completion, all traces will be available in the CAPDIR you set earlier. All traces that failed to download will have suffixed with '.bad'.


### Analysis and feature extraction.

(Working directory: fpgen)

1. To analyze a specific dump, you can run my analyze.py script.

```
(venv) $ python3 analyze.py path/to/trace.pcap
```

2. To generate the CSV that represents the final fingerprints, run csv-gen.sh, and place the output into the fingerprints directory. The classification scripts expect the fingerprints to be placed there.

```
(venv) $ ./csv-gen.sh | tee fingerprints/$FP_NAME.csv
```


### Classification.

(Working directory: classification/)


1. To train and test a Random Forest model on the generated fingerprints:

```
(venv) $ python3 classify.py $FP_NAME
```

2. To do the same but with a multi-level perceptron learner, use

```
(venv) $ python3 classify-nn.py $FP_NAME
```

3. I provide a utility script to generate 10 models and save the best one in 'auto-good-models'.

```
(venv) $ ./good-classify.sh $FP_NAME
```

4. To test the accuracy of the models in 'auto-good-models':

```
(venv) $ ./test.py $FP_NAME
```
