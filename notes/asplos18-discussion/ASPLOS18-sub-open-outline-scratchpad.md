- Outline related work (classical OS DSLs: packet filters, RPC stubs, etc, verified operating systems, clean slate correct-by-construction, existing bf languages)
- Fill in the holes in our motivation (costs of kernel porting)
- Fill in the holes in our insight (MD code size is small, may be synthesizable! BUT WHY)
- Fill in the holes in our approach (use synthesis aided languages to ease manual burden)

major modifications from POPL outline (which frankly was not POPLy enough anyway)

- ASPLOS aspects of argument: end of per-core scaling, heterogeneity-aided performance, other negative effects of architectural monoculture.
- Off-mainline architectural arguments: the 