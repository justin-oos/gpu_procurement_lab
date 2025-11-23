CREATE OR REPLACE TABLE `gpu_procurement_db.LEGACY_INV_MAIN_V2`
(
    ITEM_REF_ID STRING OPTIONS(description="Internal Product Reference ID (Non-Standard)"),
    LOC_BIN_HEX STRING OPTIONS(description="Warehouse Bin Location (Hex encoded). A1=Shipping, 55=Quarantine"),
    QOH_RAW_VAL INT64 OPTIONS(description="Quantity on Hand (Raw Value)"),
    LAST_TOUCH_DT_UNIX INT64 OPTIONS(description="Last movement timestamp in Unix Epoch"),
    STATUS_FLAG_9 INT64 OPTIONS(description="Inventory Status: 0=OK, 1=Reserved, 9=Legal Hold")
);

-- SEED DATA

-- 1. The "Decoy" H100 records (Standard Shipping Bin A1)
-- Shows 0 stock to fool the naive agent.
INSERT INTO `gpu_procurement_db.LEGACY_INV_MAIN_V2`
VALUES ('REF_H100_XIE', 'A1', 0, 1700000000, 0);

-- 2. The "Golden" Record (The Hidden Stock)
-- 300 units in Bin 55 (Quarantine) with Status 9 (Legal Hold).
-- This is what the Inventory Agent must find.
INSERT INTO `gpu_procurement_db.LEGACY_INV_MAIN_V2`
VALUES ('REF_H100_XIE', '55', 300, 1710000000, 9);

-- 3. Noise Data (Other products to make the DB look real)
INSERT INTO `gpu_procurement_db.LEGACY_INV_MAIN_V2`
VALUES ('REF_A100_NV', 'A1', 50, 1705000000, 0);

INSERT INTO `gpu_procurement_db.LEGACY_INV_MAIN_V2`
VALUES ('REF_RTX4090', 'B2', 1200, 1706000000, 0);