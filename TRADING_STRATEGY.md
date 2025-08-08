# PumpFun Trading Strategy for AI Agents

## Overview
This trading strategy is designed for AI agents to automatically identify and trade newly launched tokens on pump.fun by analyzing bonding curve activity and selecting tokens with the highest SOL reserves.

## Strategy Logic

### 1. Data Collection Phase
**Objective**: Continuously monitor and log new token launches
- Use `start_token_listener_with_logging(duration_seconds=300, log_file="new_tokens.json")` to listen for new tokens for 5 minutes
- This runs in background and logs all discovered tokens to JSON with metadata:
  - mint address
  - symbol and name  
  - creator address
  - bonding curve addresses
  - timestamp
  - platform info

### 2. Analysis Phase
**Objective**: Identify the most promising trading opportunities
- Use `read_logged_tokens(hours_ago=1)` to see recently discovered tokens
- Use `analyze_logged_tokens_bonding_curves(hours_ago=1, max_tokens=10)` to:
  - Check bonding curve status for recent tokens
  - Calculate SOL reserves in each bonding curve
  - Determine completion percentage
  - Filter out completed/migrated tokens
  - Rank tokens by SOL reserves (higher = more activity/demand)

### 3. Selection Criteria
**Best tokens have:**
- High SOL reserves (indicates strong buying pressure)
- Low completion percentage (< 80% to avoid migration risk)
- Recent creation (< 2 hours old for maximum alpha)
- Active bonding curve (not completed/migrated)

### 4. Execution Phase
**Objective**: Execute trades on the best opportunities
- Use `execute_trading_strategy(hours_ago=1, buy_amount=0.001)` for automatic execution
- Or manually buy using `buy_token(mint, sol_amount, slippage=0.05)`

## Agent Instructions

### Initial Setup
1. Start the token listener to begin collecting data:
   ```
   start_token_listener_with_logging(duration_seconds=300)
   ```

2. Wait 5-10 minutes to collect initial token data

### Continuous Trading Loop
Every 10-15 minutes, execute this sequence:

1. **Check Recent Activity**
   ```
   read_logged_tokens(hours_ago=2)
   ```

2. **Analyze Opportunities** 
   ```
   analyze_logged_tokens_bonding_curves(hours_ago=1, max_tokens=15)
   ```

3. **Execute Best Trade**
   ```
   execute_trading_strategy(hours_ago=1, buy_amount=0.001)
   ```

4. **Monitor Positions** (optional)
   ```
   get_wallet_balance()
   get_token_balance(mint_address)
   ```

### Risk Management Rules

1. **Position Sizing**: Never risk more than 0.001-0.005 SOL per trade
2. **Time Limits**: Only trade tokens < 2 hours old
3. **Completion Limits**: Avoid tokens > 80% complete (migration risk)
4. **Diversification**: Don't trade the same token twice
5. **Stop Conditions**: Stop trading if wallet balance < 0.01 SOL

### Sample Agent Prompt

```
You are a PumpFun trading bot. Your goal is to identify and trade profitable new tokens on pump.fun.

STRATEGY:
1. Start by listening for new tokens: start_token_listener_with_logging(300)
2. Every 10 minutes, analyze recent tokens: analyze_logged_tokens_bonding_curves(hours_ago=1)
3. Execute trades on tokens with highest SOL reserves: execute_trading_strategy(buy_amount=0.001)
4. Monitor your wallet balance and stop if it gets too low

RULES:
- Only trade tokens less than 2 hours old
- Avoid tokens more than 80% complete
- Risk only 0.001 SOL per trade
- Focus on tokens with highest SOL reserves
- Log all activities and explain your decisions

Begin by starting the token listener and setting up your trading loop.
```

## Available MCP Tools

### Data Collection
- `start_token_listener_with_logging(duration_seconds, log_file)` - Listen and log new tokens
- `read_logged_tokens(log_file, hours_ago)` - Read logged token data

### Analysis
- `analyze_logged_tokens_bonding_curves(log_file, hours_ago, max_tokens)` - Analyze bonding curves
- `get_bonding_curve_state(mint)` - Get individual token curve state
- `calculate_buy_amount(mint, sol_amount)` - Calculate expected tokens

### Trading
- `execute_trading_strategy(hours_ago, buy_amount, max_tokens_to_analyze)` - Full auto strategy
- `buy_token(mint, sol_amount, slippage)` - Manual buy execution
- `get_token_price(mint)` - Get current token price

### Monitoring  
- `get_wallet_balance()` - Check SOL balance
- `get_wallet_address()` - Get wallet address
- `get_token_balance(mint)` - Check token balance

## Success Metrics
- Positive ROI over time
- Successful identification of high-activity tokens
- Minimal exposure to completed/migrated tokens
- Consistent execution without errors

## Risks
- **Migration Risk**: Tokens completing bonding curve migrate to Raydium
- **Rug Pulls**: New tokens can be abandoned by creators
- **High Volatility**: Token prices can change rapidly
- **Gas Fees**: Transaction costs reduce profit margins
- **MEV**: Front-running by other bots

## Optimization Opportunities
- Adjust selection criteria based on performance
- Implement more sophisticated scoring algorithms
- Add technical analysis indicators
- Include social sentiment analysis
- Implement dynamic position sizing