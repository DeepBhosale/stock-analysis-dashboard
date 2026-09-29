export function renderPath(points: number[], min: number, max: number, width: number, height: number, xOffset = 0, yOffset = 0) {
  const range = max - min || 1;
  return points.map((value, index) => {
    const x = xOffset + (index / (points.length - 1)) * width;
    const y = yOffset + height - ((value - min) / range) * height;
    return `${index === 0 ? 'M' : 'L'} ${x.toFixed(2)} ${y.toFixed(2)}`;
  }).join(' ');
}

export function renderArea(points: number[], min: number, max: number, width: number, height: number, xOffset = 0, yOffset = 0) {
  const range = max - min || 1;
  const area = points.map((value, index) => {
    const x = xOffset + (index / (points.length - 1)) * width;
    const y = yOffset + height - ((value - min) / range) * height;
    return `${index === 0 ? 'M' : 'L'} ${x.toFixed(2)} ${y.toFixed(2)}`;
  }).join(' ');
  return `${area} L ${xOffset + width} ${yOffset + height} L ${xOffset} ${yOffset + height} Z`;
}