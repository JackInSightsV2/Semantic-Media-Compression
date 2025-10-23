export function shortenAddress(address: string): string {
    if (!address) return '';
    return `${address.slice(0, 6)}...${address.slice(-4)}`;
   }
   
   export function getExplorerUrl(txHash: string): string {
    return `https://testnet.storyscan.xyz/tx/${txHash}`;
   }
   
   export function getIPFSUrl(hash: string): string {
    return `https://gateway.pinata.cloud/ipfs/${hash}`;
   }
   
   export function getIPAssetUrl(ipAssetId: string): string {
    return `https://testnet.storyscan.xyz/address/${ipAssetId}`;
   }
   
   
   