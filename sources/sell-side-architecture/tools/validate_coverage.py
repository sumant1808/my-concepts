import json, re
d = json.load(open('/home/claude/sell-arch/spec.json'))
b = json.load(open('/home/claude/sell-arch/spec.pre-coverage.bak.json'))
ok, bad = [], []
def chk(c, m): (ok if c else bad).append(m)
comps = [c for L in d['layers'] for g in L['groups'] for c in g['components']]
ids = [c['id'] for c in comps]
old = {c['id']: c for L in b['layers'] for g in L['groups'] for c in g['components']}
new = [c for c in comps if c['id'] not in old]
chk(len(ids) == len(set(ids)), f"component ids unique ({len(ids)})")
chk(set(old) <= set(ids), "every original component still present")
chk(all(c == old[c['id']] for c in comps if c['id'] in old), "original component fields unchanged")
chk(len(new) <= 20 and all(int(c['id'][1:]) >= 104 for c in new), f"{len(new)} new components, ids C104 upward")
gids = [g['id'] for L in d['layers'] for g in L['groups']]
chk(len(gids) == len(set(gids)), f"group ids unique ({len(gids)})")
TARGET = {"L1": 6, "L2": 6, "L3": 7, "L4": 6, "L5": 6, "L6": 6, "L7": 7, "L8": 7}
for L in d['layers']:
    chk(len(L['groups']) == TARGET[L['id']], f"{L['id']} has {len(L['groups'])} groups (target {TARGET[L['id']]})")
chk(all(g['stages'] and all(re.fullmatch(r'S\d|PLATFORM', s) for s in g['stages']) for L in d['layers'] for g in L['groups']), "every group has valid stages")
chk(all(g['components'] for L in d['layers'] for g in L['groups']), "every group has at least one component")
chk(all(len(g['name'].split()) <= 4 for L in d['layers'] for g in L['groups']), "group names max 4 words")
KEYS = list(next(iter(old.values())).keys())
CALM = {"actor", "ecosystem", "system", "service", "database", "network", "ldap", "webclient", "data-asset"}
for c in new:
    chk(list(c.keys()) == KEYS, f"{c['id']} has all fields in order")
    chk(len(c['name'].split()) <= 4 and len(c['does'].split()) <= 14, f"{c['id']} name and does lengths")
    chk(c['calm'] in CALM and c['ac'] and all(a in ('EQ', 'FI', 'FX', 'DR', 'ALL') for a in c['ac']), f"{c['id']} calm and ac valid")
    chk(isinstance(c['external'], bool) and c['sor'], f"{c['id']} external and sor set")
bian = set(open('/home/claude/dl-bian/sd.txt').read().split('\n'))
chk(all(x.strip() in bian for c in new if c['bian'] for x in c['bian'].split(';')), "new BIAN labels verbatim in v10 ServiceDomain list")
ext = {e['id'] for e in d['externals']}
chk(all(l['from'] in set(ids) | ext and l['to'] in set(ids) | ext for l in d['links']), f"every link endpoint exists ({len(d['links'])} links)")
CL = {c['id']: L['id'] for L in d['layers'] for g in L['groups'] for c in g['components']}
chk(all(l['from_layer'] == CL.get(l['from'], 'EXT') and l['to_layer'] == CL.get(l['to'], 'EXT') for l in d['links']), "link layer fields match")
chk({l['thread'] for l in d['links']} == {l['thread'] for l in b['links']}, "thread tags unchanged")
chk(d['links'][:len(b['links'])] == b['links'], "original links unchanged")
chk(d['externals'] == b['externals'], "externals unchanged")
chk([(s['name'], s['verified']) for s in d['standards'][:len(b['standards'])]] == [(s['name'], s['verified']) for s in b['standards']], "original standards and verified flags unchanged")
chk(all(s['verified'] is False for s in d['standards'][len(b['standards']):]), "new standards rows unverified")
F = {"BIAN": "bian", "FIX": "fix", "FpML_CDM": "fpml_cdm", "ISO20022": "iso20022", "SWIFT_MT": "swift_mt", "regs": "regs"}
cov = d['xref_matrix']['coverage']
chk(cov['total_components'] == len(comps) and cov['CALM']['matched'] == len(comps), "coverage totals recomputed")
chk(all(cov[k]['matched'] == sum(1 for c in comps if c[f]) for k, f in F.items()), "coverage counts recomputed")
chk(cov['total_groups'] == len(gids) and sum(v['components'] for v in cov['by_band'].values()) == len(comps), "groups and band totals recomputed")
rows = d['xref_matrix']['layers']
for r, L in zip(rows, d['layers']):
    cs = [c for g in L['groups'] for c in g['components']]
    chk(r['layer'] == L['id'] and r['components'] == len(cs) and all(r['counts'][k] == sum(1 for c in cs if c[f]) for k, f in F.items()), f"xref row {L['id']} recomputed")
for t in d['xref_matrix']['stage_traceability']:
    exp = [f"{L['id']}/{g['id']} {g['name']}" for L in d['layers'] for g in L['groups'] if t['stage'] in g['stages']]
    chk(t['groups'] == exp and t['groups'], f"traceability {t['stage']} matches groups")
regtags = {r for c in new for r in c['regs']}
alltxt = json.dumps(d['standards'])
for txt in ['/home/claude/sell-arch/spec.json', '/home/claude/sell-arch/notes.md', '/home/claude/sell-arch/coverage.md']:
    try: chk(not re.search('[–—]', open(txt).read()), f"no en or em dashes in {txt.split('/')[-1]}")
    except FileNotFoundError: bad.append(f"missing {txt}")
for L in d['layers']:
    print(L['id'], len(L['groups']), 'groups', sum(len(g['components']) for g in L['groups']), 'comps |', ', '.join(f"{g['id']} {g['name']} ({len(g['components'])})" for g in L['groups']))
print('PASS' if not bad else 'FAIL', len(ok), 'checks ok'); [print(' BAD', m) for m in bad]
