-- Migration 20260628154500: force HitPay/SGD-only payment configuration
-- Description: Move tenants to SGD/$ and clear legacy online payment provider secrets.
-- Date: 2026-06-28 15:45:00

UPDATE tenant
SET currency_code = 'SGD',
    currency = '$',
    stripe_secret_key = NULL,
    stripe_publishable_key = NULL,
    revolut_merchant_secret = NULL;
