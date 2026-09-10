export function render({ model, el }) {
  const ic = model.get("icon_uris") || {};

  const img = (name, cls, label) =>
    `<img class="ic ${cls || ""}" src="${ic[name] || ""}" alt="${label || name}" title="${label || name}" draggable="false"/>`;

  // cracked-tablet glyph: the victim drug broken into fragments (cleared)
  const frags = (cls) => `
    <svg class="ic-svg ${cls}" viewBox="0 0 26 22" role="img" aria-label="drug broken into fragments">
      <path d="M11,2 A9,9 0 0 0 11,20 Z" fill="#efebca" stroke="#898259" stroke-width="1" stroke-linejoin="round"/>
      <path d="M15,3 A9.5,9.5 0 0 1 15,21 Z" fill="#e4e2b3" stroke="#898259" stroke-width="1" stroke-linejoin="round" transform="rotate(9 19 12)"/>
      <circle cx="22.5" cy="4.5" r="1.1" fill="#d2cb96"/>
      <circle cx="24" cy="17" r="0.9" fill="#d2cb96"/>
    </svg>`;

  el.innerHTML = `
    <div class="ddi-card">
      <div class="ddi-head">
        <div class="ddi-title">A drug–drug interaction (DDI), in one picture</div>
        <label class="ddi-toggle">
          <input type="checkbox" id="ddi-inhibitor"/>
          <span class="ddi-knob"></span>
          <span class="ddi-toggle-label">Add a CYP inhibitor</span>
        </label>
      </div>

      <div class="ddi-pipeline">
        <div class="ddi-station">
          <div class="ddi-dose-pile" id="ddi-pile"></div>
          <div class="ddi-station-label">victim drug<span class="ddi-sub">repeated doses</span></div>
        </div>

        <div class="ddi-flux"><span class="ddi-pipe-arrow"></span><span class="ddi-flux-stop">&#10005;</span></div>

        <div class="ddi-station">
          <div class="ddi-gate">
            ${img("liver", "ic-liver", "liver")}
            ${img("enzyme_yellow", "ic-enzyme", "CYP enzyme")}
            <div class="ddi-plug">${img("pill_blue", "ic-plug", "inhibitor")}<span class="ddi-x">&#10005;</span></div>
          </div>
          <div class="ddi-station-label">CYP enzyme<span class="ddi-sub">clears the dose (liver)</span></div>
        </div>

        <div class="ddi-flux"><span class="ddi-pipe-arrow"></span></div>

        <div class="ddi-station">
          <div class="ddi-out ddi-out-ok">
            ${frags("ddi-frags-lg")}
            <span class="ddi-out-badge ok">cleared &#10003;</span>
          </div>
          <div class="ddi-out ddi-out-bad">
            <span class="ddi-out-badge bad">nothing cleared &#10005;</span>
          </div>
          <div class="ddi-station-label">removed from the body</div>
        </div>
      </div>

      <div class="ddi-exposure">
        <div class="ddi-exposure-head">
          <span>Plasma level of the victim drug</span>
          <span class="ddi-chips">
            <span class="chip chip-base">no inhibitor</span>
            <span class="chip chip-inh">+ inhibitor</span>
          </span>
        </div>
        <svg class="ddi-chart" viewBox="0 0 560 132" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Plasma concentration of the victim drug over time, with and without a CYP inhibitor">
          <rect x="10" y="10" width="540" height="32" class="ddi-zone-toxic"></rect>
          <rect x="10" y="42" width="540" height="63" class="ddi-zone-safe"></rect>
          <line x1="10" y1="42" x2="550" y2="42" class="ddi-threshold"></line>
          <text x="16" y="37" class="ddi-svg-text warn">toxic threshold</text>
          <path class="ddi-path ddi-path-base" d="M10,100 C120,86 260,74 550,71" pathLength="1"></path>
          <path class="ddi-path ddi-path-inh" d="M10,100 C120,92 220,78 300,48 C340,32 420,24 550,20" pathLength="1"></path>
          <text x="546" y="16" class="ddi-svg-text lab-inh" text-anchor="end">+ inhibitor</text>
          <text x="546" y="64" class="ddi-svg-text lab-base" text-anchor="end">no inhibitor</text>
          <text x="550" y="128" class="ddi-svg-text" text-anchor="end">time &#8594;</text>
        </svg>
        <div class="ddi-cap ddi-cap-off">Each dose is cleared before the next arrives &mdash; plasma level stays in the therapeutic range.</div>
        <div class="ddi-cap ddi-cap-on">The inhibitor slowly shuts the CYP down &mdash; doses pile up and plasma level climbs past the toxic threshold.</div>
      </div>

      <div class="ddi-legend">
        <span>${img("drug_tablet", "ic-legend", "victim drug")} victim drug</span>
        <span>${img("pill_blue", "ic-legend", "inhibitor")} inhibitor</span>
        <span>${img("enzyme_yellow", "ic-legend", "CYP enzyme")} CYP enzyme</span>
        <span>${frags("ic-legend-frag")} cleared (broken down)</span>
      </div>
    </div>`;

  const toggle = el.querySelector("#ddi-inhibitor");
  const card = el.querySelector(".ddi-card");
  const pile = el.querySelector("#ddi-pile");
  let timer = null;

  const setPile = (n, drop) => {
    pile.innerHTML = "";
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
    if (!drop) {
      for (let i = 0; i < n; i += 1) {
        const p = document.createElement("img");
        p.src = ic["drug_tablet"];
        p.className = "ic ic-mini";
        p.alt = "victim drug dose";
        pile.appendChild(p);
      }
      return;
    }
    let k = 0;
    timer = setInterval(() => {
      if (!el.isConnected || k >= n) {
        if (timer) clearInterval(timer);
        timer = null;
        return;
      }
      k += 1;
      const p = document.createElement("img");
      p.src = ic["drug_tablet"];
      p.className = "ic ic-mini ddi-drop";
      p.alt = "accumulating victim drug dose";
      pile.appendChild(p);
    }, 170);
  };

  toggle.addEventListener("change", () => {
    if (toggle.checked) {
      card.classList.add("has-inhibitor");
      setPile(8, true);
    } else {
      card.classList.remove("has-inhibitor");
      setPile(2, false);
    }
  });

  setPile(2, false);
}