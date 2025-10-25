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
 * @fingerprint SH:JI2:6a9b2c3d4e5f60718293a4b5c6d7e8f9
 */

// Generate a QR PNG for the provided data string (returns PNG bytes)
export async function generateQrPng(data: string, size: number = 512): Promise<Uint8Array> {
  const QRCode = (await import('qrcode')).default as any;
  
  // toDataURL works in both browser and Node.js
  const dataUrl = await QRCode.toDataURL(data, {
    errorCorrectionLevel: 'M',
    margin: 1,
    width: size,
    color: { dark: '#000000', light: '#FFFFFF' },
  }) as string;

  // Convert data URL to Uint8Array
  const base64 = dataUrl.split(',')[1];
  const binaryString = atob(base64);
  const bytes = new Uint8Array(binaryString.length);
  for (let i = 0; i < binaryString.length; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }
  
  return bytes;
}


