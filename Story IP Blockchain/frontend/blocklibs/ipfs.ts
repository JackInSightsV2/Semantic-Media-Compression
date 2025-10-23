import axios from 'axios';

const PINATA_API_URL = 'https://api.pinata.cloud';

export async function uploadToIPFS(data: any) {
 try {
   const jsonString = JSON.stringify(data, null, 2);
   const blob = new Blob([jsonString], { type: 'application/json' });
  
   const formData = new FormData();
   formData.append('file', blob, 'semantic-data.json');
  
   const metadata = JSON.stringify({
     name: `Semantic Fingerprint - ${data.metadata?.title || 'Untitled'}`,
     keyvalues: {
       content_id: data.content_id,
       type: 'semantic_fingerprint',
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


