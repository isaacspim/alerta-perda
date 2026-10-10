(() => {
  const lotSelect = document.querySelector('#lote_id');
  const quantity = document.querySelector('#quantidade_perdida');
  if (!lotSelect || !quantity) return;

  lotSelect.addEventListener('change', () => {
    const selected = lotSelect.options[lotSelect.selectedIndex];
    const balance = selected.dataset.saldo;
    if (!balance) return;
    quantity.max = balance;
    quantity.placeholder = `Máximo disponível: ${balance}`;
    if (Number(quantity.value) > Number(balance)) quantity.value = balance;
  });
})();
