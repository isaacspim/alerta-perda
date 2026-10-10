(() => {
  const card = document.querySelector('#cartao-clima');
  if (!card) return;

  const endpoint = new URL('https://api.open-meteo.com/v1/forecast');
  endpoint.search = new URLSearchParams({
    latitude: card.dataset.latitude,
    longitude: card.dataset.longitude,
    current: 'temperature_2m,relative_humidity_2m,weather_code',
    daily: 'temperature_2m_max,temperature_2m_min,precipitation_probability_max',
    forecast_days: '10',
    timezone: 'America/Sao_Paulo',
  });

  const descriptions = {
    0: 'Céu limpo', 1: 'Predominantemente limpo', 2: 'Parcialmente nublado',
    3: 'Nublado', 45: 'Neblina', 48: 'Neblina com geada', 51: 'Garoa fraca',
    53: 'Garoa moderada', 55: 'Garoa intensa', 61: 'Chuva fraca',
    63: 'Chuva moderada', 65: 'Chuva intensa', 80: 'Pancadas de chuva fracas',
    81: 'Pancadas de chuva moderadas', 82: 'Pancadas de chuva intensas', 95: 'Trovoada',
  };

  const setText = (id, value) => { document.querySelector(`#${id}`).textContent = value; };

  fetch(endpoint)
    .then((response) => {
      if (!response.ok) throw new Error('Resposta meteorológica inválida');
      return response.json();
    })
    .then((data) => {
      const current = data.current;
      const daily = data.daily;
      setText('clima-atualizacao', `${card.dataset.localidade} · Atualizado em ${current.time}`);
      setText('clima-temperatura', `${current.temperature_2m} °C`);
      setText('clima-umidade', `${current.relative_humidity_2m}%`);
      setText('clima-chuva', `${daily.precipitation_probability_max[0]}%`);
      setText('clima-condicao', descriptions[current.weather_code] || 'Condição não informada');
      setText('clima-previsao', `Previsão de hoje: mínima de ${daily.temperature_2m_min[0]} °C e máxima de ${daily.temperature_2m_max[0]} °C. Use essas informações como apoio à rotina; elas não substituem a conferência dos produtos e equipamentos.`);
    })
    .catch(() => {
      setText('clima-atualizacao', 'Dados temporariamente indisponíveis.');
    });
})();
