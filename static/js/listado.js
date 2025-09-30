const avisosData = {
  1: {
    tipo: "Gato",
    cantidad: 1,
    edad: "2 meses",
    descripcion: "Gatito muy cariñoso y juguetón. Está desparasitado y con sus primeras vacunas. Busca una familia que le dé mucho amor.",
    region: "Región Metropolitana",
    comuna: "Santiago",
    sector: "Beauchef 850, terraza",
    fechaEntrega: "2025-01-20 15:00",
    nombre: "María González",
    email: "maria.gonzalez@email.com",
    celular: "+569.12345678",
    redesSociales: [
      { tipo: "whatsapp", id: "@maria_gonzalez" },
      { tipo: "instagram", id: "@maria_pets" }
    ],
    fotos: [
      { src: "../img/gato1.jpg", alt: "Gato en adopción" }
    ]
  },
  2: {
    tipo: "Perro",
    cantidad: 3,
    edad: "2 meses",
    descripcion: "Tres cachorros muy sanos y activos. Son hermanos y sería ideal adoptarlos juntos o por separado. Todos están desparasitados.",
    region: "Región Metropolitana",
    comuna: "Ñuñoa",
    sector: "Plaza Ñuñoa",
    fechaEntrega: "2025-01-19 10:00",
    nombre: "Carlos Rodríguez",
    email: "carlos.rodriguez@email.com",
    celular: "+569.87654321",
    redesSociales: [
      { tipo: "telegram", id: "@carlos_rodriguez" },
      { tipo: "whatsapp", id: "@carlos_pets" },
      { tipo: "x", id: "@carlos_adopciones" }
    ],
    fotos: [
      { src: "../img/perro1.jpg", alt: "Perros en adopción" }
    ]
  },
  3: {
    tipo: "Gato",
    cantidad: 2,
    edad: "1 mes",
    descripcion: "Dos gatitos bebés muy tiernos. Necesitan cuidados especiales por su corta edad. Ideal para personas con experiencia en gatos.",
    region: "Región Metropolitana",
    comuna: "Santiago",
    sector: "Parque O'Higgins",
    fechaEntrega: "2025-01-21 14:00",
    nombre: "Ana Silva",
    email: "ana.silva@email.com",
    celular: "+569.11223344",
    redesSociales: [
      { tipo: "instagram", id: "@ana_silva_pets" }
    ],
    fotos: [
      { src: "../img/gato2.jpg", alt: "Gatos en adopción" }
    ]
  },
  4: {
    tipo: "Perro",
    cantidad: 1,
    edad: "1 año",
    descripcion: "Perro adulto muy tranquilo y educado. Está castrado y con todas sus vacunas al día. Perfecto para una familia con niños.",
    region: "Región Metropolitana",
    comuna: "La Florida",
    sector: "Av. Vicuña Mackenna",
    fechaEntrega: "2025-01-18 11:00",
    nombre: "Pedro Martínez",
    email: "pedro.martinez@email.com",
    celular: "+569.55667788",
    redesSociales: [
      { tipo: "whatsapp", id: "@pedro_martinez" },
      { tipo: "telegram", id: "@pedro_pets" }
    ],
    fotos: [
      { src: "../img/perro2.jpg", alt: "Perro en adopción" }
    ]
  },
  5: {
    tipo: "Gato",
    cantidad: 1,
    edad: "3 años",
    descripcion: "Gato adulto muy independiente y cariñoso. Está esterilizado y es muy limpio. Ideal para personas que trabajan.",
    region: "Región Metropolitana",
    comuna: "Providencia",
    sector: "Costanera Center",
    fechaEntrega: "2025-01-17 16:00",
    nombre: "Laura Fernández",
    email: "laura.fernandez@email.com",
    celular: "+569.99887766",
    redesSociales: [
      { tipo: "instagram", id: "@laura_fernandez" },
      { tipo: "tiktok", id: "@laura_pets" }
    ],
    fotos: [
      { src: "../img/gato3.jpg", alt: "Gato en adopción" }
    ]
  }
};

const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

function formatearFecha(fechaStr) {
  const fecha = new Date(fechaStr);
  return fecha.toLocaleString('es-CL', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
}

function mostrarDetalles(avisoId) {
  const aviso = avisosData[avisoId];
  if (!aviso) return;

  $('#det-tipo').textContent = aviso.tipo;
  $('#det-cantidad').textContent = aviso.cantidad;
  $('#det-edad').textContent = aviso.edad;
  $('#det-descripcion').textContent = aviso.descripcion;

  $('#det-region').textContent = aviso.region;
  $('#det-comuna').textContent = aviso.comuna;
  $('#det-sector').textContent = aviso.sector;
  $('#det-fecha-entrega').textContent = formatearFecha(aviso.fechaEntrega);

  $('#det-nombre').textContent = aviso.nombre;
  $('#det-email').textContent = aviso.email;
  $('#det-celular').textContent = aviso.celular || 'No proporcionado';

  const redesContainer = $('#det-redes-sociales');
  redesContainer.innerHTML = '';
  
  if (aviso.redesSociales && aviso.redesSociales.length > 0) {
    const redesTitle = document.createElement('p');
    redesTitle.innerHTML = '<strong>Redes sociales:</strong>';
    redesContainer.appendChild(redesTitle);
    
    aviso.redesSociales.forEach(red => {
      const p = document.createElement('p');
      p.innerHTML = `${red.tipo.charAt(0).toUpperCase() + red.tipo.slice(1)}: ${red.id}`;
      redesContainer.appendChild(p);
    });
  } else {
    redesContainer.innerHTML = '<p><strong>Redes sociales:</strong> No proporcionadas</p>';
  }

  const fotosContainer = $('#det-fotos');
  fotosContainer.innerHTML = '';
  
  aviso.fotos.forEach((foto, index) => {
    const photoItem = document.createElement('div');
    photoItem.className = 'photo-item';
    
    const img = document.createElement('img');
    img.src = foto.src;
    img.alt = foto.alt;
    img.loading = 'lazy';
    
    img.addEventListener('click', () => ampliarFoto(foto.src, foto.alt));
    
    photoItem.appendChild(img);
    fotosContainer.appendChild(photoItem);
  });

  $('#modal-detalles').showModal();
}

function ampliarFoto(src, alt) {
  const modal = $('#photo-modal');
  const img = $('#photo-modal-img');
  
  img.src = src;
  img.alt = alt;
  modal.style.display = 'flex';
}

function cerrarModalFoto() {
  $('#photo-modal').style.display = 'none';
}

function setupEventos() {
  $$('#tabla-avisos tbody tr').forEach(fila => {
    fila.addEventListener('click', () => {
      const avisoId = parseInt(fila.dataset.aviso);
      mostrarDetalles(avisoId);
    });
  });

  $('#cerrar-modal').addEventListener('click', () => {
    $('#modal-detalles').close();
  });

  $('#photo-modal').addEventListener('click', (e) => {
    if (e.target === $('#photo-modal') || e.target.classList.contains('close-btn')) {
      cerrarModalFoto();
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if ($('#modal-detalles').open) {
        $('#modal-detalles').close();
      }
      if ($('#photo-modal').style.display === 'flex') {
        cerrarModalFoto();
      }
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  setupEventos();
});
