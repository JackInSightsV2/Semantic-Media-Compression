/**
 * Copyright 2024-2025 Stephen Henry JackInSightsV2
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * 
 * @author Stephen Henry JackInSightsV2
 * @fingerprint SH:JI2:3e6f8a1c4b7d9e2f5a8c1d4e7b0a3c6f
 */

import axios from 'axios';

// Never ship a Pinata token in the browser bundle. No write backend exists yet.
const WRITE_DISABLED = 'IPFS uploads are disabled: an authenticated server-side credentials integration is required. Nothing was uploaded.';

export async function uploadToIPFS(_data: any): Promise<string> {
  throw new Error(WRITE_DISABLED);
}

export async function uploadJSONToIPFS(_json: any, _name: string = 'metadata.json'): Promise<string> {
  throw new Error(WRITE_DISABLED);
}

export async function uploadImageBufferToIPFS(
  _buffer: Uint8Array | ArrayBuffer,
  _name: string = 'image.png'
): Promise<string> {
  throw new Error(WRITE_DISABLED);
}

// Public read-only gateway access remains available.
export async function fetchFromIPFS(ipfsHash: string) {
  const response = await axios.get(`https://gateway.pinata.cloud/ipfs/${ipfsHash}`);
  return response.data;
}
