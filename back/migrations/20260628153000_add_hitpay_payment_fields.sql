-- Migration 20260628153000: add HitPay payment configuration and order link
-- Description: Store HitPay tenant credentials and payment request IDs for online checkout.
-- Date: 2026-06-28 15:30:00

ALTER TABLE tenant
ADD COLUMN IF NOT EXISTS hitpay_api_key TEXT DEFAULT NULL;

ALTER TABLE tenant
ADD COLUMN IF NOT EXISTS hitpay_webhook_salt TEXT DEFAULT NULL;

ALTER TABLE tenant
ADD COLUMN IF NOT EXISTS hitpay_mode VARCHAR(16) DEFAULT 'sandbox';

ALTER TABLE "order"
ADD COLUMN IF NOT EXISTS hitpay_payment_request_id VARCHAR(255) DEFAULT NULL;

CREATE INDEX IF NOT EXISTS ix_order_hitpay_payment_request_id
ON "order"(hitpay_payment_request_id);
