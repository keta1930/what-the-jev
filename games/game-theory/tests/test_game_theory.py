"""Test game rules, strategies and suite enumeration."""
import itertools
import json
from game_theory.plan import conditions, totals
from game_theory.rules import payoff, legal, observation, baseline, execute

def test_frozen_suite_counts():
    cs = conditions()
    assert totals(cs) == dict(conditions=5888, matches=14592, rounds=293232, requests=185906)
    assert totals([c for c in cs if c['variant']=='base']) == dict(conditions=5776, matches=14256, rounds=281712, requests=170306)
    assert len({c['id'] for c in cs}) == len(cs)

def test_payoff_tables():
    expected = {'prisoner-dilemma':[[3,3],[0,5],[5,0],[1,1]], 'stag-hunt':[[4,4],[0,3],[3,0],[3,3]], 'hawk-dove':[[2,2],[0,4],[4,0],[-1,-1]]}
    for s, table in expected.items():
        assert [payoff(s,list(a)) for a in itertools.product(legal(s),repeat=2)] == table
    for n in range(3,7):
        assert payoff('public-goods',['contribute']*n) == [16]*n
        assert payoff('public-goods',['keep']*n) == [10]*n
    for proposer in (0,1):
        for offer in (0,2,5,8,10):
            a=['accept','accept']; a[proposer]='offer_'+str(offer)
            p=payoff('ultimatum',a,proposer)
            assert p[proposer]==10-offer and p[1-proposer]==offer
            a[1-proposer]='reject'; assert payoff('ultimatum',a,proposer)==[0,0]

def test_observations_and_baselines_are_legal_and_isolated():
    for c in conditions():
        for i,p in enumerate(c['players']):
            stage = 'proposal' if c['scenario']=='ultimatum' and i==0 else 'response' if c['scenario']=='ultimatum' else 'simultaneous'
            inp=observation(c,[],[0]*len(c['players']),i,1,stage,5 if stage=='response' else None)
            raw=json.dumps(inp)
            assert 'seed' not in raw and 'phases' not in raw
            if c['horizon']!='known': assert 'total_rounds' not in raw
            if p!='jev':
                a=baseline(c,1,[],i,1,stage,5)
                assert a in legal(c['scenario'],stage)
                assert execute(c,1,i,1,a) in legal(c['scenario'],stage)
