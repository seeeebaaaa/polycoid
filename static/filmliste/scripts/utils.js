async function api (url, body, csrf_token) {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token // CSRF token for Django POST requests
    },
    body: JSON.stringify(body)
  })

  if (response.redirected) {
    window.location.href = response.url
  }

  // Convert the response to JSON
  // const data = await response.json()
  return response
}


function hsvToRgb(h, s, v) {
  // Scale the hue from 0-1 to 0-360 degrees
  h = h * 360;

  let r, g, b;
  const i = Math.floor(h / 60);
  const f = h / 60 - i;
  const p = v * (1 - s);
  const q = v * (1 - f * s);
  const t = v * (1 - (1 - f) * s);

  switch (i % 6) {
      case 0: r = v; g = t; b = p; break;
      case 1: r = q; g = v; b = p; break;
      case 2: r = p; g = v; b = t; break;
      case 3: r = p; g = q; b = v; break;
      case 4: r = t; g = p; b = v; break;
      case 5: r = v; g = p; b = q; break;
  }

  return {
      r: Math.round(r * 255),
      g: Math.round(g * 255),
      b: Math.round(b * 255)
  };
}

function generateHSVGoldenColors(n, s=-1, v=-1) {
  golden_ratio_conjugate = 0.618033988749895
  colors = []
  h = Math.random()
  // range(n)
  for (i of [...Array(n).keys()]) {
    h += golden_ratio_conjugate
    h %= 1
    
    colors.push({"x":randomMargin(.5,.6), "y":randomMargin(.5,.6), "h": h*360, "s": s<0?randomMargin(.8,.2):s, "v": v<0?randomMargin(.6,.15):v })
  }
  console.log(colors);
  
  return colors
}

function randomMargin(x, n) {
  const min = x - n;
  const max = x + n;
  return Math.random() * (max - min) + min;
}

// Example usage:
const randomValue = randomMargin(50, 10);
console.log(randomValue); // Random value between 40 and 60
