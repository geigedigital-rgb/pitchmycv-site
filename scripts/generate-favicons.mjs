#!/usr/bin/env node
/**
 * Generate favicon PNG/ICO from favicon.svg using sharp.
 * Run: node scripts/generate-favicons.mjs
 * Requires: npm install sharp
 */
import sharp from 'sharp';
import { readFileSync, writeFileSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const svgPath = join(root, 'favicon.svg');
const svg = readFileSync(svgPath);

const sizes = [
  { name: 'favicon-16x16.png', size: 16 },
  { name: 'favicon-32x32.png', size: 32 },
  { name: 'apple-touch-icon.png', size: 180 },
  { name: 'android-chrome-192x192.png', size: 192 },
  { name: 'android-chrome-512x512.png', size: 512 },
];

for (const { name, size } of sizes) {
  const out = join(root, name);
  await sharp(svg).resize(size, size).png().toFile(out);
  console.log('Written', name);
}

console.log('Done. For favicon.ico use favicon-32x32.png or generate at https://realfavicongenerator.net/');
