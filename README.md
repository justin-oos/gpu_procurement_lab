# 🛠️ Environment Setup

## Step 1: Deploy Cloud Resources

Deploy Resources via Makefile:
```bash
make deploy project=YOUR_PROJECT_ID
```

## Step 2a: Run a Live Demo for a given Phase

To run a specific demo phase, use the **make run** target with the phase number input.

```bash
make run phase=YOUR_PHASE_NUMBER
```

For example

```bash
make run phase=1
```

## Step 2b: Run a Headless Test for a given Phase

To run a headless test for a specific demo phase, use the **make test** target with the phase number input.

```bash
make test phase=YOUR_PHASE_NUMBER
```

For example

```bash
make test phase=1
```

## Step 3: Destroy Cloud Resources

Destroy Resources via Makefile:
```bash
make destroy
```

# 🛠️ Environment Phase Overview

## Phase 1

```mermaid
graph TD
    subgraph "Phase 1"
        root_agent_P1("root_agent");

        subgraph "Sub-Agents"
            inventory_agent_P1("inventory_agent");
            legal_agent_P1("legal_agent");
            logistics_agent_P1("logistics_agent");
            purchase_order_agent_P1("purchase_order_agent");
        end

        subgraph "Tools"
            CommanderTools_P1["fs.read_file, fs.write_file, fs.append_to_log, fs.list_files, reporter.upload_report"];
            InventoryTools_P1["db.explore_schema, db.run_query"];
            LegalTools_P1["rag.analyze_contract_clause"];
            LogisticsTools_P1["api.fetch_spot_prices, api.estimate_shipping"];
            PurchaseOrderTools_P1["fs.read_file, fs.write_file, reporter.upload_report"];
        end

        root_agent_P1 --> inventory_agent_P1;
        root_agent_P1 --> legal_agent_P1;
        root_agent_P1 --> logistics_agent_P1;
        root_agent_P1 --> purchase_order_agent_P1;

        root_agent_P1 --> CommanderTools_P1;
        inventory_agent_P1 --> InventoryTools_P1;
        legal_agent_P1 --> LegalTools_P1;
        logistics_agent_P1 --> LogisticsTools_P1;
        purchase_order_agent_P1 --> PurchaseOrderTools_P1;
    end
```

## Phase 2

```mermaid
graph TD
    subgraph "Phase 2"
        root_agent_P2("root_agent");

        subgraph "Orchestrators"
            source_gpus_agent("source_gpus_agent");
            source_gpus_parallel_agent("source_gpus_parallel_agent");
            source_gpus_merge_agent("source_gpus_merge_agent");
        end

        subgraph "Sub-Agents"
            inventory_agent_P2("inventory_agent");
            legal_agent_P2("legal_agent");
            logistics_agent_P2("logistics_agent");
        end

        subgraph "Tools"
            MergeTools_P2["fs.read_file, fs.write_file, fs.append_to_log, fs.list_files, reporter.upload_report"];
            InventoryTools_P2["db.explore_schema, db.run_query"];
            LegalTools_P2["rag.analyze_contract_clause"];
            LogisticsTools_P2["api.fetch_spot_prices, api.estimate_shipping"];
        end

        root_agent_P2 --> source_gpus_agent;
        source_gpus_agent --> source_gpus_parallel_agent;
        source_gpus_agent --> source_gpus_merge_agent;

        source_gpus_parallel_agent --> inventory_agent_P2;
        source_gpus_parallel_agent --> legal_agent_P2;
        source_gpus_parallel_agent --> logistics_agent_P2;

        source_gpus_merge_agent --> MergeTools_P2;
        inventory_agent_P2 --> InventoryTools_P2;
        legal_agent_P2 --> LegalTools_P2;
        logistics_agent_P2 --> LogisticsTools_P2;
    end
```
