#!/usr/bin/env python3
from Bio import Entrez, SeqIO
import pandas as pd, matplotlib.pyplot as plt, time
class G:
    def __init__(s, e, k):
        Entrez.email, Entrez.api_key, Entrez.tool = e, k, 'MiniGen'
        s.D = []
    def S(s, t):
        r = Entrez.read(Entrez.esearch(db='nucleotide', term=f'txid{t}[Organism]', usehistory='y', retmax=0))
        s.c, s.q, s.w = int(r['Count']), r['QueryKey'], r['WebEnv']
        return s.c
    def F(s, minl, maxl, mx=200):
        f = 0
        while f < min(s.c, mx):
            h = Entrez.efetch(db='nucleotide', rettype='gb', retmode='text', retstart=f, retmax=100,
                              webenv=s.w, query_key=s.q)
            for r in SeqIO.parse(h, 'genbank'):
                if minl <= len(r.seq) <= maxl:
                    s.D.append({'acc': r.id, 'len': len(r.seq), 'desc': r.description})
            h.close()
            f += 100
            time.sleep(0.34)
    def C(s, f):
        pd.DataFrame(s.D).sort_values('len', ascending=False).to_csv(f, index=0)
    def P(s, d, o):
        d = d.sort_values('len', ascending=False)
        plt.plot(d.acc, d.len, '-o')
        plt.xticks(rotation=90, fontsize=6)
        plt.tight_layout()
        plt.savefig(o)
        plt.close()
if __name__ == '__main__':
    e = input('Email: ')
    k = input('API key: ')
    t = input('TaxID: ')
    mi = int(input('Min len: '))
    ma = int(input('Max len: '))
    mx = int(input('Max rec: '))
    g = G(e, k)
    if g.S(t):
        g.F(mi, ma, mx)
        if g.D:
            g.C(f'taxid_{t}_filtered.csv')
            g.P(pd.DataFrame(g.D).sort_values('len', ascending=False), f'taxid_{t}_lengths.png')