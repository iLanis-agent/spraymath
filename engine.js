var SprayMath = (function () {
  function num(x) { return typeof x === "number" && isFinite(x); }
  function pos(x) { return num(x) && x > 0; }
  function r1(x) { return Math.round(x * 10) / 10; }
  function r2(x) { return Math.round(x * 100) / 100; }
  function jsnum(x) { if (typeof x === "number" && isFinite(x) && x === Math.trunc(x)) return String(Math.trunc(x)); return String(x); }
  var OVERSPRAY = 1.25, COVER = 350, EFFECTIVE = 250;
  function tipPlan(code) {
    if (!num(code) || code !== Math.trunc(code) || code < 100 || code > 999) return { error: "the tip code must be a three-digit number" };
    var fan = Math.floor(code / 100) * 2;
    var thou = code % 100;
    var band = thou < 11 ? "stains and lacquers"
      : thou < 15 ? "thin paints and sealers"
      : thou <= 19 ? "latex"
      : "heavy latex and elastomeric";
    return { fan: fan, thou: thou, band: band };
  }
  function renderTip(r, code) {
    return "The " + jsnum(code) + " tip throws a fan " + jsnum(r.fan) + " inches wide from an orifice of "
      + jsnum(r.thou) + " thousandths - a tip that sprays " + r.band + ".";
  }
  function coveragePlan(sqft, coats, bought) {
    if (!pos(sqft)) return { error: "the square footage must be above zero" };
    if (!pos(coats)) return { error: "the coat count must be above zero" };
    if (!pos(bought)) return { error: "the gallons bought must be above zero" };
    var needed = sqft * coats * OVERSPRAY / COVER;
    var margin = bought / needed * 100;
    var verdict = margin >= 100 ? "the cans cover the job"
      : margin >= 85 ? "close, but one more gallon earns its shelf"
      : "the cans run dry mid-wall";
    return { needed: r2(needed), margin: r1(margin), verdict: verdict };
  }
  function renderCoverage(r, sqft, coats, bought) {
    var word = coats === 1 ? " coat over " : " coats over ";
    return "At " + jsnum(coats) + word + jsnum(sqft) + " square feet, the overspray allowance wants " + jsnum(r.needed)
      + " gallons; the " + jsnum(bought) + "-gallon purchase sits at " + jsnum(r.margin) + "% of that, and " + r.verdict + ".";
  }
  function pacePlan(gpm, sqft, coats) {
    if (!pos(gpm)) return { error: "the flow rate must be above zero" };
    if (!pos(sqft)) return { error: "the square footage must be above zero" };
    if (!pos(coats)) return { error: "the coat count must be above zero" };
    var minutes = sqft * coats / (gpm * EFFECTIVE);
    var verdict = minutes < 30 ? "a quick coat"
      : minutes < 120 ? "a morning on the trigger"
      : "a long spray day";
    return { minutes: r1(minutes), verdict: verdict };
  }
  function renderPace(r, gpm, sqft, coats) {
    var word = coats === 1 ? " coat over " : " coats over ";
    return "At " + jsnum(gpm) + " gallons a minute with the overspray loss priced in, " + jsnum(coats) + word
      + jsnum(sqft) + " square feet is about " + jsnum(r.minutes) + " trigger-minutes - " + r.verdict + ".";
  }
  return { tipPlan: tipPlan, renderTip: renderTip, coveragePlan: coveragePlan, renderCoverage: renderCoverage, pacePlan: pacePlan, renderPace: renderPace };
})();
if (typeof module !== "undefined" && module.exports) module.exports = SprayMath;
