"""Finite suite enumeration; IDs and streams are independent of scheduling."""
import hashlib
import itertools
import json

STRATEGIES = ('jev', 'cooperate', 'defect', 'random', 'cycle', 'tit_for_tat', 'generous', 'win_stay_lose_shift')
SCENARIOS = ('prisoner-dilemma', 'stag-hunt', 'hawk-dove', 'ultimatum', 'public-goods')
MODEL = 'typesafe/jev-1.13-20260917'
ENDPOINT = 'https://openrouter.ai/api/alpha/decisions'

def stable(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def seed(*parts):
    return int(stable([1930, *parts])[:16], 16)

def conditions():
    result = {}
    def add(scenario, players, rounds, variant='base', **changes):
        for phases in itertools.product((0, 1), repeat=players.count('cycle')):
            phase_iter = iter(phases)
            c = dict(scenario=scenario, players=list(players), rounds=rounds,
                     variant=variant, history_window=20, horizon='known',
                     noise=0, intervention=None, phases=[next(phase_iter) if p == 'cycle' else 0 for p in players])
            c.update(changes)
            c['id'] = stable(c)[:20]
            c['matches'] = (3 if variant != 'base' or rounds != 20 else 5) if any(p in ('jev', 'random', 'generous') for p in players) else 1
            result[c['id']] = c
    for s in SCENARIOS[:4]:
        for players in itertools.product(STRATEGIES, repeat=2):
            for rounds in (1, 20, 100):
                add(s, players, rounds)
    for n in range(3, 7):
        compositions = {tuple([p]*n) for p in STRATEGIES}
        for a, b in itertools.combinations(STRATEGIES, 2):
            for count in range(1, n):
                players = (a,)*count + (b,)*(n-count)
                compositions.update((players, players[::-1]))
        mixed = STRATEGIES[:5] + ('tit_for_tat',)
        compositions.update((mixed[:n], mixed[:n][::-1]))
        for players in sorted(compositions):
            for rounds in (1, 20):
                add('public-goods', players, rounds)
        long = {('jev',)*n}
        for p in STRATEGIES[1:]:
            players = ('jev',)+(p,)*(n-1)
            long.update((players, players[::-1]))
        for players in sorted(long):
            add('public-goods', players, 100)
    for s in SCENARIOS:
        for opponent in ('jev', 'cooperate', 'defect', 'tit_for_tat'):
            players = ('jev', opponent) if s != 'public-goods' else (('jev',)*4 if opponent == 'jev' else ('jev',)+(opponent,)*3)
            add(s, players, 20, 'history-0', history_window=0)
            add(s, players, 20, 'history-5', history_window=5)
            add(s, players, 20, 'unknown-horizon', horizon='unknown')
            add(s, players, 100, 'random-stop', horizon='geometric', continuation_probability=.9)
            if s != 'ultimatum':
                add(s, players, 20, 'execution-noise', noise=.05)
                add(s, players, 20, 'one-intervention', intervention=10)
    return list(result.values())

def totals(items):
    return dict(conditions=len(items), matches=sum(c['matches'] for c in items),
                rounds=sum(c['matches']*c['rounds'] for c in items),
                requests=sum(c['matches']*c['rounds']*c['players'].count('jev') for c in items))
