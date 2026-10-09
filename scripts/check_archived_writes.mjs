// Focused offline regression check. Requires Node 24; not a frontend build.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';

const base = new URL('../13-applications/encode-hackathon-story-blockchain/frontend/blocklibs/', import.meta.url);
async function load(name, mockAxios = false) {
  let source = stripTypeScriptTypes(readFileSync(new URL(name, base), 'utf8'));
  if (mockAxios) {
    assert.ok(source.includes("import axios from 'axios';"));
    source = source.replace("import axios from 'axios';", 'const axios = { get: async (url) => ({data: {url}}) };');
  }
  return import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`);
}
const story = await load('StoryProtocol.ts');
const ipfs = await load('ipfs.ts', true);
assert.throws(() => story.getStoryClient(), /writes are disabled/);
await assert.rejects(story.registerIPAsset({}), /writes are disabled/);
await assert.rejects(story.fileDispute('a', 'b', 'c'), /writes are disabled/);
await assert.rejects(ipfs.uploadToIPFS({}), /uploads are disabled/);
await assert.rejects(ipfs.uploadJSONToIPFS({}), /uploads are disabled/);
await assert.rejects(ipfs.uploadImageBufferToIPFS(new Uint8Array()), /uploads are disabled/);
assert.deepEqual(await ipfs.fetchFromIPFS('example'), {url: 'https://gateway.pinata.cloud/ipfs/example'});
console.log('PASS: six write entry points reject; public gateway read preserved (mock transport).');
