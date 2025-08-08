# PumpFun Trading Bot MCP Server

A complete MCP (Model Context Protocol) server for automated pump.fun token trading with support for both pre-graduation (bonding curve) and post-graduation (PumpSwap AMM) tokens.

## Features

- **Universal Trading**: Automatically detects pre/post graduation tokens and uses appropriate trading method
- **Pre-graduation Trading**: Bonding curve trading via pump.fun protocol
- **Post-graduation Trading**: PumpSwap AMM trading for migrated tokens
- **Token Monitoring**: Real-time token listener with background logging
- **Trading Strategy**: Built-in analysis and execution of optimal trades
- **MCP Integration**: Works with Claude Code and other MCP-compatible clients

## Quick Setup

### 1. Clone and Install Dependencies

```bash
git clone <your-repo-url>
cd claude-code-mcp-pump

# Create virtual environment in pump-fun-bot directory
cd pump-fun-bot
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt  # or use uv/poetry based on what's in pump-fun-bot
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
# Solana RPC Configuration
SOLANA_NODE_RPC_ENDPOINT=https://mainnet.helius-rpc.com/?api-key=YOUR_API_KEY
SOLANA_NODE_WSS_ENDPOINT=wss://mainnet.helius-rpc.com/?api-key=YOUR_API_KEY

# Your Solana wallet private key (base58 encoded)
SOLANA_PRIVATE_KEY=your_private_key_here
```

**⚠️ Security Warning**: Never commit your private key to git. Keep your `.env` file secure and consider using a dedicated trading wallet.

### 3. Configure MCP Client

Add this configuration to your MCP client settings (e.g., `~/.cursor/mcp.json` for Cursor):

```json
{
    "mcpServers": {
        "pumpfun_trading_bot": {
            "command": "/path/to/your/claude-code-mcp-pump/pump-fun-bot/.venv/bin/python",
            "args": [
                "/path/to/your/claude-code-mcp-pump/trading_bot_sdk.py"
            ],
            "env": {
                "SOLANA_NODE_RPC_ENDPOINT": "https://mainnet.helius-rpc.com/?api-key=YOUR_API_KEY",
                "SOLANA_NODE_WSS_ENDPOINT": "wss://mainnet.helius-rpc.com/?api-key=YOUR_API_KEY",
                "SOLANA_PRIVATE_KEY": "your_private_key_here"
            }
        }
    }
}
```

**Replace the paths and credentials with your actual values:**
- Update `/path/to/your/` with your actual directory path
- Replace `YOUR_API_KEY` with your Helius API key
- Replace `your_private_key_here` with your base58-encoded private key

### 4. Test the Setup

```bash
# Test the MCP server directly
python trading_bot_sdk.py

# Should show FastMCP startup message
```

## Available MCP Tools

The server provides these tools for AI agents:

### Core Trading
- `buy_token(mint, sol_amount, slippage)` - Universal buy (auto-detects pre/post graduation)
- `sell_token(mint, slippage)` - Universal sell (auto-detects pre/post graduation)
- `get_token_status(mint)` - Check if token is pre or post graduation

### Wallet & Balance
- `get_wallet_balance()` - Get SOL balance
- `get_wallet_address()` - Get wallet public address
- `get_token_balance(mint)` - Get specific token balance

### Market Analysis
- `get_token_price(mint)` - Get current token price
- `get_bonding_curve_state(mint)` - Get bonding curve progress
- `calculate_buy_amount(mint, sol_amount)` - Calculate tokens for SOL amount

### Token Monitoring
- `start_token_listener_with_logging(duration, log_file)` - Start background token listener
- `stop_token_listener(log_file)` - Stop token listener
- `read_logged_tokens(log_file, hours_ago)` - Read logged tokens
- `analyze_logged_tokens_bonding_curves()` - Analyze best trading opportunities

### Trading Strategy
- `execute_trading_strategy(hours_ago, buy_amount, max_tokens)` - Execute full strategy

## Trading Strategy

The bot implements this automated strategy:

1. **Monitor**: Start token listener to log new pump.fun tokens
2. **Analyze**: Analyze bonding curve progress and SOL reserves
3. **Select**: Choose tokens with highest SOL reserves (most momentum)
4. **Buy**: Purchase selected tokens (pre or post graduation)
5. **Monitor**: Track token status and migration
6. **Sell**: Sell when tokens migrate or reach profit targets

See `TRADING_STRATEGY.md` for detailed strategy documentation.

## Usage Examples

### Basic Trading
```python
# In your MCP client (Claude Code, etc.)
# Check token status
get_token_status("token_mint_address_here")

# Buy token (auto-detects pre/post graduation)
buy_token("token_mint_address_here", 0.001, 0.05)

# Sell token
sell_token("token_mint_address_here", 0.05)
```

### Automated Strategy
```python
# Start monitoring new tokens
start_token_listener_with_logging(21600, "new_tokens.json")  # 6 hours

# Execute strategy on recent tokens
execute_trading_strategy(1, 0.001, 10)  # Last 1 hour, 0.001 SOL, max 10 tokens
```

## Requirements

- Python 3.8+
- Solana RPC endpoint (Helius recommended)
- SOL for trading and transaction fees
- MCP-compatible client (Claude Code, etc.)

## Security Notes

- Use a dedicated trading wallet with limited funds
- Never share your private key
- Test with small amounts first
- Monitor your trades and balances

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure you're in the pump-fun-bot directory and have activated the virtual environment
2. **RPC errors**: Check your Helius API key and endpoints
3. **Transaction failures**: Ensure sufficient SOL balance for transactions and fees
4. **MCP connection issues**: Verify paths in your MCP client configuration

### Logs and Debugging

The server logs important events. Check console output for transaction details and error messages.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license here]

## Disclaimer

This bot trades real cryptocurrency. Use at your own risk. Always test with small amounts first and never trade more than you can afford to lose.