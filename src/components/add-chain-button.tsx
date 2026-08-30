"use client";

import { useState } from "react";
import { collection } from "@/data/collection";
import { Button } from "@/components/ui/button";

declare global {
  interface Window {
    ethereum?: {
      request: (args: { method: string; params?: unknown[] }) => Promise<unknown>;
    };
  }
}

export function AddChainButton() {
  const [message, setMessage] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function addChain() {
    setBusy(true);
    setMessage(null);
    try {
      if (!window.ethereum) {
        setMessage("No wallet detected. Install an EVM wallet, then try again.");
        return;
      }
      await window.ethereum.request({
        method: "wallet_addEthereumChain",
        params: [
          {
            chainId: collection.chain.chainIdHex,
            chainName: collection.chain.name,
            nativeCurrency: {
              name: "Ether",
              symbol: collection.chain.currency,
              decimals: 18,
            },
            rpcUrls: [collection.chain.rpcUrl],
            blockExplorerUrls: [collection.chain.explorer],
          },
        ],
      });
      setMessage(`${collection.chain.name} is on this wallet.`);
    } catch (error) {
      const text = error instanceof Error ? error.message : "Wallet rejected the request.";
      setMessage(text);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-2">
      <Button type="button" onClick={addChain} disabled={busy} size="lg">
        {busy ? "Waiting on wallet…" : `Add ${collection.chain.name}`}
      </Button>
      {message ? <p className="text-sm text-muted-foreground">{message}</p> : null}
    </div>
  );
}
