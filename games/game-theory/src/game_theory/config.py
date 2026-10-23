"""Independent strict configuration contract; legacy configs are untouched."""
import json
import yaml
from .plan import MODEL,ENDPOINT,SCENARIOS
from .rules import RULES,legal

SUITE=dict(schema_version=1,model=MODEL,endpoint=ENDPOINT,root_seed=1930,initial_concurrency=4,max_concurrency=8,timeout_seconds=45,attempts_per_scan=3,recovery_scans=2)

def validate_files(root):
    suite=yaml.safe_load((root/'config/suite.yaml').read_text(encoding='utf-8'))
    if suite!=SUITE: raise ValueError('suite.yaml differs from the confirmed finite suite; refusing mixed semantics')
    for s in SCENARIOS:
        expected=dict(schema_version=1,scenario=s,rule_version='1',participants=[3,4,5,6] if s=='public-goods' else [2],history_window=20,objective='maximize own cumulative payoff',identity_visibility='numbers_only')
        actual=yaml.safe_load((root/'scenarios'/s/'config.yaml').read_text(encoding='utf-8'))
        if actual!=expected: raise ValueError('Scenario configuration differs from frozen rules: '+s)
        data=json.loads((root/'scenarios'/s/'scenario.json').read_text(encoding='utf-8'))
        expected_data=dict(rule_version='1',scenario=s,rules=RULES[s],legal_actions={stage:list(legal(s,stage)) for stage in ('proposal','response')} if s=='ultimatum' else list(legal(s)),objective='Maximize your own cumulative payoff over the entire match.')
        if data!=expected_data: raise ValueError('Scenario data differs from execution rules: '+s)
    return suite
