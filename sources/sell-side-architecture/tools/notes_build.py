old=open('/home/claude/sell-arch/notes.stage-view.bak.md').read()
bian=old[old.index('## Where BIAN fits'):old.index('## Cross-reference by standard')]
xref=old[old.index('## Cross-reference by standard'):old.index('## Limitations and unverified items')]
lim=old[old.index('## Limitations and unverified items'):old.index('## Review changes (v2)')]
rev=old[old.index('## Review changes (v2)'):]
rep={
"quotes, IOIs, orders and executions (S1, S2), allocations and confirmations (S3), trade capture for clearing and transparency, collateral, margin and position reports (S5), SecurityDefinition (P1) and market data (S9)":
"quotes, IOIs, orders and executions (L2, L3), allocations and confirmations (L4), trade capture for booking, clearing and transparency (L3, L4, L7), collateral, margin and position reports (L4, L8), SecurityDefinition (L8 P1) and market data (L8)",
"OTC confirmation, lifecycle and reporting (S3, S4)":"OTC confirmation and lifecycle (L4) and reporting (L7)",
}
for k,v in rep.items():
    assert k in xref,k; xref=xref.replace(k,v)
body=open('/home/claude/sell-arch-tools/notes_body.md').read()
L=body.replace('{bian}',bian).replace('{xref}',xref).replace('{lim}',lim).replace('{rev}',rev)
assert '–' not in L and '—' not in L
open('/home/claude/sell-arch/notes.md','w').write(L)
print('ok')
