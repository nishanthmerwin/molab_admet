export function render({ model, el }) {
  const ic = model.get("icon_uris") || {};

  const caged = `
    <svg class="pg-caged" viewBox="0 0 20 20" role="img" aria-label="caged probe (non-fluorescent)">
      <circle cx="10" cy="10" r="5.2" fill="#cbd5e1" stroke="#94a3b8" stroke-width="1"/>
      <circle cx="10" cy="10" r="8.4" fill="none" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2 2.6"/>
    </svg>`;

  const dot = () => `
    <svg class="pg-dot" viewBox="0 0 20 20" role="img" aria-label="fluorescent product">
      <circle cx="10" cy="10" r="5" fill="#4ade80" fill-opacity="0.9"/>
      <circle cx="10" cy="10" r="8.2" fill="none" stroke="#22c55e" stroke-opacity="0.3" stroke-width="1"/>
    </svg>`;

  el.innerHTML = `
    <div class="pg-card">
      <div class="pg-head">
        <div class="pg-title">The readout: caged probe in, glow out</div>
        <label class="pg-slider-wrap">
          <span class="pg-slider-label">Add compound</span>
          <input type="range" id="pg-conc" min="0" max="100" value="0"/>
        </label>
      </div>

      <div class="pg-pipeline">
        <div class="pg-station">
          <div class="pg-probes">${caged}${caged}${caged}${caged}${caged}</div>
          <div class="pg-station-label">caged probe<span class="pg-sub">dark &mdash; cannot glow yet</span></div>
        </div>

        <div class="pg-flux"><span class="pg-pipe-arrow"></span></div>

        <div class="pg-station">
          <div class="pg-gate">
            <img class="ic pg-enzyme" src="${ic["enzyme_yellow"] || ""}" alt="CYP enzyme" draggable="false"/>
          </div>
          <div class="pg-station-label">CYP cleaves it<span class="pg-sub">if it is working</span></div>
        </div>

        <div class="pg-flux"><span class="pg-pipe-arrow"></span></div>

        <div class="pg-station">
          <div class="pg-well" id="pg-well"></div>
          <div class="pg-station-label">product<span class="pg-sub">fluoresces &mdash; the detector sees it</span></div>
        </div>
      </div>

      <div class="pg-meter-row">
        <span class="pg-meter-label">signal vs no-compound control</span>
        <div class="pg-meter"><div class="pg-meter-fill" id="pg-fill"></div></div>
        <span class="pg-pct"><b id="pg-pct">100%</b></span>
        <span class="pg-chip">[compound] = <b id="pg-conc-lbl">none</b></span>
      </div>

      <div class="pg-cap">More glow = more product = more working CYP. An inhibitor dims the glow &mdash; and tracing the signal across concentrations traces out the dose&ndash;response curve that <b>IC50</b> (and <b>pIC50 = &minus;log10(IC50)</b>) come from.</div>
      <div class="pg-cap pg-cap-note">CYP2D6 uses the same logic with a mass spectrometer as the detector: dextromethorphan &rarr; dextrorphan is counted, not seen.</div>
    </div>`;

  const slider = el.querySelector("#pg-conc");
  const well = el.querySelector("#pg-well");
  const fill = el.querySelector("#pg-fill");
  const pct = el.querySelector("#pg-pct");
  const concLbl = el.querySelector("#pg-conc-lbl");
  const arrows = el.querySelectorAll(".pg-pipe-arrow");

  let activity = 100;
  let acc = 0;

  const compute = (v) => {
    if (v <= 0) return { act: 100, lbl: "none" };
    const x = -1 + ((v - 1) / 99) * 3;
    const act = 100 / (1 + Math.pow(10, 0.9 * (x - 1)));
    const uM = Math.pow(10, x);
    const lbl = uM >= 1 ? `${Math.round(uM)} \u00b5M` : `${uM.toFixed(2)} \u00b5M`;
    return { act, lbl };
  };

  const update = () => {
    fill.style.width = `${activity}%`;
    pct.textContent = `${Math.round(activity)}%`;
    const flow = 0.25 + (activity / 100) * 0.75;
    arrows.forEach((a) => {
      a.style.opacity = String(flow);
      a.style.setProperty("--pg-flow-speed", `${(1.6 - (activity / 100) * 0.7).toFixed(2)}s`);
    });
  };

  const spawn = () => {
    acc += (activity / 100) * 0.85;
    while (acc >= 1) {
      acc -= 1;
      if (well.childElementCount > 20 && well.firstChild) {
        well.removeChild(well.firstChild);
      }
      const t = document.createElement("span");
      t.innerHTML = dot();
      const node = t.firstElementChild;
      node.style.left = `${(14 + Math.random() * 72).toFixed(1)}%`;
      node.style.top = `${(14 + Math.random() * 72).toFixed(1)}%`;
      node.style.animationDuration = `${(2.4 + Math.random() * 1).toFixed(2)}s`;
      node.addEventListener("animationend", () => node.remove());
      well.appendChild(node);
    }
  };

  slider.addEventListener("input", () => {
    const { act, lbl } = compute(Number(slider.value));
    activity = act;
    concLbl.textContent = lbl;
    update();
  });

  update();
  setInterval(() => {
    if (el.isConnected) spawn();
  }, 150);
}