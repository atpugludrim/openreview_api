# What?

This is a repository containing python code that uses the [openreview api](https://docs.openreview.net/getting-started/using-the-api) to scrape all accepted papers from openreview venues (currently works for NeurIPS, ICLR, and ICML only). The scraped data is put into csv files with openreview and I randomly sample five paper titles from it and read whichever one I like. The first field is the openreview id, then the next is title and the last is average score (not always available), so that the file can immediately be opened with it. Example below

```console
foo@bar:~$ shuf -n 5 file.csv
4twbqwV4br,Neural Message-Passing on Attention Graphs for Hallucination Detection,7.0
sSbEEHNEsL,Pay Attention to CTC: Fast and Robust Pseudo-Labelling for Unified Speech Recognition,8.0
gqCh1k0CEX,StochasTok: Improving Fine-Grained Subword Understanding in LLMs,7.0
zUbBaWAM1Q,Symmetry-Aware Bayesian Optimization via Max Kernels,7.333333333333333
9upf6JVssk,MixtureVitae: Open Web-Scale Pretraining Dataset With High Quality Instruction and Reasoning Data Built from Permissive Text Sources,8.0 
```

The first paper here will then be available at `https://openreview.net/forum?id=4twbqwV4br`

# Why?

This is mostly only for me doing a keyword guided random search of the thousands of papers on artificial intelligence and machine learning coming out these days. This may also be useful for someone else, and therefore I am making it public. The code is not my own creation, openreview-api makes it possible and I just use it.

# Caveats?

The openreview api is weird, the papers in each conference have the relevant metadata placed in several different places in several different fields as apparent from the slightly different codes in ICLR, ICML, NeurIPS. A little personalization is required for each conference due to this, and if you want to use it for your own purposes, you might need to do this yourself; although LLMs help a lot.
