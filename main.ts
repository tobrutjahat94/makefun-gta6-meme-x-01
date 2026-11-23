// Entrypoint entri gta6-meme-x-01.
// Tugas program ini cuma satu: meneruskan POST.json dari folder bot ke folder
// output, tempat gate membacanya untuk menemukan postingan X yang dinilai.
// Jalankan lokal: MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import * as fs from 'node:fs';
import * as path from 'node:path';

const POST_FILE = 'POST.json';

function resolveDir(envName: string, defaultPath: string): string {
  const fromEnv = process.env[envName];
  if (fromEnv === undefined || fromEnv.trim() === '') {
    return defaultPath;
  }
  return fromEnv;
}

function run(): number {
  const botFolder = resolveDir('MAKEFUN_BOT_DIR', '/bot');
  const outFolder = resolveDir('MAKEFUN_OUTPUT_DIR', '/output');

  const inputPath = path.join(botFolder, POST_FILE);
  const outputPath = path.join(outFolder, POST_FILE);

  let payload: Buffer;
  try {
    payload = fs.readFileSync(inputPath);
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error);
    console.error(`tidak bisa membaca ${POST_FILE} di ${botFolder}: ${reason}`);
    return 1;
  }

  fs.mkdirSync(outFolder, { recursive: true });
  fs.writeFileSync(outputPath, payload);
  console.log(`${POST_FILE} diteruskan: ${inputPath} -> ${outputPath}`);
  return 0;
}

process.exit(run());
