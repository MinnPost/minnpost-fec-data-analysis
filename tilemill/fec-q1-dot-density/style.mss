// Palette
@bg: #1A1818;
@obama: #40A2E7;
@romney: #E7404E;
@santorum: #EE7781;
@gingrich: #EB606C;
@paul: #E94957;

// Background for working with data
Map {
  background-color: @bg;
  background-color: transparent;
}

// Default sizes
#fec-dot-density {
  marker-width: 1;
  marker-allow-overlap: true;
  marker-line-width: 0;
  marker-opacity: .7;
}
#fec-dot-density::glow {
  marker-opacity: 0.1;
  marker-width: 3;
  marker-allow-overlap: true;
  marker-line-width: 0;
}

//Colors based on groups
#fec-dot-density,
#fec-dot-density::glow {
  [group = 'obama'] { marker-fill: @obama }
  [group = 'romney'] { marker-fill: @romney }
  [group = 'santorum'] { marker-fill: @santorum }
  [group = 'gingrich'] { marker-fill: @gingrich }
  [group = 'paul'] { marker-fill: @paul }
}

// Bigger dots as we zoom in
#fec-dot-density::glow[zoom <= 6] { marker-width: 2; }

#fec-dot-density[zoom >= 10] { marker-width: 2; }
#fec-dot-density::glow[zoom >= 10] { marker-width: 4; }

#fec-dot-density[zoom >= 13] { marker-width: 3; }
#fec-dot-density::glow[zoom >= 13] { marker-width: 6; }

// Zip lines
#fec-zip-stats {
  line-color: lighten(@bg, 20%);
  line-width: 0.5;
  line-opacity: 0.15;
  polygon-opacity: 0;
  polygon-fill: transparent;
}
