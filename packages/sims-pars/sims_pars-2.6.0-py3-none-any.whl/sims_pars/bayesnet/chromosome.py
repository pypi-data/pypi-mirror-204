import pandas as pd
import numpy as np
import networkx as nx

__all__ = ['Chromosome']


class Chromosome:
    def __init__(self, vs=None, prob=np.NaN):
        self.Locus = dict(vs) if vs else dict()
        self.LogProb = prob

    def __len__(self):
        return len(self.Locus)

    def __iter__(self):
        return iter(self.Locus.items())

    def __bool__(self):
        return True

    def __getitem__(self, item):
        return self.Locus[item]

    def __setitem__(self, key, value):
        self.Locus[key] = value
        self.reset_probability()

    def __contains__(self, item):
        return item in self.Locus

    def keys(self):
        return self.Locus.keys()

    def impulse(self, new_locus, bn=None):
        """
        Change the value of some locus
        :param new_locus: {name: value}; value = None if prior applied
        :type new_locus: dict
        :param bn: source bayesian network; None if no check needed
        :type bn: BayesNet
        :return:
        """
        if bn:
            g = bn.DAG
            imp = {k: v for k, v in new_locus.items() if k in self}
            shocked = set.union(*[set(nx.descendants(g, k)) for k in imp.keys()])
            non_imp = [k for k, v in imp.items() if v is None]
            imp = {k: v for k, v in imp.items() if v is not None}
            shocked.difference_update(imp.keys())
            shocked = shocked.union(non_imp)
            shocked.intersection_update(self.Locus.keys())
            self.Locus.update(imp)

            for nod in bn.Order:
                if nod in shocked:
                    self[nod] = g.nodes[nod]['loci'].render(self)

            if imp:
                self.reset_probability()

        else:
            imp = {k: v for k, v in new_locus.items() if k in self}
            self.Locus.update(imp)
            if imp:
                self.reset_probability()

    def clone(self):
        g = Chromosome(self.Locus, self.LogProb)
        return g

    def reset_probability(self):
        self.LogProb = np.NaN

    def is_evaluated(self):
        return not np.isnan(self.LogProb)

    def __repr__(self):
        if not self.Locus:
            return 'empty'
        loc = [('{}: {:g}' if isinstance(v, float) else '{}: {}').format(k, v) for k, v in self.Locus.items()]
        return ", ".join(loc)

    def __dict__(self):
        return dict(self.Locus)

    def to_json(self):
        return {
            'Locus': self.Locus,
            'LogProb': self.LogProb
        }

    def to_data(self):
        vs = dict(self.Locus)
        if self.is_evaluated():
            vs['LogProb'] = self.LogProb
        return vs

    @staticmethod
    def from_json(js):
        return Chromosome(js['Locus'], js['LogProb'])

    @staticmethod
    def summarise(genes):
        df = pd.DataFrame([gene.Locus for gene in genes])
        return df.describe()

    @staticmethod
    def mean(genes):
        df = pd.DataFrame([gene.Locus for gene in genes])
        return dict(df.mean())

    @staticmethod
    def to_data_frame(genes):
        return pd.DataFrame([gene.to_data() for gene in genes])
