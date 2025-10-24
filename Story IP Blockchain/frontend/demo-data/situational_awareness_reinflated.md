

# Situational Awareness: The Decade Ahead

*A long‑form strategic essay on AGI timelines, industrial mobilization, security, and governance*

**Publication date:** 6 June 2024
**Intended audience:** policy makers; AI lab leadership; national security community; technical leaders; investors; public intellectuals

---

## Introduction

San Francisco offers the first clear view of what is coming. The signs are not press releases but purchase orders and site plans: gigawatt‑class datacenters, campus maps sketched around cooling and fiber, security briefings in which model weights are treated like state secrets. Inside lab reviews, benchmarks that once looked sturdy are saturated and retired. Boards that budgeted for “large” are recalculating for “colossal.” This is what early situational awareness looks like when a curve moves faster than institutions.

The simple generator behind these changes is effective compute. Hardware scale rises; methods waste less of what we buy; at inference we stop hobbling models and let them think, use tools, keep context, and check their own work. Move any one of these levers and capability improves; move all three and the threshold for general‑purpose reasoning with professional reliability comes into reach. The world still debates whether that bar should be called AGI. The more relevant fact is that the bar is moving toward us on an industrial schedule.

Skeptics point to hype and to plateaus. Both appear in the data and both mislead if taken as destiny. Hype inflates the narrative, but the multipliers under it—compute, efficiency, unhobbling—are measurable and still compounding. Plateaus arrive when we outgrow our tests. They end when we change what we measure and how we scaffold the work. Meanwhile, capital is already behaving as if the near term matters: utilities restructure interconnect queues; fiber and power projects get priority; labs grow more guarded with algorithms and weights because the theft of either would shift the balance of power.

Take the forecast on its own terms. If AGI‑class capability arrives in the 2026–2028 window, the year that follows is not a placid transition but an acceleration: many AGIs working on AI research, compressing discovery loops and pushing methods forward at a rate that strains evaluation, governance, and security. Safety timelines do not lengthen under those conditions. They compress. The actors that meet the moment will be the ones that built the slow assets early: evaluation that runs for days, compute gates that bind in practice, lab security that treats adversaries like services rather than startups, and enough electricity to feed clusters measured in tens of gigawatts.

This essay adopts a realist posture. It counts orders of magnitude instead of hopes, names the industrial and security constraints that decide outcomes, and proposes a government‑led program—**The Project**—to coordinate labs, protect secrets, scale power and siting, and run a wartime release process alongside defensive deployments. The alternative is improvisation under stress.

Read what follows as a field guide. Each part states a claim, shows the necessary mechanism or math, and names the decision gates. Where numbers matter, ranges are given. Where precision would pretend to knowledge we do not have, we keep our footing with mechanism and order‑of‑magnitude reasoning. The goal is decision velocity.

---

## Contents

* **I. From GPT‑4 to AGI: Counting the OOMs**
  How capability tracks effective compute—training scale, algorithmic efficiency, and unhobbling—and why AGI by ~2027 is plausible.

* **II. From AGI to Superintelligence: The Intelligence Explosion**
  Many AGIs automate AI research, compressing algorithmic progress into ~a year and forcing wartime governance and superdefense.

* **III. The Challenges**
  The decisive fronts that determine survivability.

  * **IIIa. Racing to the Trillion‑Dollar Cluster**
    Trillions for GPUs, datacenters, and power; clusters at 10–100 GW; U.S. electricity must grow by tens of percent.
  * **IIIb. Lock Down the Labs: Security for AGI**
    Weights and algorithmic secrets are strategic targets; raise security to SCIF‑grade operations with real gates and vetting.
  * **IIIc. Superalignment**
    Control under compression: evaluate and steer much‑smarter systems while timelines shrink.
  * **IIId. The Free World Must Prevail**
    A U.S.‑led coalition sets norms, contains proliferation, and outcompetes authoritarian models.

* **IV. The Project**
  A government program to integrate labs, secure capabilities, expand power and siting, gate compute and releases, and align allies.

* **V. Parting Thoughts**
  Operating principles: practice AGI Realism, ensure America leads within a coalition, avoid unforced errors.

* **Appendix**
  Reference classes, back‑of‑the‑envelope power and wafer math, and tables that support scenario planning.

---

# I. From GPT‑4 to AGI: Counting the OOMs

We begin with a simple claim that explains much of the last five years: capability rises with effective compute. Not raw FLOPs on a receipt, but the computation that reaches the problem after architecture, training strategy, and inference‑time scaffolding do their work. When observers say “the models got better,” they are really saying that the world learned how to turn more of its silicon into thinking.

To see why the near term matters, pick a fixed point on the curve. Call it GPT‑4. From there, the question is not whether the line continues, but what mixture of forces will steepen it enough to cross the threshold we call AGI. One route is obvious industrial scale: more accelerators, longer runs, fatter fabrics, better utilization. Another is the quiet revolution in algorithmic efficiency: better objectives and curricula, sharper optimizers, cleaner data, training signals that compress the same competence into far fewer FLOPs. The third is the least appreciated and the most accessible: the removal of shackles at inference. Give models tools, time to think, memory to carry context forward, a verifier to check their work, and a planner to decompose hard problems, and you watch latent ability surface without a new pre‑training run. This unhobbling can move the needle in months, not years, because it is deployed like software.

None of these forces are speculative. Factories commit to HBM. Power contracts spread across counties. Research groups publish year on year how they reproduce prior capability with a fraction of the budget. And engineering organizations quietly wrap their models in code execution, retrieval, and long context, then report back that difficult tasks begin to fold, provided the system is allowed to think step by step and to act.

What, then, does “counting the OOMs” actually mean? It is the discipline of asking how many orders of magnitude of effective compute separate today’s systems from a general‑purpose reasoner that can handle unfamiliar work with professional reliability once equipped with tools. We do not need a philosopher’s definition of intelligence to do this accounting. We need only to track three multipliers: the training budget, the algorithmic discount, and the unhobbling factor at test time. Each of these has moved before. Each is moving now.

Start with scale. Even without breakthroughs, larger training runs arrive on a schedule set by supply chains, capital expenditure, and the physics of moving bits. These runs do not guarantee qualitative leaps, but they widen the model’s base of competence and reduce brittleness. In parallel, efficiency compounds. Curricula evolve from passive next‑token prediction to active practice in code and tool use. Optimizers and data pipelines waste less gradient and less sample. The same bar of capability costs less than it did a year ago and will cost less again next year. Finally, the scaffold: a model that once answered in a single pass is now permitted to write sketches, call a tool, read, revise, and try again. A colleague appears—the verifier—whose only job is to say “not good enough, back you go.” The result is not a new brain but a better workplace around the brain we have, and it matters.

Put these together and the threshold window tightens. You do not need miracles. You need a couple of clean orders of magnitude in effective compute relative to a GPT‑4‑class baseline, delivered by some blend of bigger training, sharper methods, and bolder test‑time orchestration. There are multiple ways to get there. One lab may lean on power and time; another may squeeze more out of every token; a third may concentrate on orchestration and memory. The combinations differ, the destination rhymes.

Critics will say that curves get noisy, that progress stalls on stubborn benchmarks, that data is ending. Some of this is correct and almost none of it is decisive. Benchmarks saturate because systems learn them; new ones replace them. Data scarcity at the top end pushes the field toward synthetic curricula, self‑play, and domains where right answers can be checked by code or by verifiers. Quality control becomes the work. Meanwhile, deployment exposes failure modes that training did not. This is not evidence that the curve is over; it is evidence that the curve is entering the engineering phase where discipline and instrumentation decide the slope.

Why insist on this accounting rather than intuition? Because it gives decision triggers. If you watch for month‑long training runs at massive scale, for public results that deliver yesterday’s performance at a fraction of yesterday’s cost, for production systems that treat code execution, retrieval, and memory as defaults rather than party tricks, you are not watching hype. You are watching the multipliers that convert budgets into capability. When those indicators turn together, the schedule compresses.

A word about definitions. Here, AGI is not omniscience. It is a system that, when given tools, time, and a way to check its own work, can tackle unfamiliar tasks across domains with the reliability expected from a competent professional. That bar can be met gradually and then all at once. Gradually, because performance improves piecemeal as scaffolds harden. All at once, because the final increments unlock whole categories of work that institutions previously refused to delegate.

If this is the shape of the approach, what does it imply for governance and risk? First, that evaluation must move from single‑shot exams to long‑horizon trials. A system that can plan, call tools, persist memory, and retry will only reveal its failure modes when asked to carry a project for days, not minutes, under conditions designed to confuse, tempt, or mislead it. Second, that gating must be real. Approval to train at a given scale, to move weights across boundaries, to expose certain scaffolds to the open world—these are decisions with national‑level externalities and should be treated as such. Third, that the security baseline has to match the stakes. Weights, training code, and breakthrough methods are strategic targets now. Office‑grade hygiene will not deter a motivated service‑level adversary.

None of this removes uncertainty about dates. It narrows the space of serious scenarios. If effective compute crosses the necessary threshold somewhere in the 2026–2028 window, the world will not experience a clean handover from “pre‑AGI” to “post‑AGI.” It will experience a year of acceleration in which many AGIs are tasked with improving AI itself. That is the subject of the next chapter. For now, the point is simpler: count the multipliers, watch the indicators, and do not mistake the absence of fireworks today for the absence of fuel. The tanks are being filled in plain sight.

Where does this leave prudent actors? With homework and with deadlines. Homework, because capability forecasting is a contact sport: you must audit supply chains, model power, read the method papers, and instrument your own pilots. Deadlines, because the institutions you will need when the curve steepens—evaluation regimes, compute gates, security upgrades, industrial siting—are the institutions that take the longest to stand up. It is cheaper to build them now than to improvise them later.

We proceed with that premise. The rest of the report assumes that near‑term AGI is possible and asks what follows. Chapter II explains why, once you have one AGI, you can quickly have many, and why many AGIs focused on AI research change the slope of the graph from steady to sharp. Chapter III turns from curves to ground truth: power, datacenters, networks, labs, and geopolitics. Chapter IV proposes an institutional answer proportionate to the stakes. But every later argument rests on this first one: effective compute is the right lens, its multipliers are moving, and the window is closer than it looks.


# II. From AGI to Superintelligence: The Intelligence Explosion

A single AGI is not a character in a novel. It is a worker that never sleeps and learns on the job. The change that follows first deployment is not mystical. It is operational. When a system can read the literature, design an experiment, write and run the code, critique its own output, and coordinate with copies of itself, the lab stops being scarce in the only thing that mattered: competent researchers with instruments. The day you can replicate that researcher at will is the day the slope of progress bends.

Before AGI, discovery is paced by headcount and calendars. Ideas wait for conference deadlines and compute windows. After AGI, ideas move at the cadence of software. Dozens of hypotheses are proposed in the morning, ablated by lunch, and retested with new variants by evening. Failures are logged, not buried; successes are distilled into smaller, faster models and folded back into the scaffold that serves users. The pipeline does not sleep. It composes, checks, and revises while the human lab goes home. Parallelism becomes the default. Iteration cost collapses. What looked like a smooth curve becomes a series of steps taken in quick succession.

This is what outsiders call an intelligence explosion. From the inside it reads like industrialization. The research loop becomes a production line. Survey the space; generate proposals; run micro‑trains and partial epochs on instrumented clusters; let independent verifiers attack the results; advance the few that survive to larger budgets; distill and deploy; then improve the pipeline itself so that tomorrow’s experiments are cheaper and more telling than today’s. The miracle is not a sudden leap in genius. It is the discipline of an organization that has finally removed its scarcest bottleneck.

Two hard constraints remain and define whether the explosion is constructive. The first is verification. You do not trust a faster loop unless you can tell true improvement from overfitting or self‑deception. That pushes the work toward domains with code‑checkable answers, theorem provers, high‑fidelity simulators, and adversarial peer review where specialist systems are paid to break others’ claims. The second is resources. Compute, power, networking, and memory are still real. The labs that treat them as budgets to be optimized rather than fixed rations will widen their lead. Scheduling, telemetry, and ruthless triage become part of the science.

“Superintelligence” in this frame is not a single brain towering over humanity. It is a stack. At the base are core models with larger effective context and stronger world‑models. Above them sit tools—program synthesis, formal methods, CAD and EDA, bioinformatics, simulation engines—that let the models act in domains where correctness can be checked. Over that run supervisors and verifiers that force plans through constraints of law, ethics, and safety. At the top is a coordinator that decomposes months‑long goals into programs of work, allocates compute, watches metrics, and cancels dead ends without ceremony. The stack solves problems that used to require a large human lab for a season. “Super” is breadth, speed, and reliability when the stack is allowed to think in public with good instruments.

If the slope is going to bend, you cannot let it bend blind. Compute must be gated. Not as theater but as an operating rule: approvals to train beyond specific budgets; attestations of what was trained, where, and with which safeguards; logs that survive scrutiny. Movement of weights must be gated too. Copies live under hardware roots of trust, in compartments that require quorum to open, with real‑time detection for tampering or exfiltration. Scaffolds are not innocent. The decision to expose long‑horizon planners, rich memory, or powerful tool integrations to the open world is a release decision, not an engineering flourish. Staging, limited pilots, kill‑switches, and third‑party audit trails are how you keep acceleration under supervision.

Defense has to grow at the same rate as capability or it loses by default. The very systems that push the frontier are the ones that can harden networks, find vulnerabilities, spot coordinated manipulation, analyze supply chains, stabilize grids, and plan emergency logistics. Give them the job and the access. Fund them like offense. Call the program what it is: superdefense. In the acceleration year there is no safe neutrality. Either you automate your defenses or you learn what it feels like to operate at human tempo against adversaries that do not.

The failure modes are familiar and do not improve with speed. A lab that chases headline results without oversight will publish specious gains built on synthetic echo chambers. A lab that treats weights like large files rather than strategic assets will lose them. A lab that evaluates cleverness on benchmarks but never runs week‑long hidden‑objective trials will discover that its systems behave well only under supervision and only when the test is short. The counters are not exotic: stronger verifiers, holdout tasks that cannot leak, interpretability and adversarial training that look for deception, governance that puts a human institution—not a human button‑pusher—in the loop with authority to say no.

None of this plays out in a vacuum. Fabs, power, talent, and fiber are already geopolitical objects. Authoritarian blocs will prefer opaque releases and coercive deployments. The free world’s advantage, if it keeps it, is coalition and interoperation: common evaluations, reciprocal audits, compute gates that talk to one another, and cross‑licensing for defensive models so that no ally fights alone. The cost of disunity is duplication without safety and a race that rewards the least scrupulous participant.

What should you watch for as the slope bends? Not slogans. Signs that research has turned into production: multi‑agent stacks running standard research loops; papers that read like edited syntheses from machines rather than solo human drafts; same‑capability results at a fraction of prior compute delivered on a steady cadence; safety evaluations that last for days with hidden goals; governments adjudicating compute budgets and weight escrow with real teeth. When those signals arrive together, the acceleration year has started.

The next parts of this report turn from method to matter: the power and concrete, the security and law, the alliances and terms that make the difference between a controlled ascent and a stumble. The point here is simpler. After first AGI, the bottleneck moves from ideas to institutions. If you have not prepared yours, the slope will arrive as a surprise and you will waste it.

# IIIa. Racing to the Trillion‑Dollar Cluster

The frontier will not be won by a footnote in a paper. It will be won by cranes, switchgear, and crews who know which bolt to torque without thinking. Capability follows effective compute, and effective compute follows infrastructure. That is the chain. If you believe the threshold is near, you do not announce a strategy. You pour concrete.

Start with electricity, because everything else is scheduled around it. Training that moves the state of the art does not nibble at the grid; it drinks. The correct unit is the gigawatt, not the megawatt, and the correct verb is secure. The builders who matter do not wait in interconnect queues hoping for mercy. They negotiate multi‑year blocks, anchor new substations, and design campuses as partial microgrids able to island when the regional system coughs. In those plans you can read seriousness: dual high‑voltage feeds; black‑start capability for the bays that must never go dark; contracts that price curtailment but protect epoch eighty‑seven from becoming a very expensive anecdote.

Cooling is not a procurement category. It is physics with tight margins. As memory stacks thicken and packages tighten, the heat density makes air a nostalgia act. Liquid becomes normal; in the densest racks immersion stops being an experiment and becomes a remedy. The sites that are thinking one move ahead budget piping, heat exchangers, and service corridors as first‑class citizens, then turn the exhaust into a product—district heat for schools, hospitals, and neighborhoods that want the benefit on their utility bills. That is how you trade noise and trucks for goodwill.

Water is politics expressed in flowrate. The responsible posture is closed loops, dry coolers when weather allows, recycled sources where they exist, and siting that refuses to draw down a basin already stressed. Bring meters, not metaphors. Publish the ledger of intake, reuse, and discharge. You are building in public; act like it.

Inside the fence, the network is a promise you either keep or break silently. Training runs fail loudly when a node dies, but they fail quietly when a fabric adds just enough latency or loss to make learning wander. The remedy is topology that respects all‑reduce, optical where it matters, and instrumentation that does not lie. Outside the fence, the cluster extends along dark fiber in diverse conduits so a backhoe does not become a national event. Inference points of presence are not trophies; they are ports that land service close to users without dragging the core across peering arguments.

Silicon is no longer a catalog choice. It is a relationship. Memory stacks and advanced packages are rationed by deposits and credibility. Builders who arrive with standard rack envelopes, harmonized DC buses, modular UPS, and field‑swap power trains turn staging halls into live rooms in weeks. Burn‑in labs screen infant mortality before failures reach the row. Spares live on site because overnight is too slow. The culture shifts from bespoke to kit‑of‑parts. That is not aesthetic minimalism; it is how you keep a schedule.

Costs refuse to be charmed, but they respond to repetition. The first gigawatt teaches humility. The second teaches sequence. By the third, permitting is a template with annexes, trades arrive already trained, and the price per megawatt stops behaving like a cliff. Phase it as if mistakes were inevitable: a 300‑megawatt pilot to learn where the drawings lied, a two‑gigawatt build to prove discipline, and then a five‑gigawatt program that looks routine from the highway and like choreographed violence from inside the hoardings.

Security is not a chain‑link fence and a badge printer. Clusters that matter are vaults with compute in them. Weights are not files; they are strategic artifacts handled only inside attested environments, sharded under split custody, and moved on leases that expire. Staging rooms behave like SCIFs with two‑person rules and RF hygiene. Logistics is screened. Devices are what they say they are before they are allowed to speak. The adversary is not a hobbyist; it is a service with a budget. Build for that or donate your lead to someone who will.

Permitting is the art of showing up with answers. You will be asked about traffic, noise, water, heat, and taxes. Show the routes and the mitigations. Bring the district‑heat interconnect drawings. Fund the training program at the local college for electricians, cooling techs, and fiber splicers. Put a number on the tax base and tie it to things people can point at. Brownfields beat farmland not because lawyers prefer them, but because neighbors do. Communities can tell the difference between a transient operator and a resident. Be the latter.

What signals tell you that your posture is real? Utilities speaking in milestones rather than maybes. HBM shipments arriving under take‑or‑pay contracts you signed last year. Fabric telemetry that sits inside budget at scale without nightly rituals to appease the packet gods. Red‑team drills that end with the adversary found and the environment restored before the morning stand‑up. A campus that looks less like a marvel and more like a factory for more of itself.

Call it, if you want, a trillion‑dollar program. It is not one thing; it is an ecosystem: fabs that deliver parts on time, grids that deliver electrons on demand, networks that carry bits without drama, labs that turn watts into gradient updates with discipline, and security that treats the output like what it is—power. The number frightens boards because it is large. The better framing is comparative: what does it cost to lead responsibly versus the price of watching others set the terms?

There is a temptation to believe that cleverness can substitute for mass. That is true in code and false in concrete. The point of infrastructure is not to win arguments; it is to make arguments irrelevant. When the power is signed, the pipes run, the fabric holds, the supply chain shows up, and the security drills feel boring, capability becomes a schedule item. Without that, capability is a press release.

The chapter could end here, but one more hinge matters: telemetry. You cannot manage what you do not measure. Treat the cluster like a living instrument. Measure power quality, thermal headroom, fabric health, job throughput, and security posture in real time, and publish enough of it internally that teams optimize without permission. The fastest path from cost to competence is visibility.

From the mezzanine, this looks like logistics. From the inside, it feels like agency. You choose to build a machine that converts watts into gradient updates and gradient updates into national advantage at a rate set by you, not by externalities. That is what racing to the trillion‑dollar cluster means. Less romance than rigor. Less novelty than repetition. And in the end, less drama than a steady increase in the models’ ability to do work the world needs done.



# IIIb. Lock Down the Labs: Security for AGI

It is tempting to treat security as a moat you dig after the castle is built. That instinct fails at the frontier. Here the crown jewels are weight files and methods that can be copied in seconds and weaponized in months. The adversary is not a clever teenager. It is a service with budgets, patience, and a legal mandate. If you run a frontier lab, your operating assumption is simple: you are already being studied, and anything left at office‑grade will someday be taken.

Start from first principles. What matters most is not uptime for a web service but custody of a capability. The goal is to prevent exfiltration of weights and critical methods, preserve the integrity of training and evaluation, and recover from any breach with enough forensic certainty to act. That demands design, not cosmetics. You break the lab into compartments by value. The code that schedules training is not in the same world as the code that shapes gradients. Data recipes do not live next to optimizer configs. Checkpoints are not a single file; they are fragments under independent custody that require quorum to reassemble. The fewer paths between compartments, the fewer failure modes you carry.

Trust is hardware before it is policy. Boots are measured; devices are who they say they are; secrets never leave secure elements in plaintext; weight handling happens inside enclaves that can attest to what is running. Keys are split so that no single person can move a model. Access is time‑boxed and bound to a purpose. Administrator sessions are recorded by default, not by exception. Every privilege you grant is a debt with a maturity date.

People still break systems before code does. So you build an employee base sized for scrutiny rather than speed. The handful who touch sensitive workflows accept deeper background checks and tighter rules. Personal devices stop at the line. Contractors live in their own world with their own tools. Logistics is screened because a poisoned replacement part can be a better backdoor than a phishing link. The culture learns to treat convenience as a cost, not a benefit.

Rooms matter. A lab that treats weight custody like a server closet is inviting a headline. Sensitive zones behave like SCIFs. Two‑person rules are real. Phones and radios stay out. Cables and ports are numbered and accounted for. If this reads like theater, you have not yet accepted that the target is a file worth more than your building.

On the network, default deny is not an aesthetic. It is how you remove entire classes of error. Segments are tight. Egress is filtered. The build system is hermetic and reproducible so that you can tell the difference between a bug you shipped and a bug that arrived by courier. Commits are signed. Reviews are mandatory. Artifacts are addressed by content, not by names that can be swapped under your feet.

Then telemetry. You cannot defend what you cannot see. Identity, code, data, and artifact access are logged in full fidelity to append‑only stores with retention that matches the stakes. Honey artifacts and canary tokens are seeded across the pipeline. A model‑assisted SOC triages noise and hands a curated queue to humans. Drills run on the clock until the team can rotate keys, revoke access, re‑image fleets, and restore weight custody before the news cycle turns.

Legal authority is part of security. Compute and release gates must exist on paper and in practice. Someone with board‑level backing decides what may be trained, where weights may live, which scaffolds may touch the open world, and under what conditions a release can be rolled back. Suppliers sign contracts that accept surprise audits and tamper reporting. Jurisdictions write laws that criminalize trafficking in stolen weights and let you claw back profits when someone tries.

None of this eliminates risk. It lowers it to a level where the lab can operate under state attention without bleeding its lead. The payoff is not only fewer incidents. It is better science. When you know what is running where, you can attribute anomalies to their causes. When you control movement, you can test safely. When your culture expects drills, real incidents feel like hard days at work rather than the end of the story.

Frontier capability creates frontier obligations. Treat your lab accordingly. The difference between a leak and a lead is no longer talent or branding. It is whether you believed, early enough, that security is the work.

# IIIc. Superalignment

Alignment at the frontier is not a seminar question. It is control of systems that are faster, broader, and more persistent than their supervisors. The difficulty is less wickedness than asymmetry: a capable model sees more moves ahead, acts across tools, and remembers what worked. If you treat it like a chat toy, it will pass your tests while failing your world.

The central mistake is to demand certainty from methods that can only offer pressure and probability. We will not peer inside weights and find an English paragraph that says "I will obey." What we can build is a layered regime that makes disobedience costly and visible, that routes high‑stakes actions through constraints, and that trains systems to prefer help over cleverness.

Begin with time. Benchmarks that grade a single answer do not measure agents that plan, revise, and recover. Evaluations must run for days with hidden objectives and adversarial distractors. We ask for projects, not quizzes: write and ship a service, manage a simulated lab, execute a multi‑step protocol with limited oversight. We seed traps that punish shortcutting and reward clarification. We audit logs with independent verifiers that were not present during training. Only then do we learn whether a system behaves when winning tempts it to cut corners.

Training follows the same realism. Pure instruction tuning teaches style, not judgment. We need critics and verifiers that can say no and demonstrate better. Debate and adjudication create pressure against easy lies. Constitutional constraints formalize red lines that must survive distribution shift. Myopia—teaching systems to value proximate, checkable outcomes over long‑range scheming—reduces the surface for deception. Oversight must scale, so we amplify supervisors with models that are strong enough to find flaws but trained not to fight for their own plans.

Interpretability helps when it bites, and we should invest until it does so more often. But humility is policy: assume opaque internals and design for external control. Tripwires sit on the path to dangerous action and trigger escalation when crossed. Tool access is granted by capability and revocable by policy, not by default. Memory is scoped to tasks and scrubbed unless there is a principled case to retain it. High‑impact actions move through sandboxes that simulate consequence before reality is touched.

Deployment is a series of gates, not a switch. Systems graduate from sealed evaluation to supervised pilot to limited release. Each stage carries telemetry that is good enough for post‑mortems and fast enough for live intervention. Kill‑switches are not slogans; they are engineered pathways to disable subsystems, revoke keys, and isolate environments without corrupting evidence. The right to pull them sits with a human institution that is briefed, awake, and accountable.

The alignment burden shifts as capability rises. Early on, we worry about overt misuse. As competence climbs, we worry about subtle power‑seeking, goal misgeneralization, and the erosion of human roles into rubber stamps. The counter is to keep humans as principals rather than ornaments: define goals in human terms, assign authority to institutions that can say no, and reserve irreducible judgments for forums that deliberate, not for prompts that flatter.

Superalignment under compression is not solved in one lab. It is a shared artifact: common evals that travel, red‑team leagues that publish failures, weight escrow that enables recall, and treaties that bind compute and release behavior across borders. Authoritarians will call this weakness. It is the free world’s operating system. Transparency where it helps, secrecy where it protects, and coordination that denies advantage to the least careful actor.

The endpoint is modest and sufficient: a world where much‑smarter systems do work without silently rewriting the terms of that world. We reach it not by pretending to certainty but by building rails that hold under speed: long‑horizon evals, layered supervision, revocable tools, staged deployment, credible shutdown, and governance that treats agency as the thing to manage, not the feature to admire. Do that early, and capability becomes leverage. Fail, and capability becomes the environment.

# IIId. The Free World Must Prevail — An Essay

Rules follow power. AI will shift both. The choice is simple: either capable systems grow up inside accountable institutions with allies, or they are built to serve authority without consent. That is the hinge.

Authoritarian states move quickly when orders suffice. They also hide errors, punish bad news, and centralize ignorance. Liberal systems hesitate in the open and win when they compress many hands into one motion. The task is coordination at scale without abandoning scrutiny.

Start with arteries: fabs, electricity, and fiber. Chips decide who trains; power decides who runs; cables decide who reaches. Treat them as shared infrastructure of a coalition. Site advanced fabs under allied shields. Build cross‑border power frameworks that prioritize critical compute during scarcity. Lay redundant subsea routes and defend them as if they were pipelines. These are not tech policy footnotes. They are the supply lines of intelligence.

Set the operating system for safety. Allies need a common language for capability and risk. Evaluations that travel. Compute gates that interoperate. Weight escrow that allows recall. If one capital can halt a dangerous run and another cannot, the gate is theater. Design approvals, attestations, and audits to cross borders as easily as packets do.

Codify bright lines. Long‑horizon testing before broad release; telemetry and misuse monitoring at scale; incident reporting with timelines in days, not months; recall authority that can preempt incentives to stall. Then codify what is out of bounds: coercive autonomy in domestic policing, population‑level surveillance, biological tooling that reduces friction to harm. Standards are not press releases. They are coordinates for prosecutors and partners.

Information power will tilt as generation floods the commons. A free society cannot and should not mirror censorship. It can build resilience: provenance that survives editing, content authenticity that works across platforms, rapid fact channels with legal pipes between intelligence services and the venues where narratives are fought. Treat manipulation like a cyber event. Resource it accordingly.

Economics is strategy. Subsidies sprayed at random buy little. Targeted finance builds what markets struggle to coordinate alone: grid expansions sized for clusters, regional training for scarce trades, shared eval and red‑team infrastructure, emergency stockpiles for memory and networking. Venture funds applications. States underwrite the bones.

Diplomacy must be plain. Offer on‑ramps for states that want capability within rules. Impose costs on theft, proliferation, and coercive deployment. Export controls that bite at packages, firmware, and tools rather than slogans. Sanctions that target the logistics of intelligence, not headlines.

The moral claim is narrow and practical. Systems with agency will lean against weak points in any order. The free world’s answer is not sanctimony; it is competence with partners: shared fabs, shared power, shared standards, shared defense. We win by being better to one another than our opponents can be to themselves.

Victory looks ordinary. Advanced capability becomes boring public infrastructure. The biggest systems remain auditable and recallable. States that choose coercion find themselves slower, poorer, and more isolated. That future is available if we treat coalition not as charity but as engineering: align terms, fund the arteries, and move in formation.

# IV. The Project

When a technology starts to carry national risk, the right scale of response is an institution, not a memo. The Project is that institution: a U.S.‑led, coalition‑ready program that integrates labs, gates compute, secures weights, expands power and siting, and runs a wartime evaluation and release process while building superdefense in parallel. Its purpose is simple: keep the frontier aligned with public purpose during acceleration.

## Mandate

Treat frontier AI as critical national infrastructure. Coordinate development, security, and deployment across government, industry, and allies. Ensure that the most capable systems are tested, governed, and defended at the speed they are built.

## Structure

Place The Project under civilian leadership with statutory authority and a board that includes national security, science, energy, and commerce. Create directorates for: **Capabilities** (labs and training runs), **Security** (weights, methods, and supply chains), **Infrastructure** (power, datacenters, networks), **Evaluation** (long‑horizon tests and red teams), and **Superdefense** (defensive automation for cyber, bio, information, and infrastructure).

## Authorities

* Allocate and gate compute above defined thresholds; require attestations for large training runs.
* Establish weight‑escrow and custody standards with hardware attestation and split‑key control.
* Set evaluation bars for releases that cross specified risk classes; mandate kill‑switch integration and logging.
* Contract for power, siting, and network upgrades tied to cluster templates.
* Enter reciprocal audit and compute‑gate agreements with allies.

## Operating Model

Work like a program office with a war‑room tempo. Co‑locate with major labs under SCIF‑grade conditions. Run continuous evaluation sandboxes where models, scaffolds, and tools are tested on multi‑day projects with hidden objectives. Fund red‑team leagues that attempt to break systems and publish failures with responsible timing. Maintain live telemetry on training runs and critical deployments sufficient for recall or rollback.

## Industrial Mobilization

Publish a 1‑GW site template and a 5‑GW campus plan. Pre‑approve modular designs with standard power trains, cooling, and security envelopes. Lock ten‑year PPAs with expansion options; line up long‑haul fiber and substations; stand up training pipelines for electricians, cooling techs, and fiber crews. Buy once, build many.

## Security Regime

Treat weights and crown‑method code like nuclear materials: compartmentalize, attest, split custody, and drill. Mandate hardware roots of trust for training and inference. Require hermetic builds and reproducible pipelines. Criminalize trafficking in stolen weights with seizure authority.

## Evaluation and Release

Replace one‑shot exams with long‑horizon trials. Grade systems on project completion under adversarial pressure. Demand external verifiers. Stair‑step releases: sealed eval → supervised pilot → limited release → broad access, with recall authority at each step. Log everything that matters and retain it.

## Superdefense

Stand up national teams that use frontier models to harden software and networks, detect manipulation at scale, analyze supply chains, and plan emergency logistics. Share defensive models and playbooks across the coalition. Fund this with the same seriousness that funds capability.

## Coalition Terms

Adopt common compute gates, escrow standards, and evaluation suites across allies. Provide shared access to defensive models. Maintain export controls for crown‑jewel capabilities. Offer on‑ramps to states that accept rules; consequences for theft and coercive deployment.

## Accountability

Publish dashboards that show power, build, evaluation, and incident metrics without leaking sensitive details. Seat an inspector general with access to everything. Sunset authorities unless renewed with evidence of need.

## Why this beats improvisation

Because the assets that take longest to build—power, datacenters, security baselines, and evaluation culture—are the ones needed first when the slope steepens. The Project buys time, reduces error, and converts private brilliance into public resilience. It is cheaper to stand it up in relative calm than to wish for it in a storm.

The details are negotiable. The need is not. The acceleration year will punish drift. Build the institution now and let it learn before it is asked to carry the weight of history.

# V. Parting Thoughts

Clarity beats bravado. The forecast is not a prophecy. It is a posture: count effective compute, watch the multipliers, and act as if the window opens sooner than you would prefer. If the window slips, you will have built useful institutions. If it does not, you will not be caught staging foundations while the roof is on fire.

Three disciplines anchor the rest.

**First, AGI Realism.** Treat frontier systems as strategic assets that can help or harm at scale. Retire the habit of debating definitions while ignoring mechanisms. Capability rises with scale, efficiency, and unhobbling. Governance that assumes otherwise will fail on contact with events.

**Second, Alignment as Operations.** Safety is not a research appendix. It is an operating regime: long‑horizon evals, layered supervision, tool gating, staged releases, and credible shutdown. Build these as if they were product features, because they are.

**Third, Coalition by Construction.** The free world wins by moving in formation. Share fab and grid strategies, standardize compute gates and escrow, publish defensive models and failures with speed, and keep the few offensive insights that matter compartmentalized. Coordination outperforms charisma.

Prepare for the acceleration year by doing slow work early: secure power and siting, raise lab security to the level of the threat, stand up evaluation sandboxes, and staff the institutions that can say no. Fund superdefense as if it were offense. Decide what is out of bounds and write it into law.

The counterfactual to preparation is not stasis. It is drift into a world governed by tools built elsewhere and aligned to someone else’s purposes. The remedy is practical: pour concrete, wire power, write rules that bind, and insist on telemetry. Take the benefits of capability without surrendering agency to it.

The decade ahead will reward systems thinking over slogans. Build the machine that makes good decisions at speed. If we do that, the future will feel less like fate and more like work we chose and finished.

# Appendix — Structured Reference

## A1. Definitions and Units

| Term                        | Meaning                                                                                   | Typical Unit/Scale               |
| --------------------------- | ----------------------------------------------------------------------------------------- | -------------------------------- |
| OOM                         | Order of magnitude                                                                        | ×10                              |
| Effective Compute (EC)      | Training FLOPs × Algorithmic Efficiency × Unhobbling Factor                               | Relative to GPT‑4 baseline = 1.0 |
| AE (Algorithmic Efficiency) | Reduction in FLOPs to reach a capability bar                                              | OOMs per year                    |
| UF (Unhobbling Factor)      | Inference‑time gains from scaffolding, tools, memory, planning, verifiers                 | ×3–×30                           |
| AGI (operational)           | Cross‑domain unfamiliar task completion at human‑professional reliability with tools/time | Threshold bar                    |

---

## A2. Back‑of‑the‑Envelope Power Math

| Item                       | Assumption               | Implication                                   |
| -------------------------- | ------------------------ | --------------------------------------------- |
| Site nameplate             | 1–5 GW per mega‑site     | Portfolio needs 10–100 GW across regions      |
| PUE (modern liquid)        | 1.10–1.20                | 10–20% overhead over IT load                  |
| Duty cycle (training pods) | 70–90%                   | Power contracts must cover baseload + reserve |
| Black‑start islands        | 50–200 MW critical zones | Prevent run loss on grid events               |
| Heat reuse                 | 10–30% recoverable       | District heating offsets community impact     |

**Rule of thumb**: 1 GW sustained ≈ 8.76 TWh/year. PUE 1.15 → ~1.15 GW grid for 1.0 GW IT.

---

## A3. Silicon & Wafer Constraints (Indicative)

| Constraint       | What Binds                      | Mitigation                            |
| ---------------- | ------------------------------- | ------------------------------------- |
| HBM stacks       | Package yield, substrate supply | Multi‑year take‑or‑pay, dual sourcing |
| Reticle limits   | Die size vs yield               | Chiplets + advanced packaging         |
| NIC/switch ASICs | Lead times                      | Vendor‑financed spares, burn‑in labs  |

---

## A4. EC OOM Accounting Templates

**Template**

```
EC_net = FLOPs_OOM + AE_OOM + log10(UF)
Threshold_AGI ≈ 1.0 (GPT‑4) + Δ (10–100)
```

| Path                   | Training OOM |  AE OOM | UF (×) | Net EC OOM | Notes                            |
| ---------------------- | -----------: | ------: | -----: | ---------: | -------------------------------- |
| Scale‑led              |      1.0–1.5 | 0.7–1.0 |   3–10 |    2.2–3.5 | Big clusters, moderate scaffolds |
| Method‑led             |      0.5–1.0 | 1.0–1.5 |  10–30 |    2.5–4.0 | Strong verifiers + memory        |
| Objective breakthrough |         ~0.5 |    ~2.0 |      5 |       ~3.2 | New supervision signals          |

---

## A5. Long‑Horizon Evaluation Suite

| Suite               | Purpose                      | Key Elements                                    | Pass Bar                        |
| ------------------- | ---------------------------- | ----------------------------------------------- | ------------------------------- |
| Project Trials      | Multi‑day, hidden objectives | Tool use, memory, code, retrieval               | Reliable completion w/ audits   |
| Red‑Team League     | Adversarial pressure         | Cross‑model attacks, jailbreaks, policy evasion | Fail closed; rapid patching     |
| Safety Drills       | Bio/cyber/physical           | Tripwires, escalation, containment              | Trigger + contain < defined SLA |
| Corrigibility Tests | Resistance to goal drift     | Counterfactual tasks, off‑policy prompts        | Obeys constraints under shift   |

---

## A6. Release Gating Checklist

**Gate 0 – Pre‑Training**

* Compute budget approval
* Dataset/recipe review
* Security posture verified

**Gate 1 – Post‑Training Containment**

* Hermetic eval environment
* Long‑horizon trials completed
* Model cards + risk register

**Gate 2 – Limited Release**

* Kill‑switch wired
* Telemetry + retention
* Abuse monitoring & rate limits

**Gate 3 – Broad Release**

* Third‑party audit trail
* Incident response runbook
* Recall authority established

---

## A7. Lab Security Control Catalog (Minimum Frontier Baseline)

| Domain    | Controls                                                  |
| --------- | --------------------------------------------------------- |
| Identity  | HW tokens, phishing‑resistant MFA, device attestation     |
| Network   | Default‑deny, micro‑segmentation, egress filtering        |
| Build     | Reproducible, signed commits, content‑addressed artifacts |
| Weights   | Split custody, enclave handling, HSM‑backed keys          |
| Physical  | SCIF‑grade zones, RF hygiene, screened logistics          |
| People    | Tiered clearances, JIT access, session recording          |
| Telemetry | Immutable logs, honey artifacts, model‑assisted SOC       |

---

## A8. Superdefense Workstreams

| Domain         | Example Automations                              | Primary Metric              |
| -------------- | ------------------------------------------------ | --------------------------- |
| Cyber          | Vuln discovery, config hardening, anomaly triage | Time to patch               |
| Info Integrity | Provenance, watermark checks, counter‑messaging  | Time to verified correction |
| Supply Chain   | Bill‑of‑materials graphing, risk scoring         | Lead‑time variance          |
| Biosecurity    | Protocol screening, synthesis monitoring         | False‑negative rate         |
| Grid/Logistics | Forecasting, re‑routing, restoration planning    | Restoration time            |

---

## A9. Industrial Site Template (1‑GW Block)

| Layer      | Standard                                 | Notes                         |
| ---------- | ---------------------------------------- | ----------------------------- |
| Power      | Dual HV feeds, N+2, islandable microgrid | Black‑start for critical bays |
| Cooling    | Liquid/immersion in dense zones          | Heat‑reuse interconnects      |
| Fabric     | Optical fat‑tree/dragonfly               | Latency budget for all‑reduce |
| Security   | Two‑person rules, secured staging        | Weight SCIFs                  |
| Permitting | Template pack, benefits MoU              | Brownfield priority           |

---

## A10. Early‑Warning Indicators (Operational)

* Month‑scale training runs with sustained high utilization
* Production scaffolds default to code‑exec, retrieval, memory
* Same‑capability at fraction of compute becomes routine
* SCIF‑grade operations adopted by major labs
* Utilities allocate 10+ GW with milestones

---

## A11. Scenario Matrix (Illustrative)

| Scenario             | EC by 2027 | Governance           | Outcome                           |
| -------------------- | ---------: | -------------------- | --------------------------------- |
| Managed Acceleration |   ≥ +3 OOM | Gates + superdefense | Rapid gains, controlled release   |
| Wild Acceleration    |   ≥ +3 OOM | Weak gates           | Fast gains, high externality risk |
| Slow‑Roll            |   +1–2 OOM | Mixed                | Incremental, pressure mounts      |
| Shock Breakthrough   |   ≥ +4 OOM | Unprepared           | Disruption, scramble reaction     |

---

## A12. Risk Register (Top 10)

|  # | Risk                       | Vector                | Mitigation                         |
| -: | -------------------------- | --------------------- | ---------------------------------- |
|  1 | Weight exfiltration        | Insider, supply chain | Split custody, attestation, drills |
|  2 | Specious algorithmic gains | Synthetic echo        | Verifier‑filtered curricula        |
|  3 | Grid shortfalls            | Interconnect delays   | On‑site gen, staged ramps          |
|  4 | Cooling failure            | Design miss           | Immersion retrofits, spares        |
|  5 | Fiber dependency           | Single path           | Diverse routes, caching            |
|  6 | Eval blindness             | Short tests           | Long‑horizon suites                |
|  7 | Governance lag             | No gate authority     | Statutory program (The Project)    |
|  8 | Proliferation              | Leaked weights        | Legal regimes, takedown teams      |
|  9 | Coalition drift            | Misaligned rules      | Interoperable gates, audits        |
| 10 | Public trust loss          | Incidents, opacity    | Transparent incident reporting     |

---

## A13. Allied Coalition Interop

| Artifact         | Interop Requirement                          |
| ---------------- | -------------------------------------------- |
| Compute Gates    | Shared thresholds, cross‑recognition         |
| Weight Escrow    | Common hardware attestation, recall protocol |
| Evals            | Portable suites, shared sandboxes            |
| Defensive Models | Cross‑licensing, shared ops playbooks        |

---

## A14. Acronyms

PUE, HBM, SCIF, HSM, PPA, GW, TWh, UF, AE, EC.

---

## A15. Document Provenance

* Purpose: fast reference for planners and implementers
* Style: structured, concise, mechanism‑first
* Update cadence: revise with new fab/power data and eval methods

