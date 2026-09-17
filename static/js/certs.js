document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.cert-card img').forEach(img => {
    img.addEventListener('click', () => {
      img.closest('.cert-card').classList.add('zoomed');
    });
  });

  document.querySelectorAll('.cert-close').forEach(btn => {
    btn.addEventListener('click', () => {
      btn.closest('.cert-card').classList.remove('zoomed');
    });
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      document.querySelector('.cert-card.zoomed')?.classList.remove('zoomed');
    }
  });
});
