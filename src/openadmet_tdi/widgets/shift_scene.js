export function render({ model, el }) {
  const X0 = -2, X1 = 2, NHILL = 0.9;
  const PL_X = 48, PL_W = 496, PL_Y = 120, PL_H = 102;
  const P_MIN = 4.4, P_MAX = 6.2;

  const xToSvg = (x) => PL_X + ((x - X0) / (X1 - X0)) * PL_W;
  const act = (x, p) => 100 / (1 + Math.pow(10, NHILL * (x - (6 - p))));
  const pathD = (p) => {
    let d = "";
    for (let i = 0; i <= 100; i += 1) {
      const x = X0 + ((X1 - X0) * i) / 100;
      const y = PL_Y - (act(x, p) / 100) * PL_H;
      d += (i ? " L" : "M") + xToSvg(x).toFixed(1) + "," + y.toFixed(1);
    }
    return d;
  };
  const ic50uM = (p) => Math.pow(10, 6 - p);
  const D_MIN = pathD(P_MIN);

  const tickX = [-2, -1, 0, 1, 2];
  const tickLbl = ["0.01", "0.1", "1", "10", "100"];
  const grid = tickX
    .map(
      (t, i) =>
        `<line x1="${xToSvg(t)}" y1="18" x2="${xToSvg(t)}" y2="120" class="sc-grid"></line>` +
        `<text x="${xToSvg(t)}" y="134" text-anchor="middle" class="sc-svg-text">${tickLbl[i]}</text>`
    )
    .join("");

  el.innerHTML = `
    <div class="sc-card">
      <div class="sc-head">
        <div class="sc-title">The instant read vs the pre-incubated read</div>
        <label class="sc-toggle">
          <input type="checkbox" id="sc-pre"/>
          <span class="sc-knob"></span>
          <span class="sc-toggle-label">Pre-incubate 30 min (+NADPH)</span>
        </label>
      </div>

      <svg class="sc-chart" viewBox="0 0 560 158" preserveAspectRatio="xMidYMid meet" role="img"
           aria-label="Dose-response curve of residual enzyme activity, sliding left after pre-incubation">
        <text x="8" y="11" class="sc-svg-text">% enzyme activity left</text>
        ${grid}
        <line x1="48" y1="120" x2="544" y2="120" class="sc-axis"></line>
        <line x1="48" y1="18" x2="48" y2="120" class="sc-axis"></line>
        <text x="100" y="69" class="sc-svg-text faint">50%</text>
        <line x1="48" y1="69" x2="544" y2="69" class="sc-grid"></line>
        <text x="544" y="150" text-anchor="end" class="sc-svg-text">compound concentration (&micro;M, log scale) &#8594;</text>
        <line x1="${xToSvg(1)}" y1="18" x2="${xToSvg(1)}" y2="120" class="sc-threshold"></line>
        <text x="${xToSvg(1) + 5}" y="29" class="sc-svg-text warn">hit: IC50 = 10 &micro;M</text>
        <path id="sc-ghost" class="sc-ghost" d="${D_MIN}"></path>
        <path id="sc-main" class="sc-path" d="${D_MIN}"></path>
        <circle id="sc-dot" r="4" cx="${xToSvg(6 - P_MIN)}" cy="69"></circle>
      </svg>

      <div class="sc-readout">
        <span class="sc-chip">pIC50 <b id="sc-pic50">4.40</b></span>
        <span class="sc-chip">IC50 &asymp; <b id="sc-ic50">40</b> &micro;M</span>
        <span class="sc-verdict sc-v-off">instant screen: looks clean &mdash; TDI missed</span>
        <span class="sc-verdict sc-v-on">after pre-incubation: TDI detected &#10003;</span>
      </div>

      <div class="sc-cap sc-cap-off">Measured straight away, the compound has barely disabled any enzyme &mdash; it would sail through a conventional instantaneous screen.</div>
      <div class="sc-cap sc-cap-on">While it sits with active CYP for 30 minutes, it disables more and more enzyme &mdash; the dose&ndash;response measured afterwards has slid left across the hit threshold.</div>
    </div>`;

  const toggle = el.querySelector("#sc-pre");
  const card = el.querySelector(".sc-card");
  const main = el.querySelector("#sc-main");
  const dot = el.querySelector("#sc-dot");
  const pic50El = el.querySelector("#sc-pic50");
  const ic50El = el.querySelector("#sc-ic50");

  let raf = null;
  let cur = P_MIN;

  const draw = () => {
    main.setAttribute("d", pathD(cur));
    dot.setAttribute("cx", xToSvg(6 - cur).toFixed(1));
    pic50El.textContent = cur.toFixed(2);
    const v = ic50uM(cur);
    ic50El.textContent = v >= 10 ? String(Math.round(v)) : v >= 1 ? v.toFixed(1) : v.toFixed(2);
  };

  const animateTo = (target) => {
    if (raf) cancelAnimationFrame(raf);
    const from = cur;
    const t0 = performance.now();
    const dur = 1400;
    const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
    const step = (now) => {
      const t = Math.min(1, (now - t0) / dur);
      cur = from + (target - from) * ease(t);
      draw();
      if (t < 1 && el.isConnected) raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
  };

  toggle.addEventListener("change", () => {
    card.classList.toggle("has-pre", toggle.checked);
    animateTo(toggle.checked ? P_MAX : P_MIN);
  });

  draw();
}