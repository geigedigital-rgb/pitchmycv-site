const toIco = require('to-ico');
const { readFileSync, writeFileSync } = require('fs');
const { join } = require('path');

const root = join(__dirname, '..');
const buf16 = readFileSync(join(root, 'favicon-16x16.png'));
const buf32 = readFileSync(join(root, 'favicon-32x32.png'));

toIco([buf16, buf32]).then(ico => {
  writeFileSync(join(root, 'favicon.ico'), ico);
  console.log('Written favicon.ico');
}).catch(err => console.error(err));
