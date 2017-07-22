This wiki page should summarize open ended discussion the team has regarding the POPL18 storyline, TODOs, documentation requirements, experimental and mathematical requirements. Please keep some structure to the page, but also please freely air all your thoughts, baked or not.

# CONFERENCE TARGETING AND DEADLINES

Ming: I think we aim for POPL with the realization that we are much more likely to hit ASPLOS. I need to make sure that ASPLOS decisions come back before the PLDI deadline.

DEADLINES: POPL 7/7, ASPLOS 8/11, PLDI UNK, OSDI UNK, OOPSLA UNK

# DISCUSSION OF MOTIVATION

# DISCUSSION OF CLAIMED KEY CONTRIBUTIONS

* Ming: One thing I think may be important is to *restrict* ourselves to the task of *porting* an operating system to a new or variant machine. That is, we assume that there is a functionally correct kernel for an existing machine that is likely to be close to the new machine we are porting to.

# DISCUSSION OF RELATED WORK COMPARISONS

* Ming: We primarily want to compare our technique of using a number of small synthesis-oriented DSLs _as opposed to_ using a large constructive theorem proving language such as Coq to build kernels. I want to refer to our technique as "bottom-up synthesis" from many little code snippets as opposed to "top-down synthesis" in which a few large proofs are used to construct one or few large modules.

* Margo: we want to work with legacy systems (and barrelfish is a legacy system), and build _generalizable techniques_ that can be applied to any traditional or well-designed non-traditional kernel

* verifiable kernels are great but A DIFFERENT PROBLEM. we want to mitigate the labor required to PORT AN OPERATING SYSTEM.


# DISCUSSION OF TODOS

CASE STUDIES:

mythical man-month
F35
android ports to stuff (ask MOTO friend, qcom folks)
windows team?
kernel.org commits?


MODULES:

context switch (mipsswitch, trap entry)
KLAXONS: calling conventions
syscall after switch
capability conversion (reduce stuff into semantics)

NO PAGING/VM SYSTEM CONSENSUS

context creation
how can we use a mackerel extension? what complex bit vector work do we need to do and where is it done? 
 -- look at places that mackerel is actually used and then look at the stuff that uses those. ARM GIC

## That is, what work do we need to do and how should we split up that work into chunks? 
## then, how do we assign those chunks to team members?


