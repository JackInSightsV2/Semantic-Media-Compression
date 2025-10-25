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
 * @fingerprint SH:JI2:9c2e5f8a1b4d7c0e3f6a9c2e5b8d1f4a
 */

export function shortenAddress(address: string): string {
    if (!address) return '';
    return `${address.slice(0, 6)}...${address.slice(-4)}`;
   }
   
   export function getExplorerUrl(txHash: string): string {
    return `https://aeneid.explorer.story.foundation/transactions/${txHash}`;
   }
   
   export function getIPFSUrl(hash: string): string {
    return `https://gateway.pinata.cloud/ipfs/${hash}`;
   }
   
  export function getIPAssetUrl(tokenId: string): string {
    return `https://aeneid.storyscan.io/token/0xbAc50238B65bc4F55c3729406e508f9174525d33/instance/${tokenId}?tab=metadata`;
  }
   
   
   