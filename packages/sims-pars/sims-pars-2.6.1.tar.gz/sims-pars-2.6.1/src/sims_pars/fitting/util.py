import numpy as np
from sims_pars.fitting.base import AbsObjectiveSimBased, AbsObjective
from sims_pars.bayesnet import Chromosome
from joblib import Parallel, delayed


__all__ = ['draw', 'mutate_and_draw', 'draw_parallel', 'mutate_and_draw_parallel', 'simulate',
           'serve_and_evaluate', 'serve_and_evaluate_parallel']


def draw(obj: AbsObjective, unpack=False):
    p, li, i = None, np.inf, 0
    while np.isinf(li):
        p = obj.sample_prior()
        li = obj.evaluate(p)
        i += 1
        if i > 20:
            p = Chromosome()
            p.LogLikelihood = - np.inf
            break
    if unpack:
        return p.to_json(), i
    else:
        return p, i


def draw_parallel(obj: AbsObjective, n_sim, parallel: Parallel):
    samples = parallel(delayed(draw)(obj, unpack=True) for _ in range(n_sim))
    return [(obj.serve_from_json(p), i) for p, i in samples]


def mutate(p0: Chromosome, sizes):
    p = p0.clone()
    changes = {k: v + sizes[k] for k, v in p.Locus.items() if k in sizes}

    p.impulse(changes)
    return p


def mutate_and_draw(obj: AbsObjective, p0: Chromosome, scale, unpack=False):
    p, li, i = p0, np.inf, 0
    while np.isinf(li):
        sizes = {k: np.random.normal(0, v) for k, v in scale.items()}
        try:
            p = mutate(p0, sizes)
        except ValueError:
            continue

        obj.evaluate_prior(p)
        if np.isinf(p.LogPrior):
            continue
        li = obj.evaluate(p)
        i += 1

        if i > 20:
            p = Chromosome()
            p.LogLikelihood = - np.inf
            break
    else:
        p = p0.clone()

    if unpack:
        return p.to_json(), i
    else:
        return p, i


def __mutate_and_draw(obj: AbsObjective, p0: dict, scale: dict):
    p, li, i = p0, np.inf, 0
    while np.isinf(li):
        sizes = {k: np.random.normal(0, v) for k, v in scale.items()}

        p = {k: p0[k] + v for k, v in sizes.items()}
        try:
            p = obj.serve(p)
        except ValueError:
            continue
        obj.evaluate_prior(p)
        if np.isinf(p.LogPrior):
            continue
        li = obj.evaluate(p)
        i += 1

        if i > 20:
            p = Chromosome()
            p.LogLikelihood = - np.inf
            break

    return p.to_json(), i


def mutate_and_draw_parallel(obj: AbsObjective, p0s, scale, parallel: Parallel):
    p0s_loc = [p0.Locus for p0 in p0s]
    ps = parallel(delayed(__mutate_and_draw)(obj, p0, scale) for p0 in p0s_loc)
    return [(obj.serve_from_json(p), i) for p, i in ps]


def simulate(obj: AbsObjectiveSimBased, p):
    if isinstance(p, dict):
        p = obj.serve_from_json(p)
    return obj.simulate(p)


def serve_and_evaluate(obj: AbsObjective, p):
    if isinstance(p, dict):
        p = obj.serve(p)

    obj.evaluate_prior(p)
    if np.isinf(p.LogPrior):
        return p
    obj.evaluate(p)
    return p


def __serve_and_evaluate(obj: AbsObjective, p):
    if isinstance(p, dict):
        p = obj.serve(p)

    obj.evaluate_prior(p)
    if np.isinf(p.LogPrior):
        return p.to_json()
    obj.evaluate(p)
    return p.to_json()


def serve_and_evaluate_parallel(obj: AbsObjective, p0s, parallel: Parallel):
    p0s_loc = [p0 if isinstance(p0, dict) else p0.Locus for p0 in p0s]
    ps = parallel(delayed(__serve_and_evaluate)(obj, p0) for p0 in p0s_loc)
    return [obj.serve_from_json(p) for p in ps]


if __name__ == '__main__':
    from sims_pars import bayes_net_from_script

    class BetaBinSC(AbsObjectiveSimBased):
        def simulate(self, pars):
            sim = {
                'x1': pars['x1'],
                'x2': pars['x2']
            }
            return sim

        def link_likelihood(self, sim):
            return -((sim['x1'] - 5) ** 2 + (sim['x2'] - 10) ** 2)


    scr = '''
    PCore BetaBin {
        al = 1
        be = 1
    
        p1 ~ beta(al, be)
        p2 ~ beta(al, be)
    
        x1 ~ binom(10, p1)
        x2 ~ binom(n2, p2) 
    }
    '''

    model0 = BetaBinSC(bayes_net_from_script(scr), exo={'n2': 20})
    model0.print()

    p1, _ = draw(model0)
    print(p1)

    ps = draw_parallel(model0, 3, Parallel(n_jobs=4, verbose=6))
    for p, _ in ps:
        print(p)

    si = {'p1': 0.1, 'p2': 0.5}

    try:
        print(mutate(p1, si))
    except ValueError:
        print('Out of boundaries')

    print('Mutate draw')
    print(mutate_and_draw(model0, p1, si)[0])
    print(mutate_and_draw(model0, p1, si)[0])
    print(mutate_and_draw(model0, p1, si)[0])

    ps = mutate_and_draw_parallel(model0, [p1, p1, p1], si, Parallel(n_jobs=4, verbose=6))
    for p, _ in ps:
        print(p)

    print('\nTest evaluation')

    ps = [model0.sample_prior() for _ in range(3)]
    ps = [serve_and_evaluate(model0, p) for p in ps]
    for p in ps:
        print(p, p.LogLikelihood)

    print('Evaluate parallel')

    ps = [model0.sample_prior() for _ in range(3)]
    ps = serve_and_evaluate_parallel(model0, ps, Parallel(n_jobs=4, verbose=4))
    for p in ps:
        print(p, p.LogLikelihood)
