(() => {
  const newProduct = document.querySelector('#origem-novo');
  const existingProduct = document.querySelector('#origem-existente');
  const productFields = document.querySelector('#campos-produto-novo');
  const existingFields = document.querySelector('#campos-produto-existente');
  const newLotFields = document.querySelector('#campos-novo-lote');
  const newLot = document.querySelector('#lote-novo');
  const existingLot = document.querySelector('#lote-existente');
  const lotSelection = document.querySelector('#selecao-lote-existente');
  const productSelect = document.querySelector('#produto_id');
  const lotSelect = document.querySelector('#lote_id');
  const mode = document.querySelector('#modo_entrada');

  const setDisabled = (container, disabled) => {
    container.querySelectorAll('input, select').forEach((field) => { field.disabled = disabled; });
  };

  const filterLots = () => {
    const productId = productSelect.value;
    [...lotSelect.options].forEach((option) => {
      option.hidden = Boolean(option.value) && option.dataset.produtoId !== productId;
    });
    lotSelect.value = '';
  };

  const update = () => {
    const isNewProduct = newProduct.checked;
    const usesExistingLot = !isNewProduct && existingLot.checked;
    productFields.classList.toggle('d-none', !isNewProduct);
    existingFields.classList.toggle('d-none', isNewProduct);
    newLotFields.classList.toggle('d-none', usesExistingLot);
    lotSelection.classList.toggle('d-none', !usesExistingLot);
    setDisabled(productFields, !isNewProduct);
    setDisabled(existingFields, isNewProduct);
    setDisabled(newLotFields, usesExistingLot);
    lotSelect.disabled = !usesExistingLot;
    if (isNewProduct) mode.value = 'novo_produto';
    else if (usesExistingLot) mode.value = 'lote_existente';
    else mode.value = 'produto_existente_novo_lote';
    if (!isNewProduct) filterLots();
  };

  [newProduct, existingProduct, newLot, existingLot].forEach((field) => field.addEventListener('change', update));
  productSelect.addEventListener('change', filterLots);
  update();
})();
