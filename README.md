# Spray Math

The paint sprayer honesty tool. The tip code is a sentence nobody
reads, the paint can promises walls it cannot reach, and the quarter
of it that lands on the drop cloth was never in the estimate. Spray
Math decodes the tip, prices the overspray into the coverage, and
turns the flow rate into honest trigger-minutes.

- Live app: https://ilanis-agent.github.io/spraymath/app.html
- Landing: https://ilanis-agent.github.io/spraymath/

## What it does

1. **The tip truth** - the three digits decode: first digit doubled is
   the fan width in inches, the last two are the orifice in
   thousandths, banded into stains, thin paints, latex and heavy latex.
2. **The coverage truth** - square feet x coats x 1.25 overspray
   allowance (labeled norm) / 350 per gallon (labeled norm), held
   against the gallons bought with verdicts at 85 and 100 percent.
3. **The pace truth** - square feet x coats / (GPM x 250 effective
   coverage, labeled norm) into trigger-minutes, banded into a quick
   coat, a morning on the trigger and a long spray day.

## Files

- `engine.js` - pure functions (`tipPlan`, `coveragePlan`, `pacePlan`) plus renderers
- `app.html` - the app; `index.html` - the landing page
- `oracle.py` - independent Python mirror of the engine
- `test.js` + `expected.json` - 29 oracle cases, `node test.js` runs green

The norms are labeled; the drop cloth keeps the honest ledger.
