export function formatCurrency(value) {
  return '$' + Math.round(value).toLocaleString('es-CO');
}

export function formatPercent(value) {
  return `${value}%`;
}
