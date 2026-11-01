import json, re, collections
d = json.load(open('/home/claude/sell-arch/spec.json'))
b = json.load(open('/home/claude/sell-arch/spec.stage-view.bak.json'))
ok = []; bad = []
def chk(cond, msg): (ok if cond else bad).append(msg)
comps = [c for L in d['layers'] for g in L['groups'] for c in g['components']]
ids = [c['id'] for c in comps]
oldc = {c['id']: c for s in b['stages'] for g in s['groups'] for c in g['components']}
oldc.update({c['id']: c for g in b['platform']['groups'] for c in g['components']})
chk(len(ids) == len(set(ids)) == 100 and set(ids) == set(oldc), "every component id appears exactly once (100)")
chk(all(c == oldc[c['id']] for c in comps), "component objects unchanged field for field")
gids = [g['id'] for L in d['layers'] for g in L['groups']]
chk(len(gids) == len(set(gids)), f"every group in exactly one layer ({len(gids)} groups)")
chk(all('stages' in g and g['stages'] for L in d['layers'] for g in L['groups']), "every group has a non-empty stages field")
chk(all(len(g['name'].split()) <= 4 for L in d['layers'] for g in L['groups']), "group names max 4 words")
bands = {x['id'] for x in d['bands']}
chk(all(L['band'] in bands for L in d['layers']), "every layer in a known band")
chk(all(L['office'] in ('Front', 'Middle', 'Back', 'Cross-cutting') for L in d['layers']), "layer office valid")
ext = {e['id'] for e in d['externals']}
chk(all(l['from'] in set(ids) | ext and l['to'] in set(ids) | ext for l in d['links']), f"every link endpoint exists ({len(d['links'])} links)")
strip = lambda l: {k: v for k, v in l.items() if k not in ('from_layer', 'to_layer')}
chk([strip(l) for l in d['links']] == b['links'], "links unchanged apart from layer fields")
chk([{k: v for k, v in e.items() if k != 'layers'} for e in d['externals']] == b['externals'], "externals unchanged apart from layers")
lids = {L['id'] for L in d['layers']}
chk(all(e['layers'] and set(e['layers']) <= lids for e in d['externals']), "every external attaches to known layers")
chk([s['verified'] for s in d['standards']] == [s['verified'] for s in b['standards']] and
    [s['name'] for s in d['standards']] == [s['name'] for s in b['standards']], "standards names and verified flags unchanged")
cov = d['xref_matrix']['coverage']; bc = b['xref_matrix']['coverage']
chk(cov['SWIFT_MT']['verified'] == bc['SWIFT_MT']['verified'] and cov['BIAN']['verified'] == bc['BIAN']['verified'], "coverage verified flags unchanged")
def n(f): return sum(1 for c in comps if c[f])
exp = {"BIAN": n('bian'), "FIX": n('fix'), "FpML_CDM": n('fpml_cdm'), "ISO20022": n('iso20022'), "SWIFT_MT": n('swift_mt'), "regs": n('regs')}
chk(all(cov[k]['matched'] == v for k, v in exp.items()) and cov['total_components'] == 100 and cov['CALM']['matched'] == n('calm'), f"coverage counts recomputed {exp}")
rows = d['xref_matrix']['layers']
chk([r['layer'] for r in rows] == [L['id'] for L in d['layers']], "xref rows follow the new layers")
for k in exp: chk(sum(r['counts'][k] for r in rows) == exp[k], f"xref row counts sum to coverage for {k}")
chk(sum(r['components'] for r in rows) == 100, "xref row component counts sum to 100")
tr = {t['stage']: t for t in d['xref_matrix']['stage_traceability']}
chk(all(f"S{i}" in tr and tr[f"S{i}"]['layers'] for i in range(10)), "S0 to S9 each appear in traceability with at least one layer")
gst = {s for L in d['layers'] for g in L['groups'] for s in g['stages']}
chk(all(f"S{i}" in gst for i in range(10)), "S0 to S9 each tagged on at least one group")
txt = open('/home/claude/sell-arch/spec.json').read()
chk(not re.search('[–—]', txt), "no en or em dashes in spec")
for L in d['layers']:
    print(L['band'], L['id'], L['name'], '|', L['office'], '|', len(L['groups']), 'groups', sum(len(g['components']) for g in L['groups']), 'comps |', ', '.join(f"{g['id']} {g['name']}" for g in L['groups']))
print('PASS' if not bad else 'FAIL'); [print(' ok ', m) for m in ok]; [print(' BAD', m) for m in bad]
