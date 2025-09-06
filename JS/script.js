
const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));
const setError = (name, msg) => {
  const p = document.querySelector(`.error[data-error-for="${name}"]`);
  if (p) p.textContent = msg || "";
};
const clearAllErrors = () => $$(".error").forEach(e => (e.textContent = ""));

// Usamos un Regex para validar el email
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
// +NNN.NNNNNNNN 
const telRegex = /^\+\d{3}\.\d{7,12}$/;


let minFechaEntregaISO = null;


function poblarRegiones() {
  const selRegion = $("#region");
  const selComuna = $("#comuna");

    if (typeof region_comuna === "undefined" || !Array.isArray(region_comuna.regiones)) {
    console.error("region_comuna.js no cargó o la ruta es incorrecta.");
    return;
    }


  selRegion.innerHTML = `<option value="">Seleccione una región…</option>`;
  selComuna.innerHTML = `<option value="">Seleccione una comuna…</option>`;
  selComuna.disabled = true;

  region_comuna.regiones.forEach(r => {
    const opt = document.createElement("option");
    opt.value = String(r.numero);
    opt.textContent = r.nombre;
    selRegion.appendChild(opt);
  });

  const actualizarComunas = () => {
    selComuna.innerHTML = `<option value="">Seleccione una comuna…</option>`;
    selComuna.disabled = true;

    const valor = selRegion.value.trim();
    if (!valor) return;

    const numero = Number(valor);
    const reg = region_comuna.regiones.find(r => r.numero === numero);
    if (!reg) return;

    reg.comunas.forEach(c => {
      const opt = document.createElement("option");
      opt.value = String(c.id);
      opt.textContent = c.nombre;
      selComuna.appendChild(opt);
    });
    selComuna.disabled = false;
  };

  selRegion.addEventListener("change", actualizarComunas);

  if (selRegion.value) actualizarComunas();
}

function setupContactarPor() {
  const checkboxes = $$('input[name="contactarPor"]');
  const cont = $("#contacto-ids");

  const ensureInputFor = (valor) => {
    let wrap = cont.querySelector(`[data-contact-input="${valor}"]`);
    if (!wrap) {
      wrap = document.createElement("div");
      wrap.className = "field";
      wrap.dataset.contactInput = valor;
      const label = document.createElement("label");
      label.textContent = `ID/URL de ${valor} (4–50 caracteres)`;
      const inp = document.createElement("input");
      inp.type = "text";
      inp.minLength = 4;
      inp.maxLength = 50;
      inp.name = `contact_${valor}`;
      wrap.appendChild(label);
      wrap.appendChild(inp);
      cont.appendChild(wrap);
    }
  };

  const removeInputFor = (valor) => {
    const wrap = cont.querySelector(`[data-contact-input="${valor}"]`);
    if (wrap) wrap.remove();
  };

  const actualizarInputs = () => {
    const seleccionadas = checkboxes.filter(cb => cb.checked);
    
    if (seleccionadas.length > 5) {
      const ultima = seleccionadas[seleccionadas.length - 1];
      ultima.checked = false;
      setError("contactarPor", "Máximo 5 opciones.");
      return;
    } else {
      setError("contactarPor", "");
    }

    const vals = new Set(seleccionadas.map(cb => cb.value));
    vals.forEach(v => ensureInputFor(v));
    $$("#contacto-ids .field").forEach(div => {
      const v = div.dataset.contactInput;
      if (!vals.has(v)) div.remove();
    });
  };

  checkboxes.forEach(cb => {
    cb.addEventListener("change", actualizarInputs);
  });
}

function setupFotos() {
  const wrapper = $("#fotos-wrapper");
  const btn = $("#btn-agregar-foto");
  const maxFotos = 5;

  btn.addEventListener("click", () => {
    const actuales = wrapper.querySelectorAll('input[type="file"]').length;
    if (actuales >= maxFotos) {
      setError("fotos", "Máximo 5 fotos.");
      return;
    }
    setError("fotos", "");
    const inp = document.createElement("input");
    inp.type = "file";
    inp.name = "fotos";
    inp.accept = "image/*";
    wrapper.appendChild(inp);
  });
}

function setupFechaEntrega() {
  const inp = $("#fecha-entrega");
  const now = new Date();
  now.setMinutes(now.getMinutes() + 180);
  const pad = (n) => String(n).padStart(2, "0");
  const isoLocal = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}T${pad(now.getHours())}:${pad(now.getMinutes())}`;
  inp.value = isoLocal;
  minFechaEntregaISO = isoLocal;
}

function validarFormulario() {
  clearAllErrors();
  let ok = true;

  const region = $("#region").value.trim();
  const comuna = $("#comuna").value.trim();
  const sector = $("#sector").value.trim();

  if (!region) { setError("region", "Seleccione una región."); ok = false; }
  if (!comuna) { setError("comuna", "Seleccione una comuna."); ok = false; }
  if (sector && sector.length > 100) { setError("sector", "Máximo 100 caracteres."); ok = false; }

  const nombre = $("#nombre").value.trim();
  const email = $("#email").value.trim();
  const celular = $("#celular").value.trim();
  const checkboxesContactar = $$('input[name="contactarPor"]');
  const seleccionadas = checkboxesContactar.filter(cb => cb.checked).map(cb => cb.value);

  if (nombre.length < 3 || nombre.length > 200) {
    setError("nombre", "Entre 3 y 200 caracteres.");
    ok = false;
  }
  if (!emailRegex.test(email) || email.length > 100) {
    setError("email", "Email inválido o supera 100 caracteres.");
    ok = false;
  }
  if (celular && !telRegex.test(celular)) {
    setError("celular", "Formato esperado: +NNN.NNNNNNNN");
    ok = false;
  }
  if (seleccionadas.length > 5) {
    setError("contactarPor", "Máximo 5 opciones.");
    ok = false;
  } else {
    for (const val of seleccionadas) {
      const input = document.querySelector(`[data-contact-input="${val}"] input`);
      if (!input) continue;
      const v = input.value.trim();
      if (v.length > 0 && (v.length < 4 || v.length > 50)) {
        setError("contactarPor", `El ID/URL de ${val} debe tener entre 4 y 50 caracteres.`);
        ok = false;
        break;
      }
    }
  }

  const tipo = $("#tipo").value.trim();
  const cantidad = $("#cantidad").value.trim();
  const edad = $("#edad").value.trim();
  const unidad = $("#unidad-edad").value.trim();
  const fechaEntrega = $("#fecha-entrega").value.trim();

  if (!tipo) { setError("tipo", "Seleccione el tipo (gato o perro)."); ok = false; }

  const esEnteroPos = (s) => /^\d+$/.test(s) && Number(s) >= 1;
  if (!esEnteroPos(cantidad)) { setError("cantidad", "Ingrese entero ≥ 1."); ok = false; }
  if (!esEnteroPos(edad)) { setError("edad", "Ingrese entero ≥ 1."); ok = false; }
  if (!unidad) { setError("unidadEdad", "Seleccione meses o años."); ok = false; }

  if (!fechaEntrega) {
    setError("fechaEntrega", "Ingrese fecha y hora.");
    ok = false;
  } else {
    if (fechaEntrega < minFechaEntregaISO) {
      setError("fechaEntrega", "Debe ser ≥ a la fecha/hora prellenada.");
      ok = false;
    }
  }

  // Fotos
  const fotos = $$('#fotos-wrapper input[type="file"]');
  if (fotos.length < 1) {
    setError("fotos", "Debe adjuntar al menos 1 foto.");
    ok = false;
  } else if (fotos.length > 5) {
    setError("fotos", "Máximo 5 fotos.");
    ok = false;
  }

  return ok;
}

function setupEnvio() {
  const btnEnviar = $("#btn-enviar");
  const modal = $("#modal-confirmacion");
  const si = $("#confirmar-si");
  const no = $("#confirmar-no");
  const form = $("#form-aviso");
  const exito = $("#exito");

  btnEnviar.addEventListener("click", () => {
    if (validarFormulario()) {
      modal.showModal();
    }
  });

  no.addEventListener("click", () => modal.close());

  si.addEventListener("click", () => {
    modal.close();
    form.querySelectorAll("fieldset, .actions, .error").forEach(el => el.setAttribute("hidden", "hidden"));
    exito.hidden = false;
  });
}

document.addEventListener("DOMContentLoaded", () => {
  poblarRegiones();
  setupContactarPor();
  setupFotos();
  setupFechaEntrega();
  setupEnvio();
});
