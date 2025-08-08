# 📚 Documentation Index: pump-fun-bot

*Generated on 2025-08-07 20:58:43*

## 🌳 Directory Structure

```
📁 pump-fun-bot/
├── 📁 .venv/
├── 📁 bots/
│   ├── 📄 bot-sniper-1-geyser.yaml
│   ├── 📄 bot-sniper-2-logs.yaml
│   ├── 📄 bot-sniper-3-blocks.yaml
│   └── 📄 bot-sniper-4-pp.yaml
├── 📁 idl/
│   ├── 📄 pump_fun_idl.json
│   ├── 📄 pump_swap_idl.json
│   ├── 📄 raydium_amm_idl.json
│   └── 📄 raydium_launchlab_idl.json
├── 📁 learning-examples/
│   ├── 📁 blockSubscribe-transactions/
│   │   └── 📄 raw_create_tx_from_blockSubscribe.json
│   ├── 📁 bonding-curve-progress/
│   │   ├── 📄 get_bonding_curve_status.py
│   │   ├── 📄 get_graduating_tokens.py
│   │   └── 📄 poll_bonding_curve_progress.py
│   ├── 📁 listen-migrations/
│   │   ├── 📄 compare_migration_listeners.py
│   │   ├── 📄 listen_blocksubscribe_old_raydium.py
│   │   ├── 📄 listen_logsubscribe.py
│   │   └── 📄 listen_programsubscribe.py
│   ├── 📁 listen-new-tokens/
│   │   ├── 📁 generated/
│   │   ├── 📁 proto/
│   │   ├── 📄 compare_listeners.py
│   │   ├── 📄 listen_blocksubscribe.py
│   │   ├── 📄 listen_geyser.py
│   │   ├── 📄 listen_logsubscribe.py
│   │   ├── 📄 listen_logsubscribe_abc.py
│   │   └── 📄 listen_pumpportal.py
│   ├── 📁 pumpswap/
│   │   ├── 📄 get_pumpswap_pools.py
│   │   ├── 📄 manual_buy_pumpswap.py
│   │   └── 📄 manual_sell_pumpswap.py
│   ├── 📄 blockSubscribe_extract_transactions.py
│   ├── 📄 calculate_discriminator.py
│   ├── 📄 cleanup_accounts.py
│   ├── 📄 compute_associated_bonding_curve.py
│   ├── 📄 decode_from_blockSubscribe.py
│   ├── 📄 decode_from_getAccountInfo.py
│   ├── 📄 decode_from_getTransaction.py
│   ├── 📄 decoded_buy_tx_from_getTransaction.json
│   ├── 📄 decoded_create_tx_from_getTransaction.json
│   ├── 📄 fetch_price.py
│   ├── 📄 manual_buy.py
│   ├── 📄 manual_sell.py
│   ├── 📄 mint_and_buy.py
│   ├── 📄 raw_bondingCurve_from_getAccountInfo.json
│   ├── 📄 raw_buy_tx_from_getTransaction.json
├── 📁 logs/
│   └── 📄 bot-sniper-2_20250807_195039.log
├── 📁 src/
│   ├── 📁 __pycache__/
│   ├── 📁 cleanup/
│   │   ├── 📁 __pycache__/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 manager.py
│   │   └── 📄 modes.py
│   ├── 📁 core/
│   │   ├── 📁 __pycache__/
│   │   ├── 📁 priority_fee/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 client.py
│   │   ├── 📄 pubkeys.py
│   │   └── 📄 wallet.py
│   ├── 📁 geyser/
│   │   ├── 📁 generated/
│   │   └── 📁 proto/
│   ├── 📁 interfaces/
│   │   ├── 📁 __pycache__/
│   │   └── 📄 core.py
│   ├── 📁 monitoring/
│   │   ├── 📁 __pycache__/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 base_listener.py
│   │   ├── 📄 listener_factory.py
│   │   ├── 📄 universal_block_listener.py
│   │   ├── 📄 universal_geyser_listener.py
│   │   ├── 📄 universal_logs_listener.py
│   │   └── 📄 universal_pumpportal_listener.py
│   ├── 📁 platforms/
│   │   ├── 📁 __pycache__/
│   │   ├── 📁 letsbonk/
│   │   ├── 📁 pumpfun/
│   │   └── 📄 __init__.py
│   ├── 📁 pump_bot.egg-info/
│   │   ├── 📄 dependency_links.txt
│   │   ├── 📄 entry_points.txt
│   │   ├── 📄 PKG-INFO
│   │   ├── 📄 requires.txt
│   │   ├── 📄 SOURCES.txt
│   │   └── 📄 top_level.txt
│   ├── 📁 trading/
│   │   ├── 📁 __pycache__/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 base.py
│   │   ├── 📄 platform_aware.py
│   │   ├── 📄 position.py
│   │   └── 📄 universal_trader.py
│   ├── 📁 utils/
│   │   ├── 📁 __pycache__/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 idl_manager.py
│   │   ├── 📄 idl_parser.py
│   │   └── 📄 logger.py
│   ├── 📄 __init__.py
│   ├── 📄 bot_runner.py
│   ├── 📄 config_loader.py
│   ├── 📄 granular_client.py
│   ├── 📄 mcp_client.py
│   └── 📄 mcp_server.py
├── 📁 trades/
│   └── 📄 trades.log
├── 📄 .env
├── 📄 LICENSE
├── 📄 MAINTAINERS.md
├── 📄 pyproject.toml
├── 📄 README.md
└── 📄 uv.lock
```

## 📊 Summary

- **Total Files**: 111
- **Processed Successfully**: 111
- **Cache Directory**: `.index_cache/`

## 📄 File Summaries

### 📄 `.env`

The '.env' file contains environment variables used for configuring a project, specifically related to Solana blockchain endpoints, Geyser API access, and Google API credentials. Its main purpose is to securely store sensitive information and configuration settings that the application requires to connect to external services and APIs without hardcoding them in the source code.

### 📄 `.env.example`

The `.env.example` file serves as a template for environment variables required by the project, specifically for connecting to Solana nodes and a Geyser API. It outlines necessary configurations, such as RPC and WebSocket endpoints, API tokens, and authentication types, guiding developers in setting up their local environment.

### 📄 `LICENSE`

The 'LICENSE' file contains the terms and conditions of the Apache License Version 2.0, which governs the use, reproduction, and distribution of the associated software or project. Its main purpose is to provide legal guidelines for users and contributors, ensuring that they understand their rights and obligations when using or modifying the software.

### 📄 `MAINTAINERS.md`

The 'MAINTAINERS.md' file lists the individuals responsible for maintaining the project, including their roles and contact information. Its main purpose is to provide a clear point of contact for contributors and users seeking assistance or guidance regarding issues and project management.

### 📄 `README.md`

The 'README.md' file provides an overview of the Chainstack project, which enables users to create trading bots for platforms like pump.fun and letsbonk.fun, focusing on sniping new tokens. It includes setup instructions, prerequisites, and configuration details, along with warnings about potential scams and the project's intended use for learning rather than production.

### 📄 `bots/bot-sniper-1-geyser.yaml`

The 'bots/bot-sniper-1-geyser.yaml' file is a configuration file for a bot designed to automate trading on the Solana blockchain using the Geyser API. Its main purpose is to define various operational parameters, such as trading strategies, retry mechanisms, and connection endpoints, enabling the bot to efficiently execute buy and sell orders based on predefined criteria.

### 📄 `bots/bot-sniper-2-logs.yaml`

The file 'bots/bot-sniper-2-logs.yaml' contains configuration settings for a trading bot designed to operate on the Solana blockchain. Its main purpose is to define parameters for trading strategies, including trade execution settings, priority fee management, token selection filters, and cleanup processes, allowing users to customize the bot's behavior according to their trading preferences and risk tolerance.

### 📄 `bots/bot-sniper-3-blocks.yaml`

The file 'bots/bot-sniper-3-blocks.yaml' contains configuration settings for a trading bot designed to operate on the Solana blockchain. Its main purpose is to define parameters for trading strategies, including trade execution, priority fees, token selection filters, and cleanup procedures, allowing users to customize the bot's behavior according to their trading preferences and risk tolerance.

### 📄 `bots/bot-sniper-4-pp.yaml`

The file 'bots/bot-sniper-4-pp.yaml' contains configuration settings for a trading bot designed to operate on the Solana blockchain, specifically for executing trades based on market conditions and user-defined parameters. Its main purpose is to facilitate automated trading strategies, including buy/sell execution, risk management, and token selection, while allowing users to customize various operational settings to align with their trading strategies and risk tolerance.

### 📄 `idl/pump_fun_idl.json`

The file 'idl/pump_fun_idl.json' contains an Interface Definition Language (IDL) specification for a smart contract named "pump," which is part of a blockchain project. Its main purpose is to define the instructions and associated metadata for interacting with the contract, including functions like setting a creator and updating token incentives, along with the required accounts and arguments for each instruction.

### 📄 `idl/pump_swap_idl.json`

The file 'pump_swap_idl.json' defines the interface description language (IDL) for a decentralized finance (DeFi) application related to a liquidity pool, specifically a pump automated market maker (AMM). It contains metadata about the application, including its version and description, as well as detailed instructions for administrative functions such as setting coin creators and updating token incentives, outlining the required accounts and arguments for each instruction. Its main purpose is to facilitate interaction with the smart contract by providing a structured representation of its functionalities and requirements.

### 📄 `idl/raydium_amm_idl.json`

The file 'idl/raydium_amm_idl.json' contains the Interface Definition Language (IDL) for the Raydium Automated Market Maker (AMM) on the Solana blockchain. Its main purpose is to define the various instructions, accounts, and arguments required for interacting with the Raydium AMM, facilitating operations such as initialization, monitoring, and depositing assets within the decentralized finance (DeFi) ecosystem.

### 📄 `idl/raydium_launchlab_idl.json`

The file 'idl/raydium_launchlab_idl.json' contains the Interface Definition Language (IDL) for the Raydium Launchpad, detailing the smart contract's structure, including its address, metadata, and instructions for token transactions. Its main purpose is to define the functions and associated parameters for executing token swaps within the Raydium ecosystem, facilitating interactions between users and the protocol's smart contracts.

### 📄 `learning-examples/blockSubscribe-transactions/raw_create_tx_from_blockSubscribe.json`

The file 'raw_create_tx_from_blockSubscribe.json' contains a serialized transaction in JSON format, including details such as the transaction's base64-encoded data, associated fees, pre- and post-balances for involved accounts, and inner instructions executed during the transaction. Its main purpose is to serve as an example of how to create and structure transactions using the block subscription feature in the project's blockchain framework, facilitating developers in understanding transaction handling and execution.

### 📄 `learning-examples/blockSubscribe_extract_transactions.py`

The file `blockSubscribe_extract_transactions.py` is an asynchronous Python script that connects to a Solana blockchain WebSocket endpoint to listen for transaction notifications related to a specific program. Its main purpose is to subscribe to block updates, extract transaction data, and save the details of each transaction to a JSON file, using a hashed signature as the filename for easy retrieval.

### 📄 `learning-examples/bonding-curve-progress/get_bonding_curve_status.py`

The file `get_bonding_curve_status.py` is a Python script designed to check the status of a token's bonding curve on the Solana network, specifically using the Pump.fun program. Its main role is to query and display the bonding curve state and completion status, allowing users to understand the current status of a specified token's bonding curve.

### 📄 `learning-examples/bonding-curve-progress/get_graduating_tokens.py`

The file `get_graduating_tokens.py` is a Python module designed for querying and analyzing soon-to-graduate tokens within the Pump.fun program. Its primary role is to fetch bonding curve accounts based on token reserves, allowing users to identify and retrieve associated SPL token accounts while handling potential performance issues with RPC calls.

### 📄 `learning-examples/bonding-curve-progress/poll_bonding_curve_progress.py`

The file `poll_bonding_curve_progress.py` is a Python module designed to continuously monitor and report the status of a bonding curve associated with a Pump.fun token on the Solana blockchain. Its main purpose is to poll the bonding curve's state at regular intervals, decode the relevant data, and print updates regarding token and SOL reserves, as well as overall progress towards completion.

### 📄 `learning-examples/calculate_discriminator.py`

The file `calculate_discriminator.py` contains a function that computes a unique discriminator value for a specified instruction name using the SHA256 hashing algorithm. Its main purpose is to generate a 64-bit unsigned integer that serves as an identifier for instructions in a blockchain context, specifically for use with the Anchor framework.

### 📄 `learning-examples/cleanup_accounts.py`

The file `cleanup_accounts.py` is a Python script designed to interact with the Solana blockchain, specifically to close token accounts and reclaim rent by burning any remaining tokens. Its main purpose is to safely manage and clean up associated token accounts for a specified mint address, ensuring that accounts are closed only if they exist and are empty, while logging the process for transparency.

### 📄 `learning-examples/compute_associated_bonding_curve.py`

The file `compute_associated_bonding_curve.py` contains functions to derive the bonding curve address and its associated token account for a given token mint in a blockchain environment. Its main purpose is to facilitate the calculation of bonding curves and their associated accounts, which are essential for managing token interactions within the project.

### 📄 `learning-examples/decode_from_blockSubscribe.py`

The file `decode_from_blockSubscribe.py` is a Python script designed to decode transaction data from a blockchain, specifically targeting a program related to the Pump Fun protocol. Its main purpose is to read transaction data, decode instructions based on an interface definition language (IDL), and output the decoded instructions along with their associated accounts and program IDs, facilitating the analysis of blockchain transactions.

### 📄 `learning-examples/decode_from_getAccountInfo.py`

The file `decode_from_getAccountInfo.py` is a Python script that decodes bonding curve data from a base64 encoded JSON response, parses it into a structured format, and calculates the price of tokens based on the bonding curve state. Its main purpose is to facilitate the extraction and interpretation of financial data related to token reserves and pricing in a blockchain context, specifically for applications involving decentralized finance (DeFi) protocols.

### 📄 `learning-examples/decode_from_getTransaction.py`

The file `decode_from_getTransaction.py` is a Python script designed to decode and extract transaction data from a JSON file, specifically for transactions related to a program identified as "Pump Fun." Its main purpose is to parse transaction instructions, decode specific instruction data (like "create" and "buy"), and display the relevant transaction details, including account information and decoded parameters.

### 📄 `learning-examples/decoded_buy_tx_from_getTransaction.json`

The file 'decoded_buy_tx_from_getTransaction.json' contains a detailed representation of a decoded transaction related to a buy operation on a blockchain. Its main purpose is to provide structured information about the transaction's accounts, instructions, and parsed data, facilitating easier analysis and debugging within the project's transaction processing framework.

### 📄 `learning-examples/decoded_create_tx_from_getTransaction.json`

The file 'decoded_create_tx_from_getTransaction.json' contains a decoded representation of a transaction in JSON format, detailing the account keys, instructions, and signatures involved in the transaction. Its main purpose is to provide a structured view of the transaction data, including actions such as transferring funds and creating associated token accounts, facilitating easier analysis and debugging within the project.

### 📄 `learning-examples/fetch_price.py`

The file `fetch_price.py` is a Python script designed to interact with the Solana blockchain to fetch and calculate the price of a token based on its bonding curve state. Its main purpose is to retrieve the current state of a specified bonding curve from the blockchain, validate the data, and compute the token price in SOL, providing a useful tool for developers working with decentralized finance applications on Solana.

### 📄 `learning-examples/listen-migrations/compare_migration_listeners.py`

The file `compare_migration_listeners.py` is a Python script designed to compare two methods of detecting market migrations in a blockchain environment: one using a migration program listener and the other using a direct market account listener. Its main purpose is to track and analyze the performance of these detection methods, providing detailed statistics on which method detects new markets first and the efficiency of each listener across different providers.

### 📄 `learning-examples/listen-migrations/listen_blocksubscribe_old_raydium.py`

The file `listen_blocksubscribe_old_raydium.py` is a Python script designed to listen for blockchain events related to the Raydium liquidity pool on the Solana network. Its main purpose is to connect to a WebSocket endpoint, subscribe to block notifications, and process transactions that include a specific "initialize2" instruction, extracting and displaying relevant transaction details such as token and liquidity pool addresses.

### 📄 `learning-examples/listen-migrations/listen_logsubscribe.py`

The file `listen_logsubscribe.py` is a Python script that connects to a Solana migration program via WebSocket to listen for 'Migrate' instructions. Its main purpose is to parse and log transaction details related to successful migrations, while handling errors and skipping transactions with truncated logs.

### 📄 `learning-examples/listen-migrations/listen_programsubscribe.py`

The file `listen_programsubscribe.py` is a Python script that monitors the Solana blockchain for new Pump AMM market accounts using WebSocket connections. Its main purpose is to fetch existing market data, filter out already known markets, and parse the account data of new markets, while excluding user-created markets, thereby facilitating real-time market monitoring and updates.

### 📄 `learning-examples/listen-new-tokens/compare_listeners.py`

The file `compare_listeners.py` is a Python script designed to compare four different methods for detecting new Pump.fun tokens in a blockchain environment. Its main purpose is to track and analyze the performance of each detection method—block subscription, Geyser gRPC, logs subscription, and PumpPortal WebSocket—by measuring which method detects new tokens first and providing detailed performance statistics.

### 📄 `learning-examples/listen-new-tokens/generated/__init__.py`

The file `__init__.py` in the `learning-examples/listen-new-tokens/generated/` directory serves as an initializer for the package, allowing it to be treated as a module in Python. It typically contains package-level documentation or imports necessary components, facilitating the organization and accessibility of the package's functionalities. Its main purpose is to enable the inclusion of the package in Python's module search path and to define the package's interface.

### 📄 `learning-examples/listen-new-tokens/generated/geyser_pb2.py`

The file `geyser_pb2.py` is an auto-generated Python module that contains protocol buffer definitions for the Geyser service, based on the `geyser.proto` file. Its main purpose is to facilitate communication between components of the project by defining the structure of messages used for subscribing to updates related to accounts, transactions, and blocks within a Solana blockchain context.

### 📄 `learning-examples/listen-new-tokens/generated/geyser_pb2.pyi`

The file `geyser_pb2.pyi` contains type hints for protocol buffer messages related to the Solana blockchain, specifically for handling subscription requests and various data structures like transactions and blocks. Its main purpose is to provide a Python interface for developers to interact with the Solana storage protocol, facilitating easier integration and manipulation of blockchain data in Python applications.

### 📄 `learning-examples/listen-new-tokens/generated/geyser_pb2_grpc.py`

The file `geyser_pb2_grpc.py` is an auto-generated gRPC Python module that defines client and server classes corresponding to services defined in Protocol Buffers (protobuf). Its main purpose is to facilitate communication between a gRPC client and server by providing the necessary method stubs and handlers for various RPC calls related to the "Geyser" service, such as subscribing to updates and querying block information.

### 📄 `learning-examples/listen-new-tokens/generated/solana_storage_pb2.py`

The file `solana_storage_pb2.py` is an auto-generated Python module that contains protocol buffer definitions for the Solana blockchain's storage structures, specifically related to confirmed blocks and transactions. Its main purpose is to facilitate serialization and deserialization of data structures used in communication between services in the Solana ecosystem, ensuring that data is correctly formatted and understood across different components of the project.

### 📄 `learning-examples/listen-new-tokens/generated/solana_storage_pb2.pyi`

The file `solana_storage_pb2.pyi` contains type annotations for protocol buffer message classes related to the Solana blockchain, specifically defining structures for transactions, blocks, and associated metadata. Its main purpose is to provide a Python interface for interacting with serialized data formats used in Solana, enabling developers to work with blockchain data in a type-safe manner.

### 📄 `learning-examples/listen-new-tokens/generated/solana_storage_pb2_grpc.py`

The file `solana_storage_pb2_grpc.py` is an auto-generated Python module that contains client and server classes for gRPC services defined using Protocol Buffers. Its main purpose is to facilitate communication between a client and server in a gRPC-based application, ensuring compatibility with the specified version of the gRPC library.

### 📄 `learning-examples/listen-new-tokens/listen_blocksubscribe.py`

The file `listen_blocksubscribe.py` is a Python script that connects to a Solana blockchain WebSocket to listen for 'create' instructions related to the Pump.fun program. Its main purpose is to decode transaction data from Solana blocks, extracting relevant information such as mint and user details, and printing this data for further processing or analysis.

### 📄 `learning-examples/listen-new-tokens/listen_geyser.py`

The file `listen_geyser.py` is a Python script that monitors the Solana blockchain for the creation of new Pump.fun tokens using the Geyser gRPC API. Its primary role is to decode transaction instructions related to token creation, extract relevant details such as the token's name, symbol, and mint address, and display this information in real-time. The script requires authentication via a Geyser API token and supports both Basic and X-Token authentication methods.

### 📄 `learning-examples/listen-new-tokens/listen_logsubscribe.py`

The file `listen_logsubscribe.py` is a Python script that establishes a WebSocket connection to listen for new token creations on the Solana blockchain, specifically monitoring logs for 'Create' instructions related to the Pump.fun program. Its main purpose is to decode and print details of these newly created tokens, such as their name, symbol, and mint address, providing a real-time feed of token creation events for further analysis or monitoring.

### 📄 `learning-examples/listen-new-tokens/listen_logsubscribe_abc.py`

The file `listen_logsubscribe_abc.py` is a Python script that listens for new token creations on the Solana blockchain via a WebSocket connection. Its main purpose is to monitor logs for specific 'Create' instructions, decode the relevant token details (such as name, symbol, and mint address), and calculate the associated bonding curve address for each newly created token.

### 📄 `learning-examples/listen-new-tokens/listen_pumpportal.py`

The file `listen_pumpportal.py` is a Python script that establishes a WebSocket connection to the PumpPortal API to listen for new token creations. Its main purpose is to subscribe to events related to new tokens, process incoming data, and print detailed information about each newly created token, including its name, address, creator, and market metrics.

### 📄 `learning-examples/listen-new-tokens/proto/geyser.proto`

The `geyser.proto` file defines a gRPC service for interacting with a Solana blockchain, providing methods for subscribing to updates, querying block information, and validating blockhashes. Its main purpose is to facilitate real-time data streaming and retrieval of blockchain state, including account updates, transaction statuses, and block details, which are essential for applications that require live updates from the Solana network.

### 📄 `learning-examples/listen-new-tokens/proto/solana-storage.proto`

The file `solana-storage.proto` defines the protocol buffer messages and structures used for representing confirmed blocks and transactions in the Solana blockchain. Its main purpose is to facilitate the serialization and deserialization of blockchain data, enabling efficient communication between services that interact with Solana's storage and transaction processing systems.

### 📄 `learning-examples/manual_buy.py`

The file `manual_buy.py` is a Python script designed to facilitate the purchase of tokens on the Solana blockchain using a bonding curve mechanism. Its main purpose is to connect to a Solana RPC endpoint, retrieve the current state of a specified bonding curve, calculate the appropriate token price, and execute a transaction to buy tokens while handling potential errors and retries.

### 📄 `learning-examples/manual_sell.py`

The file `manual_sell.py` contains an implementation for selling tokens on the Solana blockchain using a bonding curve mechanism. Its main purpose is to facilitate the process of selling tokens by interacting with the Solana network, retrieving token balances, calculating prices based on the bonding curve state, and executing the sell transaction while managing slippage and retries.

### 📄 `learning-examples/mint_and_buy.py`

The file `mint_and_buy.py` contains Python code for interacting with the Solana blockchain to create and purchase a custom token, referred to as a "pump.fun" token. Its main purpose is to facilitate the minting of a new token and the execution of a buy transaction, managing various blockchain accounts and instructions necessary for these operations. This file is integral to the project's functionality of token management and trading on the Solana network.

### 📄 `learning-examples/pumpswap/get_pumpswap_pools.py`

The file `get_pumpswap_pools.py` is a Python module designed to interact with the Pump AMM (Automated Market Maker) program on the Solana blockchain. Its main purpose is to retrieve market addresses based on a specified base mint and to fetch and parse market data, including pool addresses and various attributes related to liquidity pools. This functionality is essential for applications that require access to decentralized finance (DeFi) market data on the Solana network.

### 📄 `learning-examples/pumpswap/manual_buy_pumpswap.py`

The file `manual_buy_pumpswap.py` provides an interface for interacting with the PUMP Automated Market Maker (AMM) program on the Solana blockchain. Its main purpose is to facilitate operations such as finding market addresses, fetching market data, calculating token prices, and executing token purchases with slippage protection, thereby enabling users to engage in trading activities on the PUMP AMM platform.

### 📄 `learning-examples/pumpswap/manual_sell_pumpswap.py`

The file `manual_sell_pumpswap.py` provides functionality for interacting with the PUMP Automated Market Maker (AMM) on the Solana blockchain. Its main purpose is to facilitate the selling of tokens by fetching market data, calculating token prices, and ensuring slippage protection during transactions, while also managing associated token accounts.

### 📄 `learning-examples/raw_bondingCurve_from_getAccountInfo.json`

The file 'learning-examples/raw_bondingCurve_from_getAccountInfo.json' contains a JSON-RPC response that includes account information retrieved from a blockchain, specifically detailing the account's data, ownership, and associated lamports. Its main purpose is to provide a structured representation of account details for further processing or analysis within a blockchain-related project, particularly in the context of bonding curves.

### 📄 `learning-examples/raw_buy_tx_from_getTransaction.json`

The file 'raw_buy_tx_from_getTransaction.json' contains a JSON representation of a transaction on a blockchain, detailing the execution of multiple token transfer instructions and their associated metadata. Its main purpose is to provide a structured format for analyzing the transaction's components, including compute units consumed, log messages, and changes in account balances, which is essential for debugging and understanding transaction flows within the project.

### 📄 `learning-examples/raw_create_tx_from_getTransaction.json`

The file 'learning-examples/raw_create_tx_from_getTransaction.json' contains a JSON-RPC response detailing the result of a blockchain transaction, including metadata such as block time, fees, and a series of inner instructions executed during the transaction. Its main purpose is to provide a structured representation of the transaction's execution flow, showcasing various operations like account creation, token minting, and transfers, which are essential for understanding how transactions are processed in the blockchain project.

### 📄 `pyproject.toml`

The `pyproject.toml` file defines the configuration for the Python project "pump_bot," including its metadata, dependencies, and development tools. Its main purpose is to specify project details such as name, version, and required Python version, as well as to manage dependencies and linting configurations using the Ruff tool. This file serves as a central point for project setup and dependency management, facilitating development and ensuring compatibility.

### 📄 `src/__init__.py`

The file `src/__init__.py` serves as an initializer for the `src` package, allowing it to be treated as a module in Python. It may contain package-level documentation, import statements, or initialization code, establishing the structure and accessibility of the package's components. Its main purpose is to facilitate the organization and modularization of the project's codebase.

### 📄 `src/bot_runner.py`

The file `src/bot_runner.py` is responsible for initializing and running trading bots based on configurations specified in YAML files. Its main purpose is to load bot configurations, validate platform compatibility, set up logging, and manage the execution of multiple bot instances concurrently using asynchronous programming.

### 📄 `src/cleanup/__init__.py`

The file 'src/cleanup/__init__.py' serves as an initializer for the 'cleanup' package, allowing Python to recognize the directory as a package. It may contain package-level documentation or import statements to expose specific modules or functions for easier access. Its main purpose is to facilitate the organization and modularization of the cleanup-related functionalities within the project.

### 📄 `src/cleanup/manager.py`

The file `src/cleanup/manager.py` contains the `AccountCleanupManager` class, which is responsible for safely cleaning up associated token accounts (ATAs) after trading sessions on the Solana blockchain. Its main purpose is to manage the burning of any remaining tokens and the closing of ATAs, ensuring that accounts are properly handled to avoid unnecessary fees or clutter in the wallet.

### 📄 `src/cleanup/modes.py`

The file `src/cleanup/modes.py` contains functions that determine and handle various cleanup operations based on specific trading events, such as failures, sales, or post-session activities. Its main purpose is to facilitate the management of account cleanup processes by utilizing the `AccountCleanupManager`, ensuring that resources are properly managed and cleaned up in response to different trading scenarios.

### 📄 `src/config_loader.py`

The `src/config_loader.py` file is responsible for loading and validating configuration settings for a bot from a YAML file, ensuring that all required fields and specific validation rules are met. Its main purpose is to facilitate the configuration process by resolving environment variables, validating platform compatibility, and enforcing rules for various configuration parameters, thereby ensuring that the bot operates correctly across different platforms.

### 📄 `src/core/__init__.py`

The file 'src/core/__init__.py' serves as an initializer for the 'core' package in a Python project, allowing the directory to be recognized as a package. It typically contains import statements for modules or functions that should be accessible when the package is imported, facilitating organized access to core functionalities of the project.

### 📄 `src/core/client.py`

The file `src/core/client.py` implements an asynchronous client for interacting with the Solana blockchain, providing methods for operations such as fetching account information, sending transactions, and confirming transaction status. Its main purpose is to abstract the complexities of Solana's RPC API, allowing for efficient blockchain operations while managing tasks like updating the latest blockhash in the background.

### 📄 `src/core/priority_fee/__init__.py`

The file `src/core/priority_fee/__init__.py` defines an abstract base class, `PriorityFeePlugin`, for implementing priority fee calculation plugins within the project. Its main purpose is to provide a standardized interface for calculating priority fees, allowing for different implementations to be created while ensuring they adhere to the defined method signature.

### 📄 `src/core/priority_fee/dynamic_fee.py`

The file `dynamic_fee.py` defines the `DynamicPriorityFee` class, which implements a plugin for dynamically calculating priority fees using the Solana blockchain's `getRecentPrioritizationFees` method. Its main purpose is to fetch and compute the median priority fee based on recent transaction data, allowing users to optimize their transaction speed and cost on the Solana network.

### 📄 `src/core/priority_fee/fixed_fee.py`

The file `fixed_fee.py` defines the `FixedPriorityFee` class, which is a plugin for managing a fixed priority fee in microlamports. Its main purpose is to provide a method for retrieving the fixed fee amount, returning `None` if the fee is set to zero, thereby facilitating consistent fee handling within the broader priority fee management system of the project.

### 📄 `src/core/priority_fee/manager.py`

The file `manager.py` contains the `PriorityFeeManager` class, which is responsible for calculating and validating priority fees for transactions in a Solana blockchain context. Its main purpose is to manage both dynamic and fixed fee calculations, allowing for configurable parameters such as extra fees and hard caps, thereby ensuring that transaction fees are appropriately set based on the project's requirements.

### 📄 `src/core/pubkeys.py`

The file `src/core/pubkeys.py` defines system-level addresses and constants used for operations on the Solana blockchain. Its main purpose is to provide a centralized module that contains essential addresses and constants, ensuring consistency across different platforms while allowing platform-specific implementations to manage their own addresses.

### 📄 `src/core/wallet.py`

The file `src/core/wallet.py` contains a `Wallet` class that manages a Solana wallet, enabling operations such as retrieving the wallet's public key and associated token addresses for transactions. Its main purpose is to facilitate the handling of private keys and keypairs for trading operations on the Solana blockchain.

### 📄 `src/geyser/generated/geyser_pb2.py`

The file `geyser_pb2.py` is an automatically generated Python module that contains protocol buffer definitions for the Geyser project, specifically based on the `geyser.proto` file. Its main purpose is to facilitate the serialization and deserialization of structured data used in communication between components of the Geyser system, particularly for handling subscription requests and updates related to accounts, transactions, and blocks in a Solana-based environment.

### 📄 `src/geyser/generated/geyser_pb2.pyi`

The file `geyser_pb2.pyi` contains type hints for protocol buffer messages related to the Solana blockchain, specifically defining data structures for subscription requests and various transaction and block-related entities. Its main purpose is to provide a type-safe interface for developers working with the Solana storage protocol, facilitating the integration of protocol buffer messages within Python code.

### 📄 `src/geyser/generated/geyser_pb2_grpc.py`

The file `geyser_pb2_grpc.py` is an auto-generated Python module that defines gRPC client and server classes based on Protocol Buffers (protobuf) specifications for a service named "Geyser." Its main purpose is to facilitate remote procedure calls (RPCs) by providing methods for subscribing to updates and querying various data points such as block height and validity of block hashes, while ensuring compatibility with the gRPC library version.

### 📄 `src/geyser/generated/solana_storage_pb2.py`

The file `solana_storage_pb2.py` is an automatically generated Python module that defines protocol buffer (protobuf) messages and their structures for the Solana blockchain's storage system, based on the `solana-storage.proto` definition. Its main purpose is to facilitate communication between services by providing a structured format for confirmed blocks, transactions, and related data types within the Solana ecosystem, enabling efficient serialization and deserialization of these data structures.

### 📄 `src/geyser/generated/solana_storage_pb2.pyi`

The file `solana_storage_pb2.pyi` contains type hints for Protocol Buffers (protobuf) message definitions related to the Solana blockchain. Its main purpose is to provide a Python interface for interacting with serialized data structures, such as transactions and blocks, facilitating type checking and autocompletion in development environments. This file is essential for developers working with Solana's data structures in Python, ensuring proper usage of the protobuf messages defined in the corresponding `.proto` files.

### 📄 `src/geyser/generated/solana_storage_pb2_grpc.py`

The file `solana_storage_pb2_grpc.py` is an auto-generated Python module that contains client and server classes for gRPC services defined using Protocol Buffers. Its main purpose is to facilitate communication between clients and servers in a gRPC-based architecture, ensuring compatibility with the specified version of the gRPC library.

### 📄 `src/geyser/proto/geyser.proto`

The file `geyser.proto` defines the protocol buffers for a Geyser service, which facilitates real-time streaming and querying of blockchain data, specifically for the Solana network. Its main purpose is to provide a structured interface for subscribing to updates on accounts, slots, transactions, and blocks, as well as for querying the latest blockhash, block height, and other related information, enabling efficient communication between clients and the blockchain.

### 📄 `src/geyser/proto/solana-storage.proto`

The file `solana-storage.proto` defines Protocol Buffers messages for representing confirmed blocks and transactions within the Solana blockchain ecosystem. Its main purpose is to facilitate the serialization and deserialization of data structures related to blockchain transactions, including transaction metadata, rewards, and block details, enabling efficient communication between services in the project.

### 📄 `src/interfaces/core.py`

The file `src/interfaces/core.py` defines core interfaces and abstract base classes for a multi-platform trading bot architecture, facilitating unified trading operations across various protocols. Its main purpose is to establish a structured framework for implementing platform-specific functionalities, such as address management, instruction building, and price calculations, ensuring that different trading platforms can be integrated seamlessly.

### 📄 `src/mcp_client.py`

The file `src/mcp_client.py` implements an asynchronous client for interacting with a machine learning agent that manages trading bots. Its main purpose is to facilitate communication between the user and the agent, allowing the execution of commands to control the bots, while also handling logging and session management. The client initiates a subprocess for the server and processes user queries to enable, start, stop, and disable trading bots.

### 📄 `src/mcp_server.py`

The file `src/mcp_server.py` implements a trading bot for interacting with the Solana blockchain, utilizing the FastMCP framework to facilitate token buying, selling, and listening for new tokens. Its main purpose is to initialize core components such as the Solana client, wallet, and fee manager, and to provide tools for executing trades and monitoring token events on specified platforms.

### 📄 `src/monitoring/__init__.py`

The file 'src/monitoring/__init__.py' serves as an initializer for the monitoring module, allowing it to be treated as a package in Python. It may contain import statements or package-level variables that facilitate the organization and accessibility of monitoring-related functionalities within the project. Its main purpose is to define the module's interface and ensure that submodules are properly recognized and utilized.

### 📄 `src/monitoring/base_listener.py`

The file `src/monitoring/base_listener.py` defines an abstract base class, `BaseTokenListener`, for WebSocket token listeners that is designed to be platform-agnostic. Its main purpose is to provide a framework for listening to token creation events, allowing subclasses to implement specific token handling logic while optionally filtering by platform.

### 📄 `src/monitoring/listener_factory.py`

The file `listener_factory.py` defines a `ListenerFactory` class responsible for creating platform-aware token listeners based on specified configurations. Its main purpose is to provide a centralized mechanism for generating different types of listeners (e.g., logs, blocks, geyser, and pumpportal) while ensuring compatibility with various platforms and handling necessary parameters for each listener type.

### 📄 `src/monitoring/universal_block_listener.py`

The file `src/monitoring/universal_block_listener.py` implements a universal block listener that connects to various blockchain platforms via WebSocket to monitor and listen for new token creations. Its main purpose is to provide a flexible and extensible interface for tracking token events across multiple platforms, allowing for customizable filtering and handling of token information through callbacks.

### 📄 `src/monitoring/universal_geyser_listener.py`

The file `universal_geyser_listener.py` implements a `UniversalGeyserListener` class that connects to a Geyser endpoint to monitor token creation events across multiple platforms. Its primary role is to facilitate real-time token monitoring by establishing a gRPC connection, subscribing to updates, and processing token information while allowing for filtering based on specific criteria.

### 📄 `src/monitoring/universal_logs_listener.py`

The file `src/monitoring/universal_logs_listener.py` implements a universal logs listener that connects to a WebSocket endpoint to monitor token creation events across multiple platforms. Its main purpose is to facilitate the real-time detection of new tokens by subscribing to logs from various platforms, processing the incoming data, and invoking a callback function when a new token is detected, while also providing filtering options based on token attributes.

### 📄 `src/monitoring/universal_pumpportal_listener.py`

The `universal_pumpportal_listener.py` file implements a WebSocket listener for monitoring new token creations across multiple platforms using the PumpPortal service. Its main purpose is to establish a connection to the PumpPortal, receive token creation events, and process these events through platform-specific processors, allowing for flexible monitoring based on user-defined criteria.

### 📄 `src/platforms/__init__.py`

The `src/platforms/__init__.py` file serves as a platform factory and registry for managing multiple trading platforms within the project. It centralizes the instantiation and access to platform-specific implementations of trading interfaces, facilitating the integration of platforms with IDL (Interface Definition Language) support. The main role of this module is to register, create, and manage instances of various platform implementations, ensuring that the project can efficiently handle multiple trading environments.

### 📄 `src/platforms/letsbonk/__init__.py`

The file `src/platforms/letsbonk/__init__.py` serves as the initialization module for the LetsBonk platform, facilitating convenient imports of various platform implementations. Its main purpose is to streamline access to key components like address providers, curve managers, and event parsers, while also managing platform registration through a central factory.

### 📄 `src/platforms/letsbonk/address_provider.py`

The file `address_provider.py` implements the `AddressProvider` interface specifically for the LetsBonk platform, part of the Raydium LaunchLab. It defines a class that provides various addresses and Program Derived Addresses (PDAs) necessary for interacting with the LetsBonk ecosystem, including methods for deriving pool and vault addresses, as well as user token account addresses. The main purpose of this file is to facilitate address management and retrieval for token operations within the LetsBonk platform.

### 📄 `src/platforms/letsbonk/curve_manager.py`

The `curve_manager.py` file implements the `CurveManager` interface specifically for the LetsBonk platform, which is part of the Raydium LaunchLab. Its primary role is to manage pool operations, including retrieving pool states, calculating token prices, and determining expected token amounts for buy and sell operations using an IDL-based decoding approach.

### 📄 `src/platforms/letsbonk/event_parser.py`

The file `event_parser.py` implements the `EventParser` interface specifically for the LetsBonk platform, focusing on parsing token creation events from various sources using IDL-based parsing. Its main role is to extract relevant token information from transaction logs and instruction data, enabling the identification and processing of token creation events within the LetsBonk ecosystem.

### 📄 `src/platforms/letsbonk/instruction_builder.py`

The `instruction_builder.py` file implements the `InstructionBuilder` interface specifically for the LetsBonk platform (Raydium LaunchLab). Its main purpose is to construct buy and sell instructions tailored to the LetsBonk ecosystem, utilizing IDL-based discriminators to facilitate transactions involving token exchanges on the platform.

### 📄 `src/platforms/letsbonk/pumpportal_processor.py`

The file `pumpportal_processor.py` contains a class `LetsBonkPumpPortalProcessor`, which is responsible for processing token data specific to the LetsBonk platform from the PumpPortal. Its main role is to validate and extract relevant information from token data, derive necessary addresses, and return a structured `TokenInfo` object for further use in the project.

### 📄 `src/platforms/pumpfun/__init__.py`

The `src/platforms/pumpfun/__init__.py` file serves as the initialization module for the Pump.Fun platform, facilitating convenient imports of various components related to the platform's functionality. Its main purpose is to streamline access to core implementations, such as address management and event parsing, by exporting them for direct use, while also indicating that platform registration is managed by a central factory.

### 📄 `src/platforms/pumpfun/address_provider.py`

The file `address_provider.py` implements the `AddressProvider` interface specifically for the Pump.Fun platform, providing functionality to derive and manage various program-derived addresses (PDAs) and associated token accounts. Its main purpose is to encapsulate all pump.fun-specific addresses and facilitate the retrieval of necessary addresses for operations such as trading and volume accumulation within the platform.

### 📄 `src/platforms/pumpfun/curve_manager.py`

The `curve_manager.py` file implements the `CurveManager` interface specifically for the Pump.Fun platform, focusing on bonding curve operations. Its main role is to manage and calculate various aspects of bonding curves, such as retrieving pool states, calculating token prices, and determining expected outputs for buy and sell operations using IDL-based decoding.

### 📄 `src/platforms/pumpfun/event_parser.py`

The file `event_parser.py` implements the `EventParser` interface specifically for the Pump.Fun platform, focusing on parsing token creation events from transaction logs using IDL-based event parsing. Its main role is to extract and decode relevant event data from logs, validate the presence of required fields, and return structured token information when a token creation event is detected.

### 📄 `src/platforms/pumpfun/instruction_builder.py`

The `instruction_builder.py` file implements the `InstructionBuilder` interface specifically for the Pump.Fun platform, facilitating the creation of buy and sell instructions using IDL-based discriminators. Its primary role is to construct the necessary instructions for executing token transactions on the Pump.Fun platform, including handling account metadata and instruction data packaging for both buying and selling operations.

### 📄 `src/platforms/pumpfun/pumpportal_processor.py`

The file `pumpportal_processor.py` contains a class `PumpFunPumpPortalProcessor`, which is designed to handle and process token data specific to the PumpFun platform from the PumpPortal. Its main role is to validate incoming token data, extract necessary information, and return a structured `TokenInfo` object, facilitating the integration of PumpFun tokens within the broader application ecosystem.

### 📄 `src/trading/__init__.py`

The file 'src/trading/__init__.py' serves as an initializer for the 'trading' package, allowing it to be recognized as a module in Python. It typically contains import statements for submodules or functions, facilitating access to the package's features and functionalities. Its main purpose is to organize and expose the trading-related components of the project for easier use and integration.

### 📄 `src/trading/base.py`

The file `src/trading/base.py` contains enhanced base classes and interfaces for trading operations, integrating new platform support while ensuring backward compatibility with existing code. Its main role is to define the `Trader` abstract class and related data structures, such as `TradeResult` and `TokenInfo`, facilitating the execution of trading operations and the management of token information across different platforms.

### 📄 `src/trading/platform_aware.py`

The file `platform_aware.py` contains implementations for platform-aware trading operations, specifically for buying and selling tokens across various platforms. Its main purpose is to facilitate token transactions by dynamically adapting to different platform-specific requirements, thereby removing hardcoded dependencies and enhancing flexibility in trading operations.

### 📄 `src/trading/position.py`

The file `src/trading/position.py` defines a `Position` class for managing trading positions, including functionalities for take profit and stop loss conditions. Its main purpose is to encapsulate the details of an active trading position, track its status, and provide methods for evaluating exit conditions and calculating profit/loss.

### 📄 `src/trading/universal_trader.py`

The file `src/trading/universal_trader.py` defines a `UniversalTrader` class, which serves as a trading coordinator capable of operating across various platforms by abstracting platform-specific details. Its main purpose is to facilitate automated trading by managing buy and sell operations, handling platform interactions, and implementing trading strategies while ensuring flexibility and configurability for different trading scenarios.

### 📄 `src/utils/__init__.py`

The file 'src/utils/__init__.py' serves as an initializer for the 'utils' package, allowing it to be treated as a module in Python. It typically contains import statements for utility functions or classes that are intended to be accessible when the package is imported, facilitating code organization and reusability within the project.

### 📄 `src/utils/idl_manager.py`

The file `src/utils/idl_manager.py` serves as a centralized manager for Interface Definition Language (IDL) parsers specifically tailored for various Solana platforms. Its main role is to streamline the loading and management of IDL files, ensuring that parsers are not redundantly loaded across different platform implementations, thereby enhancing efficiency and organization within the project.

### 📄 `src/utils/idl_parser.py`

The `idl_parser.py` file is a module designed for parsing and decoding Anchor IDL (Interface Definition Language) files used in Solana programs. Its main purpose is to provide functionality for loading IDL files, decoding instruction data and events, and validating the structure and sizes of instructions and events based on the definitions provided in the IDL.

### 📄 `src/utils/logger.py`

The file `src/utils/logger.py` contains utilities for logging within the pump.fun trading bot, providing functions to create and manage loggers. Its main purpose is to facilitate logging configuration, allowing for the retrieval of loggers by name and setting up file logging to capture log messages in a specified log file.

### 📄 `uv.lock`

The `uv.lock` file is a dependency lock file that specifies the exact versions of packages required for a Python project, ensuring consistent installations across different environments. It includes metadata such as the Python version requirement and detailed information about each package, including their source URLs and hashes for verification. Its main purpose is to facilitate reproducible builds by locking dependencies to specific versions, preventing potential issues from version mismatches.
