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

const PINATA_API_URL = 'https://api.pinata.cloud';

export async function uploadToIPFS(data: any) {
 try {
   const jsonString = JSON.stringify(data, null, 2);
   const blob = new Blob([jsonString], { type: 'application/json' });
  
   const formData = new FormData();
   formData.append('file', blob, 'semantic-data.json');
  
  const metadata = JSON.stringify({
    name: `Semantic Fingerprint - ${data.document_metadata?.title || data.metadata?.title || 'Untitled'}`,
    keyvalues: {
      content_id: data.content_id,
      type: 'semantic_fingerprint',
      // Contract Information
      license_type: data.contract_information?.license_type || 'CC-BY-SA-4.0',
      commercial_use: data.contract_information?.commercial_use?.toString() || 'false',
      derivative_works: data.contract_information?.derivative_works?.toString() || 'true',
      attribution_required: data.contract_information?.attribution_required?.toString() || 'true',
      compression_format: 'semantic_json_v1',
      story_protocol: 'true',
      blockchain: 'story_testnet',
    },
  });
  formData.append('pinataMetadata', metadata);
  
   const response = await axios.post(
     `${PINATA_API_URL}/pinning/pinFileToIPFS`,
     formData,
     {
       headers: {
         'Authorization': `Bearer ${process.env.NEXT_PUBLIC_PINATA_JWT}`,
         'Content-Type': 'multipart/form-data',
       },
     }
   );
  
   return response.data.IpfsHash; // Returns CID like "QmX..."
 } catch (error) {
   console.error('IPFS upload failed:', error);
   throw error;
 }
}

export async function fetchFromIPFS(ipfsHash: string) {
 try {
   // Use Pinata gateway or public IPFS gateway
   const response = await axios.get(`https://gateway.pinata.cloud/ipfs/${ipfsHash}`);
   return response.data;
 } catch (error) {
   console.error('IPFS fetch failed:', error);
   throw error;
 }
}


// Upload a JSON object to IPFS via Pinata's pinJSONToIPFS
export async function uploadJSONToIPFS(json: any, name: string = 'metadata.json') {
 try {
 	const body = {
 		pinataContent: json,
 		pinataMetadata: {
 			name,
 		},
 	};

 	const response = await axios.post(
 		`${PINATA_API_URL}/pinning/pinJSONToIPFS`,
 		body,
 		{
 			headers: {
 				'Authorization': `Bearer ${process.env.NEXT_PUBLIC_PINATA_JWT}`,
 				'Content-Type': 'application/json',
 			},
 		}
 	);

 	return response.data.IpfsHash as string;
 } catch (error) {
 	console.error('IPFS JSON upload failed:', error);
 	throw error;
 }
}

// Upload a PNG image buffer (e.g., generated QR) to IPFS via Pinata
export async function uploadImageBufferToIPFS(buffer: Uint8Array | ArrayBuffer, name: string = 'image.png') {
 try {
 	const blob = new Blob([buffer as ArrayBuffer], { type: 'image/png' });

 	const formData = new FormData();
 	formData.append('file', blob, name);

 	const response = await axios.post(
 		`${PINATA_API_URL}/pinning/pinFileToIPFS`,
 		formData,
 		{
 			headers: {
 				'Authorization': `Bearer ${process.env.NEXT_PUBLIC_PINATA_JWT}`,
 				'Content-Type': 'multipart/form-data',
 			},
 		}
 	);

 	return response.data.IpfsHash as string;
 } catch (error) {
 	console.error('IPFS image upload failed:', error);
 	throw error;
 }
}


