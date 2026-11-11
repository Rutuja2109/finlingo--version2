import { Capacitor } from "@capacitor/core";
import { NativePurchases, PURCHASE_TYPE } from "@capgo/native-purchases";
import { api } from "@/lib/api";

export const isNative = () => Capacitor.isNativePlatform();

// Ask Google Play for the live prices (they depend on the country); null if unavailable.
export async function livePrices(productId) {
  try {
    const { products } = await NativePurchases.getProducts({ productIdentifiers: [productId], productType: PURCHASE_TYPE.SUBS });
    return products || [];
  } catch { return []; }
}

// Opens the Play purchase sheet, then lets the server confirm with Google before anything is unlocked.
export async function buy(productId, basePlan) {
  const tx = await NativePurchases.purchaseProduct({
    productIdentifier: productId, planIdentifier: basePlan, productType: PURCHASE_TYPE.SUBS, autoAcknowledgePurchases: false,
  });
  if (!tx?.purchaseToken) throw new Error("Google Play did not return a purchase");
  await api.post("/subscription/verify", { product_id: productId, purchase_token: tx.purchaseToken });
}

// Re-send purchases Google already has (new phone, reinstall, or a verify that failed earlier).
// True if one worked, false if Google has none; throws the server's answer if Google has one but the server refused it.
export async function restore(productId) {
  if (!isNative()) return false;
  const { purchases } = await NativePurchases.getPurchases({ productType: PURCHASE_TYPE.SUBS });
  let lastErr = null;
  for (const p of purchases || []) {
    if (p.productIdentifier === productId && p.purchaseToken) {
      try { await api.post("/subscription/verify", { product_id: productId, purchase_token: p.purchaseToken }); return true; } catch (e) { lastErr = e; }
    }
  }
  if (lastErr) throw lastErr;
  return false;
}

export const cancelled = (e) => /cancel|user_cancel|closed|dismiss/i.test(String(e?.message || e));
export const manage = () => NativePurchases.manageSubscriptions().catch(() => {});
