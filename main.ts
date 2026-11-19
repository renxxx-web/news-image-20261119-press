// Entry point for the make.fun "news-image-20261119" bounty.
//
// The deliverable is a single image — a broadsheet front page summing up
// Thursday 19 November 2026 — bundled in this repository as `entry.png`
// (see README.md and build/compose.py for how the page is composed).
// This program delivers that image to the harness output directory and
// then verifies the delivery: the copy must be byte-for-byte identical
// to the bundled file (length + SHA-256) and its PNG header must carry
// the required 1024x1024 dimensions. Any mismatch throws, so a truncated
// or corrupted write can never pass silently.

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });

const dest = join(outDir, "entry.png");
copyFileSync(source, dest);

const original = readFileSync(source);
const delivered = readFileSync(dest);

const sha256 = (buf: Buffer) => createHash("sha256").update(buf).digest("hex");
if (delivered.length !== original.length || sha256(delivered) !== sha256(original)) {
  throw new Error(`delivery mismatch: ${dest} differs from ${source}`);
}

// PNG signature (8 bytes) + IHDR: width and height are big-endian
// uint32s at byte offsets 16 and 20.
const isPng =
  delivered.length > 24 &&
  delivered.subarray(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]));
if (!isPng) {
  throw new Error("delivered file is not a PNG");
}
const width = delivered.readUInt32BE(16);
const height = delivered.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`unexpected dimensions ${width}x${height}, expected 1024x1024`);
}
if (delivered.length > 1024 * 1024) {
  throw new Error(`image is ${delivered.length} bytes, over the 1 MiB limit`);
}

console.log(
  `wrote ${dest} (${delivered.length} bytes, ${width}x${height}, sha256 ${sha256(delivered).slice(0, 12)}…)`,
);
