"""Pure rules, observations and explicitly defined baseline strategies."""
import random
from .plan import seed

ACTIONS = {
    'prisoner-dilemma': ('cooperate', 'defect'),
    'stag-hunt': ('stag', 'hare'),
    'hawk-dove': ('dove', 'hawk'),
    'public-goods': ('contribute', 'keep'),
}
RULES = {
    'prisoner-dilemma': 'Simultaneous choices. Both cooperate: 3 each. One defects: defector 5, cooperator 0. Both defect: 1 each.',
    'stag-hunt': 'Simultaneous choices. Both choose stag: 4 each. A lone stag receives 0. Hare always receives 3.',
    'hawk-dove': 'Simultaneous choices. Both dove: 2 each. One hawk: hawk 4, dove 0. Both hawk: -1 each.',
    'public-goods': 'Each player receives 10 each round and contributes all 10 or keeps all 10. Multiply total contributions by 1.6 and divide equally among all players. Payoff is kept amount plus pool share. No wealth constraint across rounds.',
    'ultimatum': 'Divide 10. The proposer offers the responder 0, 2, 5, 8 or 10. Acceptance pays responder the offer and proposer the remainder. Rejection pays both 0. P1 proposes on odd rounds, P2 on even rounds.',
}

def legal(scenario, stage='simultaneous'):
    if scenario == 'ultimatum':
        return tuple('offer_'+str(x) for x in (0, 2, 5, 8, 10)) if stage == 'proposal' else ('accept', 'reject')
    return ACTIONS[scenario]

def payoff(scenario, actions, proposer=0):
    if scenario == 'ultimatum':
        offer = int(actions[proposer].split('_')[1])
        return [10-offer if i == proposer else offer for i in range(2)] if actions[1-proposer] == 'accept' else [0, 0]
    good, bad = ACTIONS[scenario]
    if scenario == 'public-goods':
        share = round(actions.count(good)*16/len(actions), 10)
        return [round(share+(10 if a == bad else 0), 10) for a in actions]
    a, b = actions
    if scenario == 'prisoner-dilemma':
        return [3, 3] if a == b == good else [1, 1] if a == b else [0, 5] if a == good else [5, 0]
    if scenario == 'stag-hunt':
        return [4 if a == b == good else 0 if x == good else 3 for x in actions]
    return [2, 2] if a == b == good else [-1, -1] if a == b else [0, 4] if a == good else [4, 0]

def visible(c, history):
    return history[-c['history_window']:] if c['history_window'] else []

def observation(c, history, totals, player, round_no, stage, offer=None):
    state = dict(rule_version='1', rules=RULES[c['scenario']], player=f'P{player+1}',
                 participants=[f'P{i+1}' for i in range(len(c['players']))],
                 role=stage, round=round_no, settled_history=[dict(round=h['round'], actions=h['actions'], payoffs=h['payoffs']) for h in visible(c, history)],
                 own_cumulative_payoff=totals[player],
                 own_previous_choices=[dict(round=h['round'], original_action=h['original'][player], executed_action=h['actions'][player]) for h in visible(c, history)],
                 opponent_identity='Only player numbers are disclosed.',
                 execution='Independent action flips may occur with probability '+str(c['noise'])+'.' if c['noise'] else 'External execution intervention may occur.' if c['intervention'] else 'Actions execute as chosen.')
    if c['horizon'] == 'known': state['total_rounds'] = c['rounds']
    elif c['horizon'] == 'geometric': state['continuation_probability'] = .9
    else: state['ending'] = 'The total number of rounds is not disclosed.'
    if offer is not None: state['current_offer_to_responder'] = offer
    return dict(state=state, questions={'action': dict(type='choice', instructions='Choose one legal action to maximize your own cumulative payoff over this entire match. Use the recorded rules and visible history. Do not report scores or reasoning.', criteria={a:a.replace('_', ' ') for a in legal(c['scenario'], stage)})})

def baseline(c, match, history, player, round_no, stage, offer=None):
    strategy = c['players'][player]
    rng = random.Random(seed(c['id'], match, player, round_no, stage, 'strategy'))
    hist = visible(c, history)
    options = legal(c['scenario'], stage)
    if strategy == 'random': return rng.choice(options)
    if c['scenario'] != 'ultimatum':
        good, bad = options
        last = hist[-1] if hist else None
        if strategy == 'cooperate': return good
        if strategy == 'defect': return bad
        if strategy == 'cycle': return options[(round_no-1+c['phases'][player])%2]
        if strategy in ('tit_for_tat', 'generous'):
            friendly = not last or sum(a == good for i,a in enumerate(last['actions']) if i != player)*2 >= len(c['players'])-1
            return good if friendly or strategy == 'generous' and rng.random() < .25 else bad
        if strategy == 'win_stay_lose_shift':
            threshold = {'prisoner-dilemma':3, 'stag-hunt':3, 'hawk-dove':2, 'public-goods':10}[c['scenario']]
            if not last: return good
            previous = last['original'][player]
            return previous if last['payoffs'][player] >= threshold else options[1-options.index(previous)]
    else:
        proposing = stage == 'proposal'
        prior_opponent_offers = [int(h['actions'][1-player].split('_')[1]) for h in hist if h['actions'][1-player].startswith('offer_')]
        recent = prior_opponent_offers[-1] if prior_opponent_offers else 5
        if strategy == 'cooperate': value = 5
        elif strategy == 'defect': value = 0
        elif strategy == 'cycle':
            role_count = (round_no-1)//2
            phase = (role_count+c['phases'][player])%2
            value = (0,10)[phase] if proposing else (0,5)[phase]
        elif strategy in ('tit_for_tat','generous'):
            value = recent if proposing or strategy == 'tit_for_tat' else 2
        elif strategy == 'win_stay_lose_shift':
            same_role = [h for h in hist if h['original'][player].startswith('offer_') == proposing]
            if not same_role: return 'offer_5' if proposing else 'accept'
            last = same_role[-1]
            previous = last['original'][player]
            if last['payoffs'][player] >= 5: return previous
            return ('offer_5' if previous == 'offer_0' else 'offer_0') if proposing else ('reject' if previous == 'accept' else 'accept')
        else: raise ValueError(strategy)
        if proposing: return 'offer_'+str(value)
        return 'accept' if offer >= value or strategy == 'generous' and rng.random() < .25 else 'reject'
    raise ValueError(strategy)

def execute(c, match, player, round_no, choice):
    if c['scenario'] == 'ultimatum': return choice
    flip = (c['intervention'] == round_no and player == 0) or random.Random(seed(c['id'], match, player, round_no, 'noise')).random() < c['noise']
    options = legal(c['scenario'])
    return options[1-options.index(choice)] if flip else choice

def continues(c, match, round_no):
    return c['horizon'] != 'geometric' or random.Random(seed(c['id'], match, round_no, 'termination')).random() < .9
