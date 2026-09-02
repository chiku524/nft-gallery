"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";

export type WalletChain = {
  name: string;
  chainIdHex: string;
  currency: string;
  rpcUrl: string;
  explorer: string;
};

declare global {
  interface Window {
    ethereum?: {
      request: (args: { method: string; params?: unknown[] }) => Promise<unknown>;
    };
  }
}

export function AddChainButton({ chain }: { chain: WalletChain }) {
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
            chainId: chain.chainIdHex,
            chainName: chain.name,
            nativeCurrency: {
              name: chain.currency === "ETH" ? "Ether" : chain.currency,
              symbol: chain.currency,
              decimals: 18,
            },
            rpcUrls: [chain.rpcUrl],
            blockExplorerUrls: [chain.explorer],
          },
        ],
      });
      setMessage(`${chain.name} is on this wallet.`);
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
        {busy ? "Waiting on wallet…" : `Add ${chain.name}`}
      </Button>
      {message ? <p className="text-sm text-muted-foreground">{message}</p> : null}
    </div>
  );
}
